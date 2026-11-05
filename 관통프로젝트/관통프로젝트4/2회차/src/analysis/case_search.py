"""Phase 0 한글 문자 n-gram TF-IDF 검색. 의미 임베딩/생성 답변이 아니다."""
import argparse
import json
import math
import re
from collections import Counter
from src.collection.client import ROOT


def grams(text):
    text = re.sub(r'\s+', '', text.lower())
    return Counter(text[i:i+n] for n in (2, 3, 4) for i in range(len(text)-n+1))


class CaseSearch:
    def __init__(self, cases):
        # 동일 제목의 게시본이 검색 상위 자리를 중복 점유하지 않게 최신 게시본을 우선한다.
        # 원본 목록은 삭제하지 않으며, 실제 사건이 동일하다고 판정한 것은 아니다.
        by_title = {}
        for case in sorted(cases, key=lambda c: (c.get('published_date') or '', c['case_id'])):
            by_title[case['title']] = case
        self.cases = list(by_title.values())
        self.counts = [grams(c['title'] + '\n' + c['text']) for c in self.cases]
        df = Counter(token for counts in self.counts for token in counts)
        self.idf = {term: math.log((1+len(self.cases))/(1+freq))+1 for term, freq in df.items()}
        self.vectors = [self.vector(counts) for counts in self.counts]

    def vector(self, counts):
        result = {t: (1+math.log(n))*self.idf[t] for t, n in counts.items() if t in self.idf}
        norm = math.sqrt(sum(v*v for v in result.values()))
        return {t: v/norm for t, v in result.items()} if norm else {}

    def search(self, query, k=5, service=None):
        if not isinstance(query, str) or len(query) > 2000 or not 1 <= k <= 20:
            raise ValueError('질문 2000자 이하, 검색 수 1~20만 허용합니다.')
        q = self.vector(grams(query.strip()))
        if not q:
            return []
        hits = []
        for case, vector in zip(self.cases, self.vectors, strict=True):
            if service and case['service'] != service:
                continue
            score = sum(weight*vector.get(term, 0) for term, weight in q.items())
            if score <= 0:
                continue
            # 제목만 일치한 문서는 근거가 아니다. 실제 본문 문단에서 발췌한다.
            paragraphs = [p for p in case['paragraphs'] if len(p['text']) >= 35]
            def paragraph_score(paragraph):
                vector = self.vector(grams(paragraph['text']))
                return sum(v*vector.get(t, 0) for t, v in q.items())
            ranked = sorted(paragraphs, key=paragraph_score, reverse=True)
            hits.append({'case_id': case['case_id'], 'title': case['title'], 'service': case['service'],
                         'score': round(score, 6), 'source_url': case['source_url'],
                         'source_type': case['source_type'], 'published_date': case['published_date'],
                         'retrieved_at': case['retrieved_at'], 'excerpts': ranked[:2]})
        return sorted(hits, key=lambda h: (-h['score'], h['case_id']))[:k]


def validate_citation(cases, case_id, paragraph, quote):
    """다른 문서·없는 문단·변조한 인용을 거부한다."""
    case = next((c for c in cases if c['case_id'] == case_id), None)
    if case is None:
        return False
    source = next((p for p in case['paragraphs'] if p['paragraph'] == paragraph), None)
    return source is not None and isinstance(quote, str) and bool(quote.strip()) and quote in source['text']


def main():
    parser = argparse.ArgumentParser(description='실제 공식 사례 원문 검색: LLM 생성 없음')
    parser.add_argument('query')
    parser.add_argument('--top-k', type=int, default=5)
    args = parser.parse_args()
    cases = json.loads((ROOT / 'data/private/cases.json').read_text('utf-8'))
    print(json.dumps({'mode': '문자 n-gram TF-IDF 검색 원문 발췌',
                      'hits': CaseSearch(cases).search(args.query, args.top_k)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
