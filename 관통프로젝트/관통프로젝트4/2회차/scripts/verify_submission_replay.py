"""Extract current ZIP safely and smoke-test it without external HTTP/GMS."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import zipfile
ROOT = Path(__file__).resolve().parents[1]


def main():
    archive = ROOT / 'dist/AI_코어프로젝트2_FinVOC금융민원분석AI_서울_1반_강준서.zip'
    destination = ROOT / 'runtime' / ('replay_' + uuid.uuid4().hex[:12])
    destination.mkdir(parents=True)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist():
            target = (destination / name).resolve()
            if not target.is_relative_to(destination.resolve()) or '\\' in name or ':' in name:
                raise ValueError('Unsafe archive member')
        z.extractall(destination)
    # Actual local snapshots are restored only into this excluded verification directory.
    restored = ['data/processed/sector_stats.json','data/processed/insurer_stats.json',
        'data/processed/insurer_stats_all.json','data/private/cases.json','data/metadata/insurer_registry.json']
    restored += ['data/processed/insurer_stats_history.json','data/metadata/insurer_registry_history.json']
    harness = destination / 'smoke_replay.py'
    harness.write_text('''import json
from pathlib import Path
import requests
from streamlit.testing.v1 import AppTest
from src.rag.gms import GMS
root=Path(__file__).resolve().parent
def blocked(*args,**kwargs):
    raise AssertionError('External HTTP/GMS prohibited during replay')
requests.sessions.Session.request=blocked
GMS.json=blocked
app=AppTest.from_file(str(root/'app.py'),default_timeout=30).run()
assert not app.exception
if not (root/'data/private/cases.json').exists():
    assert any('분석 자료' in title.value for title in app.title)
    print('missing-data-guidance-ok')
else:
    assert app.metric[0].value=='75건'
    next(w for w in app.button_group if w.key=='workspace').set_value('근거 기반 AI').run()
    assert not app.exception
    assert any('생성 답변은 실행하지 않습니다' in value.value for value in app.info)
    print('restored-data-ui-and-key-missing-guidance-ok')
''', encoding='utf-8')
    results = []
    results.append(subprocess.check_output([sys.executable, str(harness)], cwd=destination, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace').strip())
    for name in restored:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    results.append(subprocess.check_output([sys.executable, str(harness)], cwd=destination, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace').strip())
    report = {'archive': str(archive), 'safe_paths_checked': True, 'crc_passed': True, 'actual_gms_calls': 0,
        'external_http_calls': 0, 'data_snapshots_restored_for_test_only': len(restored),
        'new_computer_remote_fetch_verified': False, 'checks': results, 'passed': True}
    (ROOT/'reports/submission_replay.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
