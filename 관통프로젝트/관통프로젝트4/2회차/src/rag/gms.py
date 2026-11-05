"""Only the current project's .env is read. No secrets or raw HTTP errors logged."""
import json
from time import perf_counter
import requests
from dotenv import dotenv_values
from src.collection.client import ROOT
from .prompts import POLICY


class GMSError(RuntimeError):
    pass


class GMS:
    def __init__(self, cfg):
        self.key = (dotenv_values(ROOT / '.env').get('GMS_KEY') or '').strip()
        if not self.key:
            raise GMSError('GMS_KEY가 없습니다. 이 프로젝트의 .env에 입력해 주세요.')
        # Match the actual distributed GMS route. Do not send credentials elsewhere.
        if cfg['gms_base_url'] != 'https://gms.ssafy.io/gmsapi/api.openai.com/v1/':
            raise GMSError('승인된 GMS 주소를 확인해 주세요.')
        self.cfg, self.calls, self.timings = cfg, 0, []

    def json(self, prompt, data):
        start = perf_counter()
        try:
            self.calls += 1
            response = requests.post(self.cfg['gms_base_url'] + 'chat/completions',
                headers={'Authorization': 'Bearer ' + self.key},
                json={'model': self.cfg['gms_model'], 'messages': [
                    {'role': 'system', 'content': POLICY + '\n' + prompt},
                    {'role': 'user', 'content': json.dumps(data, ensure_ascii=False)}],
                    'response_format': {'type': 'json_object'}, 'max_completion_tokens': 1800},
                timeout=(10, 65), allow_redirects=False)
            if response.status_code != 200:
                raise GMSError(f'GMS 요청 실패(HTTP {response.status_code}). 키·사용량·서버 상태를 확인해 주세요.')
            content = response.json()['choices'][0]['message']['content']
            value = json.loads(content)
            if type(value) is not dict:
                raise ValueError('object required')
            return value
        except requests.RequestException:
            raise GMSError('GMS에 연결하지 못했습니다. 네트워크를 확인한 뒤 다시 시도해 주세요.') from None
        except (ValueError, KeyError, IndexError, TypeError):
            raise GMSError('GMS 응답 형식이 올바르지 않아 결과를 표시하지 않았습니다.') from None
        finally:
            self.timings.append(round(perf_counter() - start, 3))
