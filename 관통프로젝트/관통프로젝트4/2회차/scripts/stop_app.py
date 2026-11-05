"""사용자가 실행한 FinVOC만 종료한다. PID·앱 경로·실제 명령을 확인하고 다른 프로세스는 거부한다."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'app.py'
RECEIPT=ROOT/'runtime/server.json'


def validate_record(record):
    return (isinstance(record,dict) and record.get('app')==str(APP)
            and type(record.get('pid')) is int and record['pid']>0
            and type(record.get('port')) is int and 8540<=record['port']<=8560)


def run(record,check_only=False):
    if not validate_record(record):return {'status':'refused','message':'본 프로젝트의 실행 기록이 아니므로 종료하지 않습니다.'}
    if os.name!='nt':return {'status':'unsupported','message':'이 종료 도구는 Windows용입니다.'}
    # PowerShell의 같은 실행 안에서 실제 명령·생성 시각을 확인한다. 포트로 PID를 찾아 종료하지 않는다.
    app=str(APP).replace("'","''")
    script=fr'''
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new()
$expectedPid={record['pid']}
$expectedApp='{app}'
$checkOnly={'$true' if check_only else '$false'}
$p=Get-CimInstance Win32_Process -Filter "ProcessId = $expectedPid"
if ($null -eq $p) {{ @{{status='not_running';message='기록된 서버는 이미 종료되었습니다.'}} | ConvertTo-Json -Compress;exit }}
$escaped=[regex]::Escape($expectedApp)
$pattern='(?i)(?:^|\s)-m\s+streamlit\s+run\s+(?:"'+$escaped+'"|'+$escaped+')(?=\s|$)'
if ($p.CommandLine -notmatch $pattern) {{ @{{status='refused';message='PID의 실제 앱이 달라 종료하지 않습니다.'}} | ConvertTo-Json -Compress;exit }}
if ($checkOnly) {{ @{{status='managed_running';message='이 FinVOC 서버가 실행 중입니다.'}} | ConvertTo-Json -Compress;exit }}
$process=Get-Process -Id $expectedPid -ErrorAction Stop
$again=Get-CimInstance Win32_Process -Filter "ProcessId = $expectedPid"
if ($null -eq $again -or $again.CreationDate -ne $p.CreationDate -or $again.CommandLine -notmatch $pattern) {{ throw '프로세스가 변경되어 중단합니다.' }}
Stop-Process -InputObject $process -ErrorAction Stop
@{{status='stopped';message='이 FinVOC 서버를 종료했습니다.'}} | ConvertTo-Json -Compress
'''
    encoded=base64.b64encode(script.encode('utf-16le')).decode('ascii')
    completed=subprocess.run(['powershell','-NoProfile','-EncodedCommand',encoded],capture_output=True,
        encoding='utf-8-sig',errors='replace',timeout=15,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if completed.returncode:raise RuntimeError('종료 확인 중 오류가 발생했습니다. 다른 프로세스는 추가 종료하지 않습니다.')
    return json.loads(completed.stdout.strip())


def main():
    parser=argparse.ArgumentParser(description='이 프로젝트의 FinVOC 서버만 종료')
    parser.add_argument('--check-only',action='store_true',help='서버 소유 여부만 확인하며 종료하지 않음')
    args=parser.parse_args()
    if not RECEIPT.exists():
        print('이 폴더에서 실행한 서버 기록이 없습니다. 다른 서버는 종료하지 않습니다.');return
    try:
        result=run(json.loads(RECEIPT.read_text('utf-8')),args.check_only)
        print(result['message'])
        if result['status'] in {'refused','unsupported'}:sys.exit(1)
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError):
        print('서버 기록과 실제 프로세스를 확인할 수 없어 종료하지 않았습니다.');sys.exit(1)


if __name__=='__main__':main()
