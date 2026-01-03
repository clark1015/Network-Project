"""
HTTP 클라이언트 웹 GUI (Flask)
브라우저에서 실행되는 HTTP 클라이언트입니다.
"""

from flask import Flask, render_template, request, jsonify
import socket
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.HTTPConstants import CLIENT_HOST, DEFAULT_PORT, BUFFER_SIZE
from client.HTTPRequest import HTTPRequest

app = Flask(__name__)


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/send_request', methods=['POST'])
def send_request():
    """HTTP 요청 전송"""
    try:
        # 요청 데이터 받기
        data = request.json
        host = data.get('host', CLIENT_HOST)
        port = int(data.get('port', DEFAULT_PORT))
        method = data.get('method', 'GET')
        path = data.get('path', '/')
        body = data.get('body', '')
        
        # HTTP 요청 생성
        if method == 'GET':
            http_request = HTTPRequest.build_GET(path)
        elif method == 'HEAD':
            http_request = HTTPRequest.build_HEAD(path)
        elif method == 'POST':
            body_data = json.loads(body) if body else {}
            http_request = HTTPRequest.build_POST(path, body_data)
        elif method == 'PUT':
            body_data = json.loads(body) if body else {}
            http_request = HTTPRequest.build_PUT(path, body_data)
        elif method == 'DELETE':
            http_request = HTTPRequest.build_DELETE(path)
        elif method == 'PATCH':
            body_data = json.loads(body) if body else {}
            http_request = HTTPRequest.build_PATCH(path, body_data)
        else:
            return jsonify({'error': f'Unsupported method: {method}'}), 400
        
        # 소켓 연결
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # 5초 타임아웃
        client_socket.connect((host, port))
        
        # 요청 전송
        request_string = http_request.to_string()
        client_socket.send(request_string.encode('utf-8'))
        
        # 응답 수신
        response_bytes = client_socket.recv(BUFFER_SIZE)
        response_string = response_bytes.decode('utf-8')
        
        # 연결 종료
        client_socket.close()
        
        # 응답 반환
        return jsonify({
            'success': True,
            'request': request_string,
            'response': response_string
        })
    
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400
    except ConnectionRefusedError:
        return jsonify({'error': f'Connection refused: {host}:{port}'}), 500
    except socket.timeout:
        return jsonify({'error': 'Request timeout (5s)'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("🌐 HTTP 클라이언트 웹 GUI 시작")
    print("=" * 70)
    print()
    print("브라우저에서 다음 주소로 접속하세요:")
    print("  👉 http://localhost:5000")
    print()
    print("종료하려면 Ctrl+C를 누르세요.")
    print("=" * 70)
    print()
    
    app.run(debug=True, port=5000, use_reloader=False)
