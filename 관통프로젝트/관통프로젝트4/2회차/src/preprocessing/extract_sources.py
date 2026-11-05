"""PDF 전체 페이지를 읽어 페이지 번호가 보존된 연구용 텍스트를 만든다."""
import json
from pathlib import Path
import pymupdf
from src.collection.client import ROOT


def main():
    catalog = json.loads((ROOT / 'data/metadata/source_catalog.json').read_text('utf-8'))
    out = ROOT / 'data/private/extracted'
    out.mkdir(parents=True, exist_ok=True)
    inventory = []
    for source in catalog:
        path = ROOT / source['document']['local_path']
        if path.suffix != '.pdf':
            continue
        with pymupdf.open(path) as document:
            pages = [{'page': i + 1, 'text': page.get_text(sort=True)}
                     for i, page in enumerate(document)]
        (out / (source['source_id'] + '.json')).write_text(
            json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
        (out / (source['source_id'] + '.txt')).write_text(
            '\n\n'.join(f"--- PDF PAGE {p['page']} ---\n{p['text']}" for p in pages), encoding='utf-8')
        inventory.append({'source_id': source['source_id'], 'pages': len(pages),
                          'characters': sum(len(p['text']) for p in pages),
                          'empty_pages': [p['page'] for p in pages if not p['text'].strip()]})
    report = ROOT / 'reports'
    report.mkdir(exist_ok=True)
    (report / 'pdf_inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(inventory, ensure_ascii=False))


if __name__ == '__main__':
    main()
