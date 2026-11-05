"""공식 출처 전용 캐시 수집기. robots 금지·403을 우회하지 않는다."""
import hashlib,json,time
from time import sleep
from pathlib import Path
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse,urljoin
from urllib.robotparser import RobotFileParser
import requests

ROOT=Path(__file__).resolve().parents[2]
ALLOWED={'www.fss.or.kr','eiec.kdi.re.kr','www.hanainsure.co.kr','www.shinhanez.co.kr',
         'www.kbinsure.co.kr','www.kyobo.com','www.nhlife.co.kr','consumer.knia.or.kr'}
AGENT='FinVOCKoreaResearch/0.1'

def retry_delay(value,attempt,now=None):
    """Retry-After의 초/HTTP-date 두 표현을 처리한다. 긴 대기는 자동 재요청하지 않는다."""
    now=now or datetime.now(timezone.utc)
    if value.isdecimal():delay=float(value)
    elif value:
        try:delay=max(0,(parsedate_to_datetime(value)-now).total_seconds())
        except (ValueError,TypeError,OverflowError):delay=2**attempt
    else:delay=2**attempt
    if delay>60:raise RuntimeError('긴 서버 대기 요청으로 중단')
    return delay

class Client:
    def __init__(self,root=ROOT):
        self.root=Path(root);self.raw=self.root/'data/raw';self.meta=self.root/'data/metadata'
        self.raw.mkdir(parents=True,exist_ok=True);self.meta.mkdir(parents=True,exist_ok=True)
        self.session=requests.Session();self.session.headers['User-Agent']=AGENT
        self.last={};self.policies={};self.calls=0;self.hits=0

    def _request(self,url):
        host=urlparse(url).hostname
        if host not in ALLOWED:raise ValueError('승인하지 않은 출처 호스트')
        for attempt in range(3):
            sleep(max(0,1-(time.monotonic()-self.last.get(host,0))))
            self.last[host]=time.monotonic();self.calls+=1
            target=url
            for redirect in range(5):
                # 외부 호스트에 요청을 보낸 뒤 검사하지 않도록 자동 리다이렉트를 끈다.
                r=self.session.get(target,timeout=(10,35),allow_redirects=False)
                if r.status_code not in {301,302,303,307,308}:break
                target=urljoin(target,r.headers.get('Location',''))
                if urlparse(target).hostname!=host or urlparse(target).scheme!='https':
                    raise ValueError('호스트 밖/비 HTTPS 리다이렉트 확인 필요')
            else:raise ValueError('리다이렉트 상한 초과')
            if r.status_code in {429,500,502,503,504} and attempt<2:
                retry=r.headers.get('Retry-After','')
                sleep(retry_delay(retry,attempt));continue
            r.raise_for_status()
            if len(r.content)>50*1024*1024:raise ValueError('파일 크기 상한50MiB')
            return r
        raise RuntimeError('공개 자료 요청 실패')

    def policy(self,host):
        if host in self.policies:return self.policies[host]
        path=self.meta/('robots_'+host+'.json')
        if path.exists():record=json.loads(path.read_text('utf-8'))
        else:
            r=self._request('https://'+host+'/robots.txt')
            content_type=r.headers.get('Content-Type','')
            if host=='consumer.knia.or.kr' and r.url=='https://consumer.knia.or.kr/error/error_pm.jpg' and content_type.startswith('image/'):
                # 이 공개 포털은 존재하지 않는 robots 경로를 이미지로 연결한다.
                # 금지 규칙으로 해석하거나 이미지 바이트를 robots 텍스트로 파싱하지 않는다.
                policy_text=''
                policy_state='unavailable_nontext_redirect; public pages only, low-volume cached requests'
            else:
                if not content_type.startswith('text/plain'):
                    raise ValueError('robots 응답이 텍스트 정책이 아니므로 출처별 확인 필요')
                try:policy_text=r.content.decode('utf-8-sig')
                except UnicodeDecodeError:policy_text=r.text
                policy_state='published_text'
            record={'url':r.url,'status':r.status_code,'text':policy_text,'policy_state':policy_state,
                    'content_type':content_type,'checked_at':datetime.now(timezone.utc).isoformat()}
            path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        rp=RobotFileParser();rp.parse(record['text'].splitlines());self.policies[host]=rp;return rp

    def fetch(self,url,kind='html'):
        host=urlparse(url).hostname
        if host not in ALLOWED:raise ValueError('출처 허용 목록 밖')
        if not self.policy(host).can_fetch(AGENT,url):raise PermissionError('robots에서 자동 수집을 허용하지 않습니다.')
        key=hashlib.sha256(url.encode()).hexdigest();receipt=self.meta/(key+'.json')
        if receipt.exists():
            record=json.loads(receipt.read_text('utf-8'));path=self.root/record['local_path']
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']:
                self.hits+=1;return path,record
            raise ValueError('기존 출처 캐시 무결성 확인 필요')
        r=self._request(url)
        if kind=='pdf' and not r.content.startswith(b'%PDF-'):raise ValueError('PDF가 아닌 응답')
        path=self.raw/(key+'.'+kind);path.write_bytes(r.content)
        record={'url':url,'final_url':r.url,'local_path':path.relative_to(self.root).as_posix(),
            'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content),
            'retrieved_at':datetime.now(timezone.utc).isoformat(),'content_type':r.headers.get('Content-Type'),
            'reuse_permission':'별도 출처 정책 및 자료별 이용조건 검토 기록 참조'}
        receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        return path,record
