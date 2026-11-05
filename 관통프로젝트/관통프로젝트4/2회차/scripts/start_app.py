"""본 프로젝트 서버만 재사용하고, 사용 중인 포트/다른 프로세스는 건드리지 않는다."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import webbrowser
import requests

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'app.py'
RUNTIME=ROOT/'runtime'
RECEIPT=RUNTIME/'server.json'
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)


def healthy(port):
    try:
        response=requests.get(f'http://127.0.0.1:{port}/_stcore/health',timeout=2)
        return response.status_code==200 and response.text.strip()=='ok'
    except requests.RequestException:
        return False


def owned(record):
    if os.name!='nt' or record.get('app')!=str(APP):
        return False
    try:
        pid=int(record['pid']);port=int(record['port'])
        if pid<=0 or not 8540<=port<=8560:
            return False
        # 조회만 한다. 기존 서버를 종료하거나 점유 포트를 해제하지 않는다.
        command=subprocess.check_output(['powershell','-NoProfile','-Command',
            "[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new(); "
            f"Get-CimInstance Win32_Process -Filter 'ProcessId = {pid}' | Select-Object -ExpandProperty CommandLine"],
            timeout=8,creationflags=FLAGS).decode('utf-8-sig',errors='replace')
        return str(APP).casefold() in command.casefold() and healthy(port)
    except (ValueError,KeyError,subprocess.SubprocessError):
        return False


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--no-browser',action='store_true')
    args=parser.parse_args()
    RUNTIME.mkdir(exist_ok=True)
    if RECEIPT.exists():
        try:
            record=json.loads(RECEIPT.read_text('utf-8'))
            if owned(record):
                url=f"http://127.0.0.1:{record['port']}/"
                print(url)
                if not args.no_browser:webbrowser.open(url)
                return
        except (OSError,json.JSONDecodeError):
            pass
    for port in range(8540,8561):
        with socket.socket() as sock:
            try:sock.bind(('127.0.0.1',port))
            except OSError:continue
        log=RUNTIME/f'streamlit-{port}.log'
        with log.open('ab') as stream:
            proc=subprocess.Popen([sys.executable,'-m','streamlit','run',str(APP),
                '--server.address=127.0.0.1',f'--server.port={port}','--server.headless=true'],
                cwd=ROOT,stdin=subprocess.DEVNULL,stdout=stream,stderr=stream,creationflags=FLAGS)
        record={'app':str(APP),'pid':proc.pid,'port':port,'url':f'http://127.0.0.1:{port}/'}
        RECEIPT.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        for _ in range(80):
            if proc.poll() is not None:break
            if healthy(port):
                print(record['url'])
                if not args.no_browser:webbrowser.open(record['url'])
                return
            time.sleep(.4)
        if proc.poll() is None:
            raise RuntimeError('서버 시작 대기 시간을 넘었습니다. runtime의 로컬 로그를 확인하세요.')
    raise RuntimeError('사용 가능한 포트를 찾지 못했습니다. 기존 프로세스는 종료하지 않았습니다.')


if __name__=='__main__':
    main()
