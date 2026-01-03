"""
HTTP 요청 파싱 모듈
클라이언트로부터 받은 raw HTTP 요청 데이터를 파싱하여 딕셔너리로 변환합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import CRLF


class HTTPParser:
    """HTTP 요청을 파싱하는 클래스"""
    
    def __init__(self):
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = None
    
    def parse_request(self, raw_data):
        """
        raw HTTP 요청 데이터를 파싱합니다.
        
        Args:
            raw_data (str): 클라이언트로부터 받은 HTTP 요청 문자열
            
        Returns:
            dict: 파싱된 요청 정보 {'method', 'path', 'version', 'headers', 'body'}
        """
        try:
            # CRLF로 줄 분리
            lines = raw_data.split(CRLF)
            
            # 1. 요청 라인 파싱 (첫 번째 줄)
            # 예: "GET /index.html HTTP/1.1"
            request_line = lines[0]
            parts = request_line.split(' ')
            
            if len(parts) != 3:
                raise ValueError("Invalid request line")
            
            self.method = parts[0]
            self.path = parts[1]
            self.version = parts[2]
            
            # 2. 헤더 파싱 (두 번째 줄부터 빈 줄 전까지)
            i = 1
            while i < len(lines) and lines[i] != '':
                line = lines[i]
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.headers[key.strip()] = value.strip()
                i += 1
            
            # 3. 바디 파싱 (빈 줄 이후)
            # 빈 줄 다음부터가 바디
            if i + 1 < len(lines):
                self.body = CRLF.join(lines[i + 1:])
            
            return {
                'method': self.method,
                'path': self.path,
                'version': self.version,
                'headers': self.headers,
                'body': self.body
            }
        
        except Exception as e:
            print(f"파싱 에러: {e}")
            return None
    
    def get_method(self):
        """HTTP 메소드 반환"""
        return self.method
    
    def get_path(self):
        """요청 경로 반환"""
        return self.path
    
    def get_headers(self):
        """헤더 딕셔너리 반환"""
        return self.headers
    
    def get_body(self):
        """바디 반환"""
        return self.body
