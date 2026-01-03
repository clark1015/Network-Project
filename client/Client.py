"""
HTTP 클라이언트
서버에 연결하여 다양한 HTTP 요청을 전송하고 응답을 받습니다.
"""

import socket
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import CLIENT_HOST, DEFAULT_PORT, BUFFER_SIZE
from client.HTTPRequest import HTTPRequest


class HTTPClient:
    """HTTP 클라이언트 클래스"""
    
    def __init__(self, host=CLIENT_HOST, port=DEFAULT_PORT):
        """
        Args:
            host (str): 서버 호스트
            port (int): 서버 포트
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """서버에 연결"""
        try:
            # 1. 소켓 생성
            # socket.AF_INET: IPv4 주소 체계 사용
            # socket.SOCK_STREAM: TCP 프로토콜 사용 (연결 지향, 신뢰성)
            #   (vs SOCK_DGRAM: UDP - 비연결, 빠르지만 신뢰성 낮음)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 2. 서버에 연결 (connect)
            self.socket.connect((self.host, self.port))
            print(f"✅ 서버 연결 성공: {self.host}:{self.port}")
            return True
        
        except Exception as e:
            print(f"❌ 서버 연결 실패: {e}")
            return False
    
    def send_request(self, request):
        """
        HTTP 요청 전송
        
        Args:
            request (HTTPRequest): 전송할 요청 객체
        """
        try:
            # HTTPRequest 객체 → 문자열 → 바이트
            request_string = request.to_string()
            request_bytes = request_string.encode('utf-8')
            
            # 요청 전송
            self.socket.send(request_bytes)
            print(f"📤 요청 전송: {request.method} {request.path}")
        
        except Exception as e:
            print(f"❌ 요청 전송 실패: {e}")
    
    def receive_response(self):
        """
        HTTP 응답 수신
        
        Returns:
            str: 응답 문자열
        """
        try:
            # 응답 받기 (recv: 블로킹 함수)
            # - 서버로부터 데이터가 올 때까지 여기서 **대기** (멈춤)
            # - 응답이 오면 그때 다음 줄로 진행
            # - 동기 방식: 응답 올 때까지 기다림 (비동기 아님)
            # - BUFFER_SIZE(4096바이트)만큼 수신
            response_bytes = self.socket.recv(BUFFER_SIZE)
            
            # 바이트 → 문자열
            response_string = response_bytes.decode('utf-8')
            
            print(f"📥 응답 수신 완료")
            return response_string
        
        except Exception as e:
            print(f"❌응답 수신 실패: {e}")
            return None
    
    def close(self):
        """연결 종료"""
        if self.socket:
            self.socket.close()
            print(f"🔌 연결 종료\n")
    
    def send_and_receive(self, request):
        """
        요청 전송 및 응답 수신 (편의 메소드)
        
        Args:
            request (HTTPRequest): 전송할 요청
            
        Returns:
            str: 응답 문자열
        """
        if not self.connect():
            return None
        
        self.send_request(request)
        response = self.receive_response()
        self.close()
        
        return response


def print_response(response):
    """응답을 보기 좋게 출력"""
    if not response:
        return
    
    print("=" * 60)
    print("📋 응답 내용:")
    print("=" * 60)
    
    # 상태 라인과 헤더만 출력 (바디는 너무 길 수 있음)
    lines = response.split('\r\n')
    
    # 상태 라인
    print(f"상태: {lines[0]}")
    
    # 헤더
    print("\n헤더:")
    i = 1
    while i < len(lines) and lines[i] != '':
        print(f"  {lines[i]}")
        i += 1
    
    # 바디 (처음 200자만)
    if i + 1 < len(lines):
        body = '\r\n'.join(lines[i + 1:])
        if len(body) > 200:
            print(f"\n바디 (처음 200자): {body[:200]}...")
        else:
            print(f"\n바디: {body}")
    
    print("=" * 60)
    print()


def main():
    """
    메인 함수
    
    CLI 클라이언트는 자동 테스트용으로만 사용됩니다.
    GUI 클라이언트를 사용하면 모든 요청을 직접 테스트할 수 있습니다.
    """
    
    print("=" * 70)
    print("🚀 HTTP Socket Client")
    print("=" * 70)
    print()
    print("이 CLI 클라이언트는 자동 테스트용입니다.")
    print()
    print("💡 GUI 클라이언트 사용을 권장합니다:")
    print("   python3 client/ClientGUI.py")
    print()
    print("GUI에서 다음 기능을 사용할 수 있습니다:")
    print("  ✅ 서버 IP/포트 설정")
    print("  ✅ 모든 HTTP 메소드 선택 (GET, HEAD, POST, PUT, DELETE, PATCH)")
    print("  ✅ 경로 및 바디 직접 입력")
    print("  ✅ 빠른 테스트 버튼")
    print("  ✅ 실시간 요청/응답 확인")
    print()
    print("=" * 70)
    print()
    
    # 간단한 테스트 예시
    choice = input("간단한 테스트를 실행하시겠습니까? (y/n): ").strip().lower()
    
    if choice == 'y':
        print("\n🧪 GET / 테스트 실행 중...\n")
        
        client = HTTPClient()
        request = HTTPRequest.build_GET('/')
        response = client.send_and_receive(request)
        
        if response:
            print_response(response)
        
        print("\n✅ 테스트 완료!")
        print("\n더 많은 테스트를 하려면 GUI 클라이언트를 사용하세요:")
        print("  python3 client/ClientGUI.py")
    else:
        print("\nGUI 클라이언트를 실행하세요:")
        print("  python3 client/ClientGUI.py")


if __name__ == '__main__':
    main()
