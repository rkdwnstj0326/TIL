import hashlib
import json
import os
from pathlib import Path
from dotenv import dotenv_values
from src.collection.client import ROOT

os.environ['LANGSMITH_TRACING'] = 'false'
os.environ['ANONYMIZED_TELEMETRY'] = 'False'


def settings():
    cfg = json.loads((ROOT / 'config/rag.json').read_text('utf-8'))
    if cfg['chunk_size'] < 32 or not 0 <= cfg['chunk_overlap'] < cfg['chunk_size']:
        raise ValueError('청크 크기와 중복 설정을 확인해 주세요.')
    if not 1 <= cfg['top_k'] <= 20 or not cfg['top_k'] <= cfg['fetch_k'] <= 100:
        raise ValueError('검색 수 설정을 확인해 주세요.')
    return cfg


def fingerprint(cfg):
    fields = ('embedding_model', 'embedding_revision', 'embedding_pipeline', 'token_limit', 'chunk_size', 'chunk_overlap', 'mode')
    return hashlib.sha256(json.dumps({k: cfg[k] for k in fields}, sort_keys=True).encode()).hexdigest()[:16]


def runtime():
    # Native HNSW paths must be ASCII on Windows; never put credentials here.
    base = Path(os.environ['LOCALAPPDATA']) / 'FinVOCKorea' if os.name == 'nt' else ROOT / 'runtime/rag'
    base.mkdir(parents=True, exist_ok=True)
    return base


def key_configured():
    return bool((dotenv_values(ROOT / '.env').get('GMS_KEY') or '').strip())
