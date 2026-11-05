import hashlib
import json
import chromadb
import numpy as np
from chromadb.config import Settings
from .config import runtime, fingerprint


class Store:
    def __init__(self, cfg, embed, path=None):
        self.cfg, self.embed = cfg, embed
        self.signature = fingerprint(cfg)
        self.client = chromadb.PersistentClient(path=str(path or runtime() / 'chroma'), settings=Settings(anonymized_telemetry=False))
        self.meta = self.client.get_or_create_collection('items_' + self.signature, metadata={'hnsw:space': 'cosine'}, embedding_function=None)
        self.docs = self.client.get_or_create_collection('docs_' + self.signature, metadata={'hnsw:space': 'cosine'}, embedding_function=None)

    def index_items(self, items):
        for item in items:
            digest = hashlib.sha256(item['text'].encode()).hexdigest()
            old = self.meta.get(ids=[item['item_id']], include=['metadatas'])
            if old['ids'] and old['metadatas'][0].get('body_hash') == digest:
                continue
            self.meta.upsert(ids=[item['item_id']], documents=[item['text']],
                embeddings=[self.embed.document_vector(item['text'])],
                metadatas=[{k: item[k] for k in ('item_id', 'title', 'url', 'source_type', 'collected_at', 'company', 'period')} | {'body_hash': digest}])

    def doc_ids(self, item_id, doc_id):
        return self.docs.get(where={'$and': [{'item_id': item_id}, {'doc_id': doc_id}]})['ids']

    def index_doc(self, item_id, doc):
        digest = hashlib.sha256(doc['text'].encode()).hexdigest()
        old = self.docs.get(where={'$and': [{'item_id': item_id}, {'doc_id': doc['doc_id']}]}, include=['metadatas'])
        if old['ids'] and all(m.get('body_hash') == digest for m in old['metadatas']):
            return old['ids']
        pieces = []
        for paragraph in doc['paragraphs']:
            if len(paragraph['text'].strip()) < 35:
                continue
            for start, end, text in self.embed.windows(paragraph['text']):
                pieces.append((paragraph['paragraph'], start, end, text))
        if not pieces:
            raise ValueError('색인할 실제 본문이 없습니다.')
        ids = [f'{item_id}:{doc["doc_id"]}:{i}' for i in range(len(pieces))]
        metadata = [{k: str(doc.get(k, '')) for k in ('doc_id', 'title', 'url', 'source_type', 'collected_at', 'event_company_name')} |
                    {'item_id': item_id, 'paragraph': p, 'start': start, 'end': end, 'body_hash': digest, 'is_self': bool(doc['is_self'])}
                    for p, start, end, _ in pieces]
        for start in range(0, len(ids), 48):
            self.docs.upsert(ids=ids[start:start + 48], documents=[p[3] for p in pieces[start:start + 48]],
                embeddings=self.embed.vectors([p[3] for p in pieces[start:start + 48]]).tolist(), metadatas=metadata[start:start + 48])
        stale = set(old['ids']) - set(ids)
        if stale:
            self.docs.delete(ids=list(stale))
        if set(self.doc_ids(item_id, doc['doc_id'])) != set(ids):
            raise RuntimeError('DB 색인 완료를 확인하지 못했습니다.')
        receipt = runtime() / ('indexed_' + self.signature + '.json')
        history = json.loads(receipt.read_text('utf-8')) if receipt.exists() else {}
        history[item_id + ':' + doc['doc_id']] = {'body_hash': digest, 'chunks': len(ids), 'verified_in_db': True}
        receipt.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')
        return ids

    def retrieve(self, item_id, question, allowed_doc_ids=None, method=None, top_k=None):
        selected = self.meta.get(ids=[item_id], include=['documents', 'metadatas'])
        if not selected['ids']:
            raise ValueError('선택 항목 메타데이터 색인이 없습니다.')
        evidence = [selected['metadatas'][0] | {'text': selected['documents'][0], 'chunk_id': item_id, 'doc_id': item_id, 'is_self': True}]
        k = top_k or self.cfg['top_k']
        where = {'item_id': item_id} if allowed_doc_ids is None else {'$and': [{'item_id': item_id}, {'doc_id': {'$in': allowed_doc_ids}}]}
        count = len(self.docs.get(where=where)['ids']) if allowed_doc_ids != [] else 0
        if not count or k == 1:
            return evidence
        q = np.asarray(self.embed.document_vector(question))
        hits = self.docs.query(query_embeddings=[q.tolist()], where=where, n_results=min(count, self.cfg['fetch_k']), include=['documents', 'metadatas', 'embeddings'])
        vectors = np.asarray(hits['embeddings'][0])
        vectors /= np.maximum(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-12)
        pool, chosen, seen = list(range(len(vectors))), [], set()
        # Ensure a passage from the selected item's own disclosure is retained.
        self_hits = [j for j in pool if hits['metadatas'][0][j].get('is_self')]
        if self_hits:
            chosen.append(max(self_hits, key=lambda j: float(vectors[j] @ q)))
            pool.remove(chosen[0])
        while pool and len(chosen) < k - 1:
            def score(j):
                rel = float(vectors[j] @ q)
                if (method or self.cfg['search_method']) != 'mmr' or not chosen:
                    return rel
                return self.cfg['mmr_lambda'] * rel - (1 - self.cfg['mmr_lambda']) * max(float(vectors[j] @ vectors[c]) for c in chosen)
            j = max(pool, key=score)
            pool.remove(j)
            text = hits['documents'][0][j]
            if text in seen:
                continue
            seen.add(text)
            chosen.append(j)
        for j in chosen:
            evidence.append(hits['metadatas'][0][j] | {'text': hits['documents'][0][j], 'chunk_id': hits['ids'][0][j]})
        return evidence

    def discover(self, query, allowed_ids, k=8):
        if not allowed_ids:
            return []
        return self.meta.query(query_embeddings=[self.embed.document_vector(query)], where={'item_id': {'$in': allowed_ids}}, n_results=min(k, len(allowed_ids)))['ids'][0]
