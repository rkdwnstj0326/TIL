"""금감원 공개 보험 사례 4개 목록 페이지만 제한 수집. 본문은 로컬 연구용."""
import json
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
from .client import Client, ROOT


def soup(path):
    # 공식 페이지의 UTF-8을 명시한다. 자동 인코딩 추정의 한글 손상을 방지한다.
    return BeautifulSoup(path.read_bytes(), 'html.parser', from_encoding='utf-8')


def collect(page_numbers=(1, 2, 3, 4)):
    if len(page_numbers) > 8 or any(not 1 <= p <= 16 for p in page_numbers):
        raise ValueError('한 번에 목록 8페이지 이하, 확인된 1~16페이지 범위만 허용')
    c = Client()
    target = ROOT / 'data/metadata/case_catalog.json'
    records = json.loads(target.read_text('utf-8')) if target.exists() else []
    seen = {r['case_id'].removeprefix('fss_case_') for r in records}
    for page in page_numbers:
        url = ('https://www.fss.or.kr/fss/job/fncCnflCase/list.do?'
               + urlencode({'menuNo': '201195', 'rgnlCode': 'B', 'pageIndex': page}))
        path, _ = c.fetch(url)
        for row in soup(path).select('#container tbody tr'):
            link = next((a for a in row.select('a[href]') if 'view.do?caseSlno=' in a['href']), None)
            if not link:
                continue
            original = urljoin(url, link['href'])
            number = parse_qs(urlparse(original).query)['caseSlno'][0]
            if number in seen:
                continue
            seen.add(number)
            # 목록 페이지 번호는 문서 식별자가 아니다. 고정 식별자 URL로 캐시한다.
            view = ('https://www.fss.or.kr/fss/job/fncCnflCase/view.do?'
                    + urlencode({'caseSlno': number, 'menuNo': '201195'}))
            body_path, receipt = c.fetch(view)
            records.append({'case_id': 'fss_case_' + number, 'title': link.get_text(' ', strip=True),
                            'source_url': view, 'list_page': url,
                            'list_cells': [td.get_text(' ', strip=True) for td in row.select('td')],
                            'publisher': '금융감독원', 'source_type': '공개 분쟁조정사례',
                            'receipt': receipt})
        print(f'목록 {page} 완료: 누적 {len(records)}개 문서', flush=True)
    target.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = {'documents': len(records), 'http_calls': c.calls, 'cache_hits': c.hits}
    (ROOT / 'reports/case_collection.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    collect()
