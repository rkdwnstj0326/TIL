"""Exactly two LangGraph nodes: retrieve -> generate. No GMS calls on import."""
import hashlib
import json
import re
import sqlite3
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from .config import runtime, fingerprint
from .data import candidates, DocumentCollector
from . import prompts


class State(TypedDict, total=False):
    item: dict
    question: str
    history: list
    sources: list
    warnings: list
    in_scope: bool
    result: dict
    steps: list
    scope_issue: str


def validate_keywords(obj):
    if type(obj.get('in_scope')) is not bool or type(obj.get('keywords')) is not list:
        raise ValueError('검색어 JSON 형식 오류')
    words = obj['keywords']
    if len(words) > 5 or any(type(w) is not str or not 1 <= len(w) <= 100 for w in words):
        raise ValueError('검색어 타입·길이 오류')
    return obj


def validate_selection(obj, allowed):
    values = obj.get('selected_ids')
    if type(values) is not list or len(values) > 4 or any(type(x) is not str or x not in allowed for x in values):
        raise ValueError('문서 선별에 허용되지 않은 ID가 있습니다.')
    return list(dict.fromkeys(values))


def validate_answer(obj, sources):
    if type(obj.get('answer')) is not str or not obj['answer'].strip() or len(obj['answer']) > 15000:
        raise ValueError('답변 본문 형식 오류')
    if obj.get('status') not in ('근거 있음', '근거와 상충', '확인 불가'):
        raise ValueError('답변 상태 형식 오류')
    declared = obj.get('cited_numbers')
    if type(declared) is not list or any(type(n) is not int for n in declared):
        raise ValueError('인용 번호 타입 오류')
    cited = sorted({int(n) for n in re.findall(r'\[(\d+)\]', obj['answer'])})
    if '[근거' in obj['answer'] or any(n < 1 or n > len(sources) for n in cited + declared) or set(declared) != set(cited):
        raise ValueError('존재하지 않거나 일치하지 않는 근거 번호')
    if not cited:
        return {'answer': '확인 불가: 답변에 검증 가능한 근거 인용이 없어 결과를 보류했습니다.', 'status': '확인 불가', 'cited_numbers': []}
    return obj | {'cited_numbers': cited}


