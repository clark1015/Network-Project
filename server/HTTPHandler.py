"""
HTTP 요청 처리 모듈
각 HTTP 메소드(GET, HEAD, POST, PUT, DELETE, PATCH)에 대한 처리 로직을 담당합니다.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.HTTPResponse import HTTPResponse


class HTTPHandler:
    """HTTP 요청을 처리하는 클래스"""
    
    def __init__(self, data_dir=None):
        """
        Args:
            data_dir (str): 데이터 파일이 저장된 디렉토리 경로 (기본값: 현재 파일 기준 data 디렉토리)
        """
        if data_dir is None:
            # 현재 파일의 디렉토리를 기준으로 절대 경로 생성
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, 'data')
        
        self.data_dir = data_dir
        self.static_dir = os.path.join(data_dir, 'static')
        self.users_file = os.path.join(data_dir, 'users.json')
    
    def handle_request(self, method, path, headers, body):
        """
        요청 메소드에 따라 적절한 핸들러 호출
        
        Args:
            method (str): HTTP 메소드
            path (str): 요청 경로
            headers (dict): 요청 헤더
            body (str): 요청 바디
            
        Returns:
            HTTPResponse: 생성된 HTTP 응답 객체
        """
        if method == 'GET':
            return self.handle_GET(path)
        elif method == 'HEAD':
            return self.handle_HEAD(path)
        elif method == 'POST':
            return self.handle_POST(path, body)
        elif method == 'PUT':
            return self.handle_PUT(path, body)
        elif method == 'DELETE':
            return self.handle_DELETE(path)
        elif method == 'PATCH':
            return self.handle_PATCH(path, body)
        else:
            return HTTPResponse.create_400_response(f'Unsupported method: {method}')
    
    def handle_GET(self, path):
        """
        GET 요청 처리: API 엔드포인트 및 정적 파일 자동 반환
        
        - GET /users → users.json 반환 (200, 딕셔너리 → 리스트 변환)
        - GET / → index.html 반환 (200)
        - GET /about → about.html 반환 (200, 자동으로 .html 확장자 추가)
        - GET /notfound → 404 반환
        
        정적 파일은 파일 시스템 기반으로 자동 서빙됩니다.
        """
        try:
            # 1. API 엔드포인트 처리 (/users)
            if path == '/users':
                # 딕셔너리 → 리스트 변환 (클라이언트 호환성)
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 딕셔너리 values를 리스트로 변환
                users_list = list(data['users'].values())
                response_data = {'users': users_list}
                content = json.dumps(response_data, ensure_ascii=False)
                return HTTPResponse.create_200_response(content, 'application/json')
            
            # 2. 정적 파일 자동 처리
            # 루트 경로(/) → index.html로 변환
            if path == '/':
                path = '/index.html'
            
            # 확장자 없는 경로 → .html 자동 추가 (예: /about → /about.html)
            if not '.' in path:
                path = path + '.html'
            
            # 파일 시스템 경로 생성 (예: /about.html → server/data/static/about.html)
            file_path = os.path.join(self.static_dir, path.lstrip('/'))
            
            # 파일 존재 확인 및 반환
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Content-Type 자동 감지
                content_type = self._get_content_type(file_path)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return HTTPResponse.create_200_response(content, content_type)
            else:
                # 파일이 존재하지 않음 → 404
                return HTTPResponse.create_404_response(f'File not found: {path}')
        
        except FileNotFoundError:
            return HTTPResponse.create_404_response(f'File not found: {path}')
        except Exception as e:
            return HTTPResponse.create_500_response(f'Server error: {str(e)}')
    
    def handle_HEAD(self, path):
        """
        HEAD 요청 처리: GET과 동일하지만 바디 없이 헤더만 반환
        
        - HEAD / → 200 (바디 없음)
        """
        # GET과 동일한 로직으로 응답 생성
        response = self.handle_GET(path)
        # 바디만 제거
        response.body = ''
        return response
    
    def handle_POST(self, path, body):
        """
        POST 요청 처리: 새 데이터 생성
        
        - POST /users (올바른 JSON) → 201 Created
        - POST /users (잘못된 JSON) → 400 Bad Request
        """
        if path == '/users':
            try:
                # JSON 파싱
                user_data = json.loads(body)
                
                # 기존 데이터 읽기
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Auto Increment ID 생성 (O(1))
                new_id = data['next_id']
                data['next_id'] += 1
                
                # 사용자 데이터에 ID 추가
                user_data['id'] = new_id
                
                # 딕셔너리에 추가 (O(1))
                data['users'][str(new_id)] = user_data
                
                # 파일에 저장
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # 201 Created 응답
                response_body = json.dumps({'message': 'User created', 'user': user_data}, ensure_ascii=False)
                return HTTPResponse.create_201_response(response_body)
            
            except json.JSONDecodeError:
                return HTTPResponse.create_400_response('Invalid JSON format')
            except Exception as e:
                return HTTPResponse.create_500_response(f'Server error: {str(e)}')
        else:
            return HTTPResponse.create_404_response(f'Endpoint not found: {path}')
    
    def handle_PUT(self, path, body):
        """
        PUT 요청 처리: 데이터 전체 수정
        
        - PUT /users/1 (존재하는 사용자) → 200 OK
        - PUT /users/999 (존재하지 않는 사용자) → 404 Not Found
        """
        # 경로에서 사용자 ID 추출
        if path.startswith('/users/'):
            try:
                user_id = int(path.split('/')[-1])
                user_id_str = str(user_id)
                
                # JSON 파싱
                updated_data = json.loads(body)
                
                # 기존 데이터 읽기
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 사용자 존재 확인 (O(1))
                if user_id_str in data['users']:
                    # ID 유지
                    updated_data['id'] = user_id
                    
                    # 딕셔너리 업데이트 (O(1))
                    data['users'][user_id_str] = updated_data
                    
                    # 파일에 저장
                    with open(self.users_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    # 200 OK 응답
                    response_body = json.dumps({'message': 'User updated', 'user': updated_data}, ensure_ascii=False)
                    return HTTPResponse.create_200_response(response_body, 'application/json')
                else:
                    return HTTPResponse.create_404_response(f'User not found: {user_id}')
            
            except json.JSONDecodeError:
                return HTTPResponse.create_400_response('Invalid JSON format')
            except ValueError:
                return HTTPResponse.create_400_response('Invalid user ID')
            except Exception as e:
                return HTTPResponse.create_500_response(f'Server error: {str(e)}')
        else:
            return HTTPResponse.create_404_response(f'Endpoint not found: {path}')
    
    def handle_DELETE(self, path):
        """
        DELETE 요청 처리: 데이터 삭제
        
        - DELETE /users/1 (존재하는 사용자) → 200 OK
        - DELETE /users/999 (존재하지 않는 사용자) → 404 Not Found
        """
        # 경로에서 사용자 ID 추출
        if path.startswith('/users/'):
            try:
                user_id = int(path.split('/')[-1])
                user_id_str = str(user_id)
                
                # 기존 데이터 읽기
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 사용자 존재 확인 및 삭제 (O(1))
                if user_id_str in data['users']:
                    deleted_user = data['users'].pop(user_id_str)
                    
                    # 파일에 저장
                    with open(self.users_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    # 200 OK 응답
                    response_body = json.dumps({'message': 'User deleted', 'user': deleted_user}, ensure_ascii=False)
                    return HTTPResponse.create_200_response(response_body, 'application/json')
                else:
                    return HTTPResponse.create_404_response(f'User not found: {user_id}')
            
            except ValueError:
                return HTTPResponse.create_400_response('Invalid user ID')
            except Exception as e:
                return HTTPResponse.create_500_response(f'Server error: {str(e)}')
        else:
            return HTTPResponse.create_404_response(f'Endpoint not found: {path}')
    
    def handle_PATCH(self, path, body):
        """
        PATCH 요청 처리: 데이터 부분 수정
        
        - PATCH /users/1 (존재하는 사용자) → 200 OK
        - PATCH /users/999 (존재하지 않는 사용자) → 404 Not Found
        
        PUT과의 차이: PUT은 전체 리소스 교체, PATCH는 부분 수정
        (이 구현에서는 동작이 유사하지만, 의미적으로 구분)
        """
        # 경로에서 사용자 ID 추출
        if path.startswith('/users/'):
            try:
                user_id = int(path.split('/')[-1])
                user_id_str = str(user_id)
                
                # JSON 파싱
                patch_data = json.loads(body)
                
                # 기존 데이터 읽기
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 사용자 존재 확인 (O(1))
                if user_id_str in data['users']:
                    # 부분 업데이트 (기존 필드 유지, 새 필드만 변경)
                    for key, value in patch_data.items():
                        if key != 'id':  # ID는 변경 불가
                            data['users'][user_id_str][key] = value
                    
                    # 파일에 저장
                    with open(self.users_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    # 200 OK 응답
                    response_body = json.dumps({'message': 'User patched', 'user': data['users'][user_id_str]}, ensure_ascii=False)
                    return HTTPResponse.create_200_response(response_body, 'application/json')
                else:
                    return HTTPResponse.create_404_response(f'User not found: {user_id}')
            
            except json.JSONDecodeError:
                return HTTPResponse.create_400_response('Invalid JSON format')
            except ValueError:
                return HTTPResponse.create_400_response('Invalid user ID')
            except Exception as e:
                return HTTPResponse.create_500_response(f'Server error: {str(e)}')
        else:
            return HTTPResponse.create_404_response(f'Endpoint not found: {path}')
    
    def _get_content_type(self, file_path):
        """
        파일 확장자에 따라 Content-Type 자동 감지
        
        Args:
            file_path (str): 파일 경로
            
        Returns:
            str: Content-Type 문자열
        """
        if file_path.endswith('.html'):
            return 'text/html'
        elif file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'application/javascript'
        elif file_path.endswith('.json'):
            return 'application/json'
        elif file_path.endswith('.png'):
            return 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            return 'image/jpeg'
        elif file_path.endswith('.gif'):
            return 'image/gif'
        elif file_path.endswith('.svg'):
            return 'image/svg+xml'
        else:
            return 'text/plain'
