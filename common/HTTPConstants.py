"""
HTTP 상수 정의 모듈
HTTP 메소드, 상태 코드, 기본 헤더 등을 정의합니다.
"""

# HTTP 메소드
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH']

# HTTP 상태 코드와 메시지
STATUS_CODES = {
    200: 'OK',
    201: 'Created',
    400: 'Bad Request',
    404: 'Not Found',
    500: 'Internal Server Error'
}

# HTTP 버전
HTTP_VERSION = 'HTTP/1.1'

# 기본 설정
# 서버용: 모든 네트워크 인터페이스에서 접속 허용
SERVER_HOST = '0.0.0.0'
# 클라이언트용: 기본 접속 주소 (사용자가 변경 가능)
CLIENT_HOST = 'localhost'
# 하위 호환성을 위한 별칭
DEFAULT_HOST = SERVER_HOST  # 서버에서 사용
DEFAULT_PORT = 8080
BUFFER_SIZE = 4096

# CRLF (줄바꿈)
CRLF = '\r\n'
