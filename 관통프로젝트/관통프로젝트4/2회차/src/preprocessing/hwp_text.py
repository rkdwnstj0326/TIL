"""HWP 5의 본문 텍스트 레코드만 읽는다. 포함된 스크립트/매크로를 실행하지 않는다."""
import struct
import zlib
import olefile


def extract_body(path):
    texts=[]
    with olefile.OleFileIO(path) as document:
        header=document.openstream('FileHeader').read()
        if not header.startswith(b'HWP Document File'):raise ValueError('HWP 5 형식 아님')
        flags=struct.unpack_from('<I',header,36)[0]
        if flags & 2:raise ValueError('암호화 문서 지원 안 함')
        for stream in sorted(document.listdir()):
            if stream[0]!='BodyText':continue
            data=document.openstream(stream).read()
            if flags&1:data=zlib.decompress(data,-15)
            if len(data)>10*1024*1024:raise ValueError('본문 크기 상한 초과')
            offset=0
            while offset+4<=len(data):
                record=struct.unpack_from('<I',data,offset)[0];offset+=4
                size=record>>20;tag=record&1023
                if size==4095:
                    size=struct.unpack_from('<I',data,offset)[0];offset+=4
                if offset+size>len(data):raise ValueError('HWP 레코드 크기 오류')
                if tag==67:texts.append(data[offset:offset+size].decode('utf-16le'))
                offset+=size
    return '\n'.join(texts)
