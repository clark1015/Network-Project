"""
HTTP 요청 생성 모듈
각 HTTP 메소드에 대한 요청 문자열을 생성합니다.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import HTTP_VERSION, CRLF, DEFAULT_HOST, DEFAULT_PORT


class HTTPRequest:
    """HTTP 요청을 생성하는 클래스"""
    
    def __init__(self, method, path, headers=None, body=None):
        """
        Args:
            method (str): HTTP 메소드 (GET, HEAD, POST, PUT)
            path (str): 요청 경로
            headers (dict): 요청 헤더
            body (str): 요청 바디
        """
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body or ''
        
        # 기본 헤더 설정
        if 'Host' not in self.headers:
            self.headers['Host'] = f'{DEFAULT_HOST}:{DEFAULT_PORT}'
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = 'Python-Socket-Client/1.0'
    
    def add_header(self, key, value):
        """헤더 추가"""
        self.headers[key] = value
    
    def to_string(self):
        """
        HTTP 요청 객체를 문자열로 변환
        (소켓은 바이트만 전송 가능하므로 문자열로 변환 필요)
        
        Returns:
            str: HTTP 요청 문자열
        """
        # 1. 요청 라인 (Request Line)
        # 예: "GET /index.html HTTP/1.1"
        request_line = f"{self.method} {self.path} {HTTP_VERSION}{CRLF}"
        
        # 2. Content-Length 헤더 자동 추가 (바디가 있는 경우)
        if self.body and 'Content-Length' not in self.headers:
            self.headers['Content-Length'] = str(len(self.body.encode('utf-8')))
        
        # 3. 헤더
        header_lines = ''
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}{CRLF}"
        
        # 4. 요청 조합 (요청 라인 + 헤더 + 빈 줄 + 바디)
        request = request_line + header_lines + CRLF + self.body
        
        return request
    
    @staticmethod
    def build_GET(path, headers=None):
        """GET 요청 생성 헬퍼 메소드"""
        return HTTPRequest('GET', path, headers)
    
    @staticmethod
    def build_HEAD(path, headers=None):
        """HEAD 요청 생성 헬퍼 메소드"""
        return HTTPRequest('HEAD', path, headers)
    
    @staticmethod
    def build_POST(path, data, headers=None):
        """
        POST 요청 생성 헬퍼 메소드
        
        Args:
            path (str): 요청 경로
            data (dict): JSON으로 변환할 데이터
            headers (dict): 추가 헤더
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        body = json.dumps(data, ensure_ascii=False)
        return HTTPRequest('POST', path, headers, body)
    
    @staticmethod
    def build_PUT(path, data, headers=None):
        """
        PUT 요청 생성 헬퍼 메소드
        
        Args:
            path (str): 요청 경로
            data (dict): JSON으로 변환할 데이터
            headers (dict): 추가 헤더
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        body = json.dumps(data, ensure_ascii=False)
        return HTTPRequest('PUT', path, headers, body)
    
    @staticmethod
    def build_DELETE(path, headers=None):
        """DELETE 요청 생성 헬퍼 메소드"""
        return HTTPRequest('DELETE', path, headers)
    
    @staticmethod
    def build_PATCH(path, data, headers=None):
        """
        PATCH 요청 생성 헬퍼 메소드
        
        Args:
            path (str): 요청 경로
            data (dict): JSON으로 변환할 데이터 (부분 업데이트)
            headers (dict): 추가 헤더
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        body = json.dumps(data, ensure_ascii=False)
        return HTTPRequest('PATCH', path, headers, body)
