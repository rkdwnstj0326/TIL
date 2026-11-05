"""종료 도구는 실제 서버를 죽이지 않고 거부/확인 분기를 검사한다."""
import json
from types import SimpleNamespace
from scripts import stop_app


def record():return {'app':str(stop_app.APP),'pid':54321,'port':8540}


def test_refuse_other_app_before_any_process_call(monkeypatch):
    def blocked(*a,**k):raise AssertionError('다른 앱에 프로세스 도구 호출 금지')
    monkeypatch.setattr(stop_app.subprocess,'run',blocked)
    r=record();r['app']='C:/other/app.py'
    assert stop_app.run(r)['status']=='refused'
    r=record();r['port']=80
    assert stop_app.run(r)['status']=='refused'


def test_check_only_does_not_issue_stop_branch(monkeypatch):
    calls=[]
    def fake_run(args,**kwargs):
        import base64
        script=base64.b64decode(args[-1]).decode('utf-16le');calls.append(script)
        return SimpleNamespace(returncode=0,stdout=json.dumps({'status':'managed_running','message':'시험 응답'}))
    monkeypatch.setattr(stop_app.subprocess,'run',fake_run)
    result=stop_app.run(record(),check_only=True)
    assert result['status']=='managed_running'
    assert '$checkOnly=$true' in calls[0] and '$p.CommandLine -notmatch $pattern' in calls[0]


def test_changed_process_is_refused(monkeypatch):
    monkeypatch.setattr(stop_app.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,
        stdout=json.dumps({'status':'refused','message':'다른 실제 프로세스'})))
    assert stop_app.run(record())['status']=='refused'
