"""ONNX semantic embeddings; split at tokenizer offsets to preserve Korean tails."""
from threading import RLock
import numpy as np
from fastembed import TextEmbedding
from tokenizers import Tokenizer
from .config import runtime


class LocalEmbedding:
    def __init__(self, cfg):
        self.cfg, self.lock = cfg, RLock()
        supported = {m['model']: m for m in TextEmbedding.list_supported_models()}
        if cfg['embedding_model'] not in supported:
            raise ValueError('현재 FastEmbed에서 지원하지 않는 모델입니다.')
        self.model = TextEmbedding(cfg['embedding_model'], cache_dir=str(runtime() / 'model_cache'),
                                   threads=4, revision=cfg['embedding_revision'])
        self.tokenizer = Tokenizer.from_str(self.model.model.tokenizer.to_str())
        self.tokenizer.no_truncation()
        self.tokenizer.no_padding()
        actual = self.model.model.tokenizer.truncation
        if not actual or actual['max_length'] != cfg['token_limit']:
            raise ValueError('실제 모델의 토큰 상한과 설정이 다릅니다.')
        self.limit = cfg['token_limit']
        self.budget = self.limit - self.tokenizer.num_special_tokens_to_add(False) - 4

    def token_count(self, text):
        return len(self.tokenizer.encode(text).ids)

    def windows(self, text, chars=None, overlap=None):
        chars = chars or self.cfg['chunk_size']
        overlap = self.cfg['chunk_overlap'] if overlap is None else overlap
        if chars < 32 or not 0 <= overlap < chars:
            raise ValueError('잘못된 청크 설정')
        result, start = [], 0
        while start < len(text):
            end = min(len(text), start + chars)
            encoded = self.tokenizer.encode(text[start:end], add_special_tokens=False)
            if len(encoded.ids) > self.budget:
                end = start + encoded.offsets[self.budget - 1][1]
            while self.token_count(text[start:end]) > self.limit:
                end -= 1
            if end <= start:
                raise ValueError('토큰 창 생성 실패')
            result.append((start, end, text[start:end]))
            if end == len(text):
                break
            start = max(start + 1, end - min(overlap, (end - start) // 4))
        return result

    def vectors(self, texts):
        with self.lock:
            return np.asarray(list(self.model.embed(texts)), dtype=np.float32)

    def document_vector(self, text):
        windows = self.windows(text)
        if not windows:
            raise ValueError('빈 문서는 임베딩하지 않습니다.')
        vec = self.vectors([w[2] for w in windows]).mean(axis=0)
        return (vec / max(float(np.linalg.norm(vec)), 1e-12)).tolist()
