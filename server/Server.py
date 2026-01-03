"""
HTTP 소켓 서버 (멀티스레딩)
TCP 소켓을 사용하여 HTTP 요청을 받고 응답하는 서버입니다.
각 클라이언트 연결을 별도의 스레드로 처리합니다.
"""

import socket
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import DEFAULT_HOST, DEFAULT_PORT, BUFFER_SIZE
from server.HTTPParser import HTTPParser
from server.HTTPHandler import HTTPHandler


class HTTPServer:
    """멀티스레딩 HTTP 서버"""
    
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """
        Args:
            host (str): 서버 호스트 주소
            port (int): 서버 포트 번호
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.handler = HTTPHandler()
    
    def start(self):
        """서버 시작"""
        try:
            # 1. 소켓 생성 (IPv4, TCP)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 소켓 옵션 설정 (포트 재사용 가능)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 2. bind: 주소와 포트 바인딩
            self.server_socket.bind((self.host, self.port))
            
            # 3. listen: 연결 대기 (최대 10개 대기 큐)
            self.server_socket.listen(10)
            
            self.running = True
            print(f"🚀 서버 시작: http://{self.host}:{self.port}")
            print(f"📡 연결 대기 중... (Ctrl+C로 종료)")
            print("-" * 50)
            
            # 4. accept 루프: 클라이언트 연결 수락
            while self.running:
                try:
                    # accept(): 클라이언트 연결 대기 (블로킹)
                    client_socket, client_address = self.server_socket.accept()
                    print(f"✅ 클라이언트 연결: {client_address}")
                    
                    # 새 스레드 생성하여 클라이언트 처리
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    print("\n\n⚠️  서버 종료 중...")
                    break
                except Exception as e:
                    print(f"❌ 연결 수락 에러: {e}")
        
        except Exception as e:
            print(f"❌ 서버 시작 실패: {e}")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, client_address):
        """
        클라이언트 요청 처리 (별도 스레드에서 실행)
        
        Args:
            client_socket: 클라이언트 소켓
            client_address: 클라이언트 주소
        """
        try:
            # 1. 요청 받기 (recv: 블로킹)
            raw_data = client_socket.recv(BUFFER_SIZE)
            
            if not raw_data:
                return
            
            # 바이트 → 문자열 변환
            request_string = raw_data.decode('utf-8')
            
            print(f"\n📨 요청 받음 from {client_address}:")
            print(request_string.split('\r\n')[0])  # 요청 라인만 출력
            
            # 2. 요청 파싱
            parser = HTTPParser()
            parsed = parser.parse_request(request_string)
            
            if not parsed:
                # 파싱 실패 → 400 Bad Request
                response = "HTTP/1.1 400 Bad Request\r\n\r\nBad Request"
                client_socket.send(response.encode('utf-8'))
                return
            
            # 3. 요청 처리
            method = parsed['method']
            path = parsed['path']
            headers = parsed['headers']
            body = parsed['body']
            
            response_obj = self.handler.handle_request(method, path, headers, body)
            
            # 4. 응답 생성
            response_string = response_obj.build_response()
            
            print(f"📤 응답 전송: {response_obj.status_code} {method} {path}")
            
            # 5. 응답 전송 (문자열 → 바이트)
            client_socket.send(response_string.encode('utf-8'))
        
        except Exception as e:
            print(f"❌ 클라이언트 처리 에러: {e}")
            try:
                error_response = "HTTP/1.1 500 Internal Server Error\r\n\r\nServer Error"
                client_socket.send(error_response.encode('utf-8'))
            except:
                pass
        finally:
            # 6. 연결 종료
            client_socket.close()
            print(f"🔌 연결 종료: {client_address}")
    
    def shutdown(self):
        """서버 종료"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("✅ 서버 종료 완료")


if __name__ == '__main__':
    # 서버 실행
    server = HTTPServer()
    server.start()
