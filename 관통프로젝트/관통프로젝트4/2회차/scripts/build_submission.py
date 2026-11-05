"""Build the official submission ZIP directly from the canonical project folder."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime
from urllib.parse import unquote, urlparse
import zipfile
from dotenv import dotenv_values
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from refresh_rag_docs import refresh
BLOCKED = {'.venv','venv','env','.conda','.git','__pycache__','.pytest_cache','.pytest_tmp','node_modules','site-packages','runtime','model_cache','dist','chroma','chroma_db','raw','private','processed','metadata'}
ZIP_NAME = 'AI_코어프로젝트2_FinVOC금융민원분석AI_서울_1반_강준서.zip'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_links(root):
    count = 0
    for path in root.rglob('*.md'):
        if any(part in BLOCKED for part in path.relative_to(root).parts):
            continue
        for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', path.read_text('utf-8-sig')):
            ref = match.group(1).strip().strip('<>')
            if urlparse(ref).scheme or ref.startswith('#'):
                continue
            ref = unquote(ref.split('#', 1)[0])
            if ref and not (path.parent / ref).is_file() and not (path.parent / ref).is_dir():
                raise ValueError('Broken document link: ' + str(path.relative_to(root)))
            count += 1
    return count


def selected_files():
    names = ['.gitignore','.env.example','.streamlit/config.toml','app.py','README.md',
        'SUBMISSION_STATUS.json','requirements.txt','requirements-phase0.txt','requirements-lock.txt',
        'pytest.ini','setup.ps1','prepare_data.ps1','FinVOC 실행.cmd','FinVOC 종료.cmd','제출용 압축.cmd']
    files = [ROOT / name for name in names]
    for folder in ['src','scripts','tests','docs','config','submission_human']:
        files += [p for p in (ROOT / folder).rglob('*') if p.is_file() and not any(x.casefold() in BLOCKED for x in p.relative_to(ROOT).parts)]
    reports = ['phase0_audit.json','PHASE0_REPORT.md','pdf_inventory.json','case_quality.json',
        'statistics_validation.json','cross_source_validation.json','validation_summary.json','design_validation.json',
        'insurer_expansion.json','INSURER_EXPANSION.md','insurer_ui_validation.json','submission_profile.json',
        'submission_pytest_20261023.xml','rag_index.json','gms_connection.json','rag_local_validation.json',
        'rag_comparison_summary.json','rag_browser_validation.json','start_stop_validation.json','submission_replay.json',
        'insurer_history.json','history_browser_validation.json','history_rag_validation.json']
    files += [ROOT / 'reports' / name for name in reports if (ROOT / 'reports' / name).is_file()]
    files += [p for p in (ROOT / 'reports/evidence/insurers').glob('*.png') if p.name in {'samsung-overview.png','kyobo-overview.png','validation.png','unconfirmed-denominator.png'}]
    files += [p for p in (ROOT / 'reports/evidence/rag').glob('*.png') if p.name in {'rag-answer.png','rag-discovery.png'}]
    files += [p for p in (ROOT / 'reports/evidence/history').glob('*.png') if p.name in {'past-quarter.png','standard-boundary.png'}]
    return sorted(set(files))


def main():
    status = refresh()
    file_list = selected_files()
    key = (dotenv_values(ROOT / '.env').get('GMS_KEY') or '').strip()
    for path in file_list:
        if not path.is_file():
            raise FileNotFoundError(path.name)
        relative = path.relative_to(ROOT)
        if any(p.casefold() in BLOCKED for p in relative.parts) or (path.name.startswith('.env') and path.name != '.env.example'):
            raise ValueError('Excluded path selected')
        if path.suffix == '.png':
            continue
        text = path.read_text('utf-8-sig')
        if key and key in text:
            raise ValueError('Secret found in selected file: ' + str(relative))
        if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text):
            raise ValueError('Contact-like value found: ' + str(relative))
    link_count = check_links(ROOT)
    (ROOT / 'dist').mkdir(exist_ok=True)
    archive_path = ROOT / 'dist' / ZIP_NAME
    if archive_path.exists():
        backup = ROOT / 'runtime/package_history'
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive_path, backup / (datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.zip'))
    manifest = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in file_list}
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in file_list:
            archive.write(p, p.relative_to(ROOT).as_posix())
        archive.writestr('MANIFEST.sha256.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        for name, expected in manifest.items():
            assert digest(archive.read(name)) == expected
        assert not any(any(part.casefold() in BLOCKED for part in Path(name).parts) or Path(name).name == 'pyvenv.cfg' for name in archive.namelist())
        assert not any(Path(name).name == '.env' for name in archive.namelist())
        assert not key or not any(key.encode() in archive.read(name) for name in archive.namelist())
    report = {'archive': str(archive_path), 'sha256': digest(archive_path.read_bytes()), 'files': len(manifest),
        'crc_passed': True, 'member_hashes_passed': True, 'virtual_environment_members': 0,
        'actual_env_members': 0, 'actual_key_occurrences': 0, 'markdown_links_checked': link_count,
        'ready_for_final_submission': status['ready_for_final_submission'], 'uploaded': False,
        'data_preparation_required': True}
    (ROOT / 'dist/package_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT / 'reports/submission_package_latest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