class QueryCache:
    def __init__(self, path=None):
        self.path = path or runtime() / 'query_cache.sqlite3'
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS entries (key TEXT PRIMARY KEY, value TEXT NOT NULL)')

    def get(self, key):
        with sqlite3.connect(self.path) as db:
            row = db.execute('SELECT value FROM entries WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, key, value):
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO entries VALUES (?,?)', (key, json.dumps(value, ensure_ascii=False)))


class Pipeline:
    def __init__(self, cfg, store, cases, gms=None, collector=None, progress=None, cache=None):
        self.cfg, self.store, self.cases, self.gms = cfg, store, cases, gms
        self.collector = collector or DocumentCollector()
        self.progress = progress or (lambda _: None)
        self.cache = cache or QueryCache()
        self.corpus_hash = hashlib.sha256(json.dumps([(c['case_id'], c['text_sha256']) for c in cases], sort_keys=True).encode()).hexdigest()
        builder = StateGraph(State)
        builder.add_node('retrieve', self.retrieve)
        builder.add_node('generate', self.generate)
        builder.add_edge(START, 'retrieve')
        builder.add_edge('retrieve', 'generate')
        builder.add_edge('generate', END)
        self.graph = builder.compile()

    def retrieve(self, state):
        item, question = state['item'], state['question']
        if not question.strip() or len(question) > 2000:
            raise ValueError('질문은 1~2000자로 입력해 주세요.')
        if item.get('comparison_blocked') and re.search(r'전분기|증감|늘었|줄었|증가|감소|변했',question):
            return {'sources':self.store.retrieve(item['item_id'],question,[]),'warnings':[],
                'in_scope':True,'steps':['definition_change_comparison_blocked'],
                'scope_issue':'2024년2분기 공시기준 개선 전후이므로 전분기 증감 비교를 보류합니다.'}
        requested = re.search(r'(20\d{2})\s*년?\s*([1-4])\s*분기', question)
        if requested:
            period = requested.group(1) + 'Q' + requested.group(2)
            if (period not in item['available_periods']) if 'available_periods' in item else (period not in item['text']):
                return {'sources': self.store.retrieve(item['item_id'], question, []), 'warnings': [],
                    'in_scope': True, 'steps': ['requested_period_not_in_evidence'],
                    'scope_issue': f'요청한 {period} 공시는 현재 근거에 없습니다. 선택 항목은 {item["period"]}입니다.'}
        self.progress('검색어 추출 · 공식 목록에서 후보 탐색')
        key = hashlib.sha256(json.dumps([item['item_id'], question, fingerprint(self.cfg), self.corpus_hash,
                    self.cfg['gms_model'], bool(self.gms), 'prompts-v1'], ensure_ascii=False).encode()).hexdigest()
        cached = self.cache.get(key)
        steps, warnings = [], []
        if cached:
            words, selected, in_scope = cached['keywords'], cached['selected_ids'], cached['in_scope']
            steps.append('keyword_selection_cache_hit')
        else:
            if self.gms:
                extracted = validate_keywords(self.gms.json(prompts.KEYWORDS, {'item': {'company': item['company'], 'period': item['period']}, 'question': question}))
                words, in_scope = extracted['keywords'], extracted['in_scope']
            else:
                words = [question[:100]]
                in_scope = bool(re.search(r'보험|민원|공시|계약|보상|환산|분모|분기|지급|손보|생명|사례|청구|건수', question))
            found = candidates(question, words, self.cases, self.cfg['candidate_limit']) if in_scope else []
            if self.gms and found:
                selected = validate_selection(self.gms.json(prompts.SELECT, {'question': question, 'candidates': [
                    {'id': h['case_id'], 'title': h['title'], 'service': h['service'], 'body': '\n'.join(p['text'] for p in h['excerpts'])[:1700]} for h in found]}), {h['case_id'] for h in found})
            else:
                selected = [h['case_id'] for h in found[:self.cfg['selection_limit']]]
            self.cache.put(key, {'keywords': words, 'selected_ids': selected, 'in_scope': in_scope})
            steps.append('keywords_and_candidates_selected')
        if not in_scope:
            return {'sources': [], 'in_scope': False, 'warnings': [], 'steps': steps + ['out_of_scope']}
        self.progress('선택 공시 우선 수집 · 관련 사례 본문 수집 및 색인')
        allowed_docs = []
        try:
            own = self.collector.own_document(item)
            self.store.index_doc(item['item_id'], own)
            allowed_docs.append(own['doc_id'])
        except (OSError, ValueError, RuntimeError) as error:
            warnings.append('선택 공시 원문을 확인하지 못했습니다. 기존 메타데이터만 사용합니다.')
        # A cache entry is not proof of indexing: collect/verify the actual DB each time.
        for doc_id in selected:
            try:
                doc = self.collector.case_document(doc_id)
                self.store.index_doc(item['item_id'], doc)
                allowed_docs.append(doc_id)
            except (OSError, ValueError, RuntimeError):
                warnings.append('관련 사례 원문 일부를 수집·색인하지 못했습니다.')
        self.progress('항목 ID 필터 · 메타데이터와 의미 검색 근거 병합')
        sources = self.store.retrieve(item['item_id'], question, allowed_docs)
        return {'sources': sources, 'warnings': warnings, 'in_scope': True, 'steps': steps + ['item_filtered_semantic_retrieval']}

    def generate(self, state):
        if not state['in_scope']:
            result = {'answer': '확인 불가: 현재 범위는 보험 공시와 공개 보험 사례입니다. 이 질문에 사용할 근거가 없습니다.',
                      'status': '확인 불가', 'cited_numbers': [], 'mode': '범위 안내'}
        elif self.gms is None:
            result = {'answer': '실제 의미 검색으로 찾은 원문 발췌입니다. GMS 생성·판정은 실행하지 않았습니다.',
                      'status': '생성 미실행', 'cited_numbers': [], 'mode': '원문 발췌'}
        else:
            self.progress('GMS 근거 답변 생성 · 인용 번호 검증')
            response = self.gms.json(prompts.ANSWER, {'question': state['question'],
                'item': {'company': state['item']['company'], 'period': state['item']['period']},
                'history': state.get('history', [])[-4:],
                'mandatory_abstention_reason': state.get('scope_issue'),
                'evidence': [{'number': n + 1, **s} for n, s in enumerate(state['sources'])]})
            result = validate_answer(response, state['sources']) | {'mode': 'GMS 실제 생성'}
            if state.get('scope_issue') and result['status'] != '확인 불가':
                result = {'answer': '확인 불가: ' + state['scope_issue'] + ' [1]', 'status': '확인 불가',
                    'cited_numbers': [1], 'mode': '기간 검사에 따른 보류', 'model_answer_rejected': True}
        used = [state['sources'][n - 1] | {'number': n} for n in result['cited_numbers']]
        result['used_sources'] = used
        return {'result': result, 'steps': state['steps'] + ['generate_and_validate']}

    def run(self, item, question, history=None):
        return self.graph.invoke({'item': item, 'question': question, 'history': history or []})
