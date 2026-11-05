"""Explicit opt-in GMS connection check. Never invoked by automatic tests."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.rag.config import settings, key_configured
from src.rag.gms import GMS, GMSError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    if not args.run:
        print('미실행: --run 옵션으로 실제 GMS 연결을 검사합니다.')
        return
    report = {'key_configured': key_configured(), 'actual_call': True}
    try:
        client = GMS(settings())
        value = client.json('연결 검사입니다. 다른 설명 없이 JSON {"connected":true}를 출력하세요.', {})
        report |= {'connected': value.get('connected') is True, 'calls': client.calls, 'seconds': client.timings, 'model': client.cfg['gms_model']}
    except GMSError as error:
        report |= {'connected': False, 'safe_error': str(error)}
    target = Path(__file__).resolve().parents[1] / 'reports/gms_connection.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
