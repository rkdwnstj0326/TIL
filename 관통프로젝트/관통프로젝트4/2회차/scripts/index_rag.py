"""Build metadata only. External bodies are fetched/indexed at question time."""
import json
import os
from pathlib import Path
import sys
from time import perf_counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.rag.config import settings
from src.rag.data import items
from src.rag.embedding import LocalEmbedding
from src.rag.store import Store


def main():
    start = perf_counter()
    cfg = settings()
    embed = LocalEmbedding(cfg)
    store = Store(cfg, embed)
    catalog = items()
    store.index_items(catalog)
    report = {'items': len(catalog), 'metadata_count': store.meta.count(), 'external_count': store.docs.count(),
        'actual_token_limit': embed.limit, 'dimension': len(embed.document_vector('보험 공시')),
        'signature': store.signature, 'seconds': round(perf_counter()-start, 3), 'gms_calls': 0}
    root = Path(__file__).resolve().parents[1]
    (root / 'reports/rag_index.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
