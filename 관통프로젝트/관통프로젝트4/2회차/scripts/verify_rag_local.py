"""Real ONNX/Chroma/source cache checks. No GMS calls, no synthetic vectors."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.collection.client import ROOT
from src.rag.config import settings, runtime, fingerprint
from src.rag.data import items, DocumentCollector
from src.rag.embedding import LocalEmbedding
from src.rag.store import Store


def main():
    cfg = settings()
    embed = LocalEmbedding(cfg)
    catalog = items()
    selected = [next(i for i in catalog if i['company'] == c and i['period'] == '2026Q2') for c in ('하나손해보험', '신한EZ손해보험')]
    store = Store(cfg, embed, runtime() / ('verification_' + uuid.uuid4().hex[:12]))
    store.index_items(selected)
    collector = DocumentCollector()
    doc = collector.case_document('fss_case_73')
    a = store.index_doc(selected[0]['item_id'], doc)
    b = store.index_doc(selected[1]['item_id'], doc)
    count = store.docs.count()
    store.index_doc(selected[0]['item_id'], doc)
    repeated = collector.case_document('fss_case_73')
    windows = embed.windows(('보험금 청구와 보장 범위를 확인합니다. ' * 200) + '마지막 문장 보존 확인')
    text = ('보험금 청구와 보장 범위를 확인합니다. ' * 200) + '마지막 문장 보존 확인'
    coverage = bytearray(len(text))
    for start, end, piece in windows:
        coverage[start:end] = b'\1' * (end - start)
    similarity = store.retrieve(selected[0]['item_id'], '추가 서류 요구 진료비 영수증', [doc['doc_id']], method='similarity', top_k=4)
    mmr = store.retrieve(selected[0]['item_id'], '추가 서류 요구 진료비 영수증', [doc['doc_id']], method='mmr', top_k=4)
    smaller = Store(cfg | {'chunk_size': 400, 'chunk_overlap': 30}, embed, runtime() / ('verification_' + uuid.uuid4().hex[:12]))
    smaller.index_items(selected[:1])
    # Use an embedder with the alternate chunking config for this check.
    old_cfg = embed.cfg
    embed.cfg = smaller.cfg
    try:
        small_ids = smaller.index_doc(selected[0]['item_id'], doc)
    finally:
        embed.cfg = old_cfg
    checks = {
        'actual_dimension_384': len(embed.document_vector('보험 민원')) == 384,
        'actual_token_limit_128': embed.limit == 128,
        'every_window_within_limit': all(embed.token_count(w[2]) <= embed.limit for w in windows),
        'all_korean_characters_covered': all(coverage),
        'last_korean_sentence_covered': windows[-1][1] == len(text),
        'reindex_count_stable': count == store.docs.count(),
        'shared_doc_ids_disjoint': not (set(a) & set(b)),
        'other_item_not_mixed': all(s['item_id'] == selected[0]['item_id'] for s in mmr),
        'selected_metadata_first': mmr[0]['chunk_id'] == selected[0]['item_id'],
        'repeat_source_http_zero': collector.client.calls == 0,
        'repeat_body_identical': doc['text'] == repeated['text'],
        'top_k_applied': len(mmr) <= 4 and len(similarity) <= 4,
        'config_uses_new_collections': smaller.signature != store.signature,
        'new_chunks_actually_indexed': bool(small_ids),
    }
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'real_local_model': True, 'gms_calls': 0,
        'checks': checks, 'passed': all(checks.values()), 'source_http_calls': collector.client.calls,
        'cache_hits': collector.client.hits, 'long_text_windows': len(windows),
        'max_window_tokens': max(embed.token_count(w[2]) for w in windows),
        'original_doc_chunks': len(a), 'alternate_chunks': len(small_ids),
        'similarity_ids': [s['chunk_id'] for s in similarity], 'mmr_ids': [s['chunk_id'] for s in mmr],
        'ordering_differs': [s['chunk_id'] for s in similarity] != [s['chunk_id'] for s in mmr]}
    (ROOT / 'reports/rag_local_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
