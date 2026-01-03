"""
HTTP 응답 생성 모듈
상태 코드, 헤더, 바디를 조합하여 HTTP 응답 문자열을 생성합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import HTTP_VERSION, STATUS_CODES, CRLF
from datetime import datetime


class HTTPResponse:
    """HTTP 응답을 생성하는 클래스"""
    
    def __init__(self, status_code=200, headers=None, body=''):
        """
        Args:
            status_code (int): HTTP 상태 코드 (200, 404 등)
            headers (dict): 응답 헤더 딕셔너리
            body (str): 응답 바디
        """
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body
        
        # 기본 헤더 설정
        if 'Server' not in self.headers:
            self.headers['Server'] = 'Python-Socket-Server/1.0'
        if 'Date' not in self.headers:
            self.headers['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    def set_header(self, key, value):
        """헤더 추가/수정"""
        self.headers[key] = value
    
    def build_response(self):
        """
        HTTP 응답 문자열을 생성합니다.
        
        Returns:
            str: 완성된 HTTP 응답 문자열
        """
        # 1. 상태 라인 생성
        # 예: "HTTP/1.1 200 OK"
        status_message = STATUS_CODES.get(self.status_code, 'Unknown')
        status_line = f"{HTTP_VERSION} {self.status_code} {status_message}{CRLF}"
        
        # 2. Content-Length 헤더 자동 추가
        if self.body and 'Content-Length' not in self.headers:
            self.headers['Content-Length'] = str(len(self.body.encode('utf-8')))
        
        # 3. 헤더 생성
        header_lines = ''
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}{CRLF}"
        
        # 4. 응답 조합 (상태 라인 + 헤더 + 빈 줄 + 바디)
        response = status_line + header_lines + CRLF + self.body
        
        return response
    
    @staticmethod
    def create_200_response(body, content_type='text/html'):
        """200 OK 응답 생성 헬퍼 메소드"""
        headers = {'Content-Type': content_type}
        return HTTPResponse(200, headers, body)
    
    @staticmethod
    def create_201_response(body):
        """201 Created 응답 생성 헬퍼 메소드"""
        headers = {'Content-Type': 'application/json'}
        return HTTPResponse(201, headers, body)
    
    @staticmethod
    def create_400_response(message='Bad Request'):
        """400 Bad Request 응답 생성 헬퍼 메소드"""
        headers = {'Content-Type': 'text/plain'}
        return HTTPResponse(400, headers, message)
    
    @staticmethod
    def create_404_response(message='Not Found'):
        """404 Not Found 응답 생성 헬퍼 메소드"""
        headers = {'Content-Type': 'text/plain'}
        return HTTPResponse(404, headers, message)
    
    @staticmethod
    def create_500_response(message='Internal Server Error'):
        """500 Internal Server Error 응답 생성 헬퍼 메소드"""
        headers = {'Content-Type': 'text/plain'}
        return HTTPResponse(500, headers, message)
