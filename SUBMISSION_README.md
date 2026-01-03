# HTTP 소켓 프로그래밍 프로젝트 - 제출 문서

## 📋 프로젝트 개요

본 프로젝트는 Python의 소켓 프로그래밍을 활용하여 HTTP/1.1 프로토콜을 구현한 웹 서버 및 클라이언트 시스템입니다. TCP 소켓을 기반으로 HTTP 요청/응답을 처리하며, RESTful API를 지원합니다.

### 주요 특징

- **멀티스레딩 서버**: 여러 클라이언트의 동시 접속 처리
- **웹 기반 GUI 클라이언트**: Flask를 활용한 브라우저 기반 인터페이스
- **네트워크 간 통신 지원**: 0.0.0.0 바인딩으로 외부 접속 허용
- **RESTful API**: GET, HEAD, POST, PUT, DELETE, PATCH 메소드 지원
- **JSON 기반 데이터 관리**: 딕셔너리 구조로 O(1) 성능 보장

---

## 📁 프로젝트 구조

```
Network-Project/
├── server/                      # 서버 모듈
│   ├── Server.py               # 메인 서버 (멀티스레딩)
│   ├── HTTPHandler.py          # HTTP 요청 처리 로직
│   ├── HTTPParser.py           # HTTP 요청 파싱
│   ├── HTTPResponse.py         # HTTP 응답 생성
│   └── data/                   # 데이터 및 정적 파일
│       ├── users.json          # 사용자 데이터 (JSON)
│       └── static/             # 정적 HTML 파일
│           ├── index.html
│           └── about.html
├── client/                      # 클라이언트 모듈
│   ├── Client.py               # CLI 클라이언트
│   ├── ClientWeb.py            # 웹 GUI 클라이언트 (Flask)
│   ├── HTTPRequest.py          # HTTP 요청 생성
│   └── templates/              # Flask 템플릿
│       └── index.html          # 웹 GUI 인터페이스
├── common/                      # 공통 모듈
│   └── HTTPConstants.py        # HTTP 상수 정의
├── captures/                    # Wireshark 캡처 파일
├── README.md                    # 프로젝트 개요
├── GUI_GUIDE.md                # GUI 사용 가이드
└── WIRESHARK_GUIDE.md          # Wireshark 캡처 가이드
```

---

## 💻 소스 파일 설명

### 1. 서버 모듈 (server/)

#### `Server.py` (5.3 KB)
- **역할**: HTTP 서버의 메인 실행 파일
- **주요 기능**:
  - TCP 소켓 생성 및 바인딩 (0.0.0.0:8080)
  - 멀티스레딩을 통한 동시 클라이언트 처리
  - 각 클라이언트 연결을 별도 스레드로 처리
- **핵심 코드**:
  ```python
  # 모든 네트워크 인터페이스에서 접속 허용
  self.server_socket.bind(('0.0.0.0', 8080))
  
  # 각 클라이언트를 별도 스레드로 처리
  client_thread = threading.Thread(
      target=self.handle_client,
      args=(client_socket, client_address)
  )
  client_thread.start()
  ```

#### `HTTPHandler.py` (13.6 KB)
- **역할**: HTTP 요청 메소드별 처리 로직
- **주요 기능**:
  - GET: 정적 파일 자동 서빙 (파일 시스템 기반)
  - POST: 새 사용자 생성 (Auto Increment ID)
  - PUT: 사용자 정보 전체 수정
  - PATCH: 사용자 정보 부분 수정
  - DELETE: 사용자 삭제
  - HEAD: 헤더만 반환
- **설계 특징**:
  - 딕셔너리 기반 데이터 구조로 O(1) 검색/삽입/삭제
  - Content-Type 자동 감지 (HTML, CSS, JS, JSON, 이미지 등)
  - 정적 파일 자동 라우팅 (코드 수정 없이 파일 추가 가능)

#### `HTTPParser.py` (2.6 KB)
- **역할**: HTTP 요청 문자열 파싱
- **주요 기능**:
  - Request Line 파싱 (메소드, 경로, HTTP 버전)
  - 헤더 파싱 (Key-Value 딕셔너리)
  - 바디 추출 (JSON 데이터)

#### `HTTPResponse.py` (3.3 KB)
- **역할**: HTTP 응답 생성
- **주요 기능**:
  - 상태 코드별 응답 생성 (200, 201, 400, 404, 500)
  - Content-Length 자동 계산
  - 기본 헤더 자동 추가 (Server, Date)

---

### 2. 클라이언트 모듈 (client/)

#### `ClientWeb.py` (3.3 KB)
- **역할**: Flask 기반 웹 GUI 클라이언트
- **주요 기능**:
  - 브라우저에서 HTTP 요청 전송
  - 실시간 요청/응답 확인
  - 모든 HTTP 메소드 지원
- **실행 방법**:
  ```bash
  python3 client/ClientWeb.py
  # 브라우저에서 http://localhost:5000 접속
  ```

#### `Client.py` (6.0 KB)
- **역할**: CLI 기반 클라이언트
- **주요 기능**:
  - 터미널에서 HTTP 요청 전송
  - 각 메소드별 테스트 함수 제공

#### `HTTPRequest.py` (4.1 KB)
- **역할**: HTTP 요청 메시지 생성
- **주요 기능**:
  - 메소드별 요청 빌더 (GET, POST, PUT, DELETE, PATCH, HEAD)
  - JSON 바디 자동 직렬화
  - Content-Length 자동 계산

---

### 3. 공통 모듈 (common/)

#### `HTTPConstants.py` (512 B)
- **역할**: HTTP 프로토콜 상수 정의
- **주요 내용**:
  - HTTP 메소드 목록
  - 상태 코드 및 메시지
  - 서버/클라이언트 기본 설정
  ```python
  SERVER_HOST = '0.0.0.0'      # 모든 네트워크 인터페이스
  CLIENT_HOST = 'localhost'     # 클라이언트 기본값
  DEFAULT_PORT = 8080
  ```

---

## 🖥️ 동작 환경

### 필수 요구사항

- **운영체제**: macOS, Linux, Windows
- **Python 버전**: Python 3.7 이상
- **필수 라이브러리**:
  ```bash
  pip install flask
  ```

### 테스트 환경

본 프로젝트는 다음 환경에서 개발 및 테스트되었습니다:

- **OS**: macOS
- **Python**: 3.x
- **네트워크**: Wi-Fi (172.30.1.59)
- **테스트 도구**: Wireshark 4.x

---

## 🚀 실행 방법

### 1. 서버 실행

```bash
cd Network-Project
python3 server/Server.py
```

**출력 예시**:
```
🚀 서버 시작: http://0.0.0.0:8080
📡 연결 대기 중... (Ctrl+C로 종료)
--------------------------------------------------
```

### 2. 클라이언트 실행

#### 방법 A: 웹 GUI 클라이언트 (권장)

```bash
python3 client/ClientWeb.py
```

브라우저에서 `http://localhost:5000` 접속

#### 방법 B: CLI 클라이언트

```bash
python3 client/Client.py
```

---

## 🌐 네트워크 간 테스트 (다른 컴퓨터에서 접속)

### 설정 이유

본 프로젝트는 **0.0.0.0:8080**으로 서버를 바인딩하여 **모든 네트워크 인터페이스**에서 접속을 허용합니다.

- **localhost (127.0.0.1)**: 같은 컴퓨터에서만 접속 가능
- **0.0.0.0**: 모든 네트워크 인터페이스에서 접속 가능 (Wi-Fi, Ethernet 등)

### 다른 컴퓨터에서 접속 방법

1. **서버 컴퓨터의 IP 주소 확인**:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   예시 출력: `inet 172.30.1.59`

2. **같은 Wi-Fi 네트워크에 연결**

3. **클라이언트에서 서버 IP로 접속**:
   - 웹 GUI: Host 필드에 `172.30.1.59` 입력
   - 브라우저: `http://172.30.1.59:8080` 접속

---

## 📡 HTTP 명령어 결과

### 1. GET 요청

#### 요청 (성공 - 200 OK)

```http
GET / HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0

```

#### 응답

```http
HTTP/1.1 200 OK
Content-Type: text/html
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 1343

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>HTTP 서버 홈</title>
</head>
<body>
    <h1>HTTP 소켓 서버에 오신 것을 환영합니다!</h1>
    ...
</body>
</html>
```

#### 요청 (실패 - 404 Not Found)

```http
GET /notfound HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0

```

#### 응답

```http
HTTP/1.1 404 Not Found
Content-Type: text/plain
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 25

File not found: /notfound
```

---

### 2. HEAD 요청

#### 요청

```http
HEAD / HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0

```

#### 응답 (바디 없음)

```http
HTTP/1.1 200 OK
Content-Type: text/html
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT

```

**특징**: GET과 동일하지만 응답 바디가 없음 (헤더만 반환)

---

### 3. POST 요청

#### 요청 (성공 - 201 Created)

```http
POST /users HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0
Content-Type: application/json
Content-Length: 52

{"name": "Charlie", "email": "charlie@example.com"}
```

#### 응답

```http
HTTP/1.1 201 Created
Content-Type: application/json
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 97

{"message": "User created", "user": {"id": 3, "name": "Charlie", "email": "charlie@example.com"}}
```

**특징**: Auto Increment ID 자동 생성 (next_id 사용)

#### 요청 (실패 - 400 Bad Request)

```http
POST /users HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0
Content-Type: application/json
Content-Length: 12

invalid json
```

#### 응답

```http
HTTP/1.1 400 Bad Request
Content-Type: text/plain
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 19

Invalid JSON format
```

---

### 4. PUT 요청

#### 요청 (성공 - 200 OK)

```http
PUT /users/1 HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0
Content-Type: application/json
Content-Length: 60

{"name": "Alice Updated", "email": "alice_new@example.com"}
```

#### 응답

```http
HTTP/1.1 200 OK
Content-Type: application/json
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 105

{"message": "User updated", "user": {"id": 1, "name": "Alice Updated", "email": "alice_new@example.com"}}
```

**특징**: 전체 리소스 교체 (기존 데이터 덮어쓰기)

#### 요청 (실패 - 404 Not Found)

```http
PUT /users/999 HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0
Content-Type: application/json
Content-Length: 24

{"name": "NonExistent"}
```

#### 응답

```http
HTTP/1.1 404 Not Found
Content-Type: text/plain
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 19

User not found: 999
```

---

### 5. PATCH 요청

#### 요청 (성공 - 200 OK)

```http
PATCH /users/1 HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0
Content-Type: application/json
Content-Length: 20

{"name": "Alice V2"}
```

#### 응답

```http
HTTP/1.1 200 OK
Content-Type: application/json
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 95

{"message": "User patched", "user": {"id": 1, "name": "Alice V2", "email": "alice_new@example.com"}}
```

**특징**: 부분 수정 (name만 변경, email은 유지)

---

### 6. DELETE 요청

#### 요청 (성공 - 200 OK)

```http
DELETE /users/1 HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0

```

#### 응답

```http
HTTP/1.1 200 OK
Content-Type: application/json
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 95

{"message": "User deleted", "user": {"id": 1, "name": "Alice Updated", "email": "alice_new@example.com"}}
```

#### 요청 (실패 - 404 Not Found)

```http
DELETE /users/999 HTTP/1.1
Host: localhost:8080
User-Agent: Python-Socket-Client/1.0

```

#### 응답

```http
HTTP/1.1 404 Not Found
Content-Type: text/plain
Server: Python-Socket-Server/1.0
Date: Fri, 03 Jan 2026 04:57:02 GMT
Content-Length: 19

User not found: 999
```

---

## 🎯 주요 설계 결정 및 구현 특징

### 1. 멀티스레딩 방식 선택

#### 선택 이유

- **동시성**: 여러 클라이언트가 동시에 접속해도 서버가 멈추지 않음
- **응답성**: 한 클라이언트의 요청이 느려도 다른 클라이언트에 영향 없음
- **확장성**: 클라이언트 수에 따라 자동으로 스레드 생성

#### 구현 방식

```python
# Server.py
while self.running:
    client_socket, client_address = self.server_socket.accept()
    
    # 각 클라이언트를 별도 스레드로 처리
    client_thread = threading.Thread(
        target=self.handle_client,
        args=(client_socket, client_address)
    )
    client_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
    client_thread.start()
```

#### 장점

- 메인 스레드는 계속 새로운 연결을 수락 가능
- 각 클라이언트는 독립적으로 처리됨
- I/O 대기 시간 동안 다른 클라이언트 처리 가능

---

### 2. 웹 기반 GUI 클라이언트 선택

#### 선택 이유

- **크로스 플랫폼**: 브라우저만 있으면 어디서든 실행 가능
- **사용 편의성**: GUI로 직관적인 요청 전송
- **실시간 확인**: 요청/응답을 즉시 확인 가능
- **macOS GUI 문제 해결**: Tkinter의 macOS 호환성 문제 회피

#### 구현 방식

- **Flask**: 경량 웹 프레임워크
- **AJAX**: 비동기 HTTP 요청 전송
- **Bootstrap**: 반응형 UI 디자인

#### 기능

- 모든 HTTP 메소드 지원 (GET, POST, PUT, DELETE, PATCH, HEAD)
- Host/Port 설정 가능
- JSON 바디 입력
- 요청/응답 실시간 표시

---

### 3. 0.0.0.0 네트워크 바인딩

#### 선택 이유

- **외부 접속 허용**: 다른 컴퓨터에서 서버 테스트 가능
- **실제 네트워크 환경**: 로컬호스트가 아닌 실제 네트워크 통신 구현
- **Wireshark 캡처**: 네트워크 패킷 분석 가능

#### 구현 방식

```python
# HTTPConstants.py
SERVER_HOST = '0.0.0.0'  # 모든 네트워크 인터페이스
CLIENT_HOST = 'localhost'  # 클라이언트 기본값 (사용자가 변경 가능)

# Server.py
self.server_socket.bind(('0.0.0.0', 8080))
```

#### 보안 고려사항

- 프로덕션 환경에서는 방화벽 설정 필요
- 테스트 목적으로만 사용 권장

---

### 4. 딕셔너리 기반 데이터 구조

#### 선택 이유

- **성능**: O(1) 검색/삽입/삭제 (리스트는 O(n))
- **효율성**: ID로 직접 접근 가능
- **확장성**: 데이터가 많아져도 성능 유지

#### 구현 방식

```json
{
  "users": {
    "1": {"id": 1, "name": "Alice", "email": "alice@example.com"},
    "2": {"id": 2, "name": "Bob", "email": "bob@example.com"}
  },
  "next_id": 3
}
```

#### 성능 비교

| 작업 | 리스트 | 딕셔너리 |
|------|--------|----------|
| ID로 검색 | O(n) | O(1) |
| 삽입 | O(1) | O(1) |
| 삭제 | O(n) | O(1) |

---

### 5. 정적 파일 자동 서빙

#### 선택 이유

- **유지보수성**: 파일 추가 시 코드 수정 불필요
- **확장성**: HTML, CSS, JS, 이미지 등 자동 지원
- **Content-Type 자동 감지**: 파일 확장자로 MIME 타입 결정

#### 구현 방식

```python
# HTTPHandler.py
def handle_GET(self, path):
    # 루트 경로 → index.html
    if path == '/':
        path = '/index.html'
    
    # 확장자 없으면 .html 추가
    if not '.' in path:
        path = path + '.html'
    
    # 파일 시스템에서 찾기
    file_path = os.path.join(self.static_dir, path.lstrip('/'))
    
    if os.path.exists(file_path):
        content_type = self._get_content_type(file_path)
        # 파일 읽고 반환
```

---

## 🦈 Wireshark 패킷 캡처

### 캡처 방법

1. **Wireshark 실행**:
   ```bash
   open -a Wireshark
   ```

2. **인터페이스 선택**:
   - 같은 컴퓨터: **Loopback: lo0**
   - 다른 컴퓨터: **Wi-Fi: en0** 또는 **Ethernet: en1**

3. **필터 설정**:
   ```
   tcp.port == 8080
   ```

4. **캡처 시작** → 요청 전송 → **캡처 중지**

### 분석 방법

- **Follow TCP Stream**: 우클릭 → Follow → TCP Stream
- **HTTP 필터**: `http` 입력
- **특정 메소드**: `http.request.method == "POST"`

자세한 내용은 `WIRESHARK_GUIDE.md` 참조

---

## 📊 테스트 결과

### 기능 테스트

| 메소드 | 경로 | 상태 코드 | 결과 |
|--------|------|-----------|------|
| GET | / | 200 | ✅ 성공 |
| GET | /about | 200 | ✅ 성공 |
| GET | /users | 200 | ✅ 성공 |
| GET | /notfound | 404 | ✅ 성공 |
| HEAD | / | 200 | ✅ 성공 |
| POST | /users | 201 | ✅ 성공 |
| POST | /users (잘못된 JSON) | 400 | ✅ 성공 |
| PUT | /users/1 | 200 | ✅ 성공 |
| PUT | /users/999 | 404 | ✅ 성공 |
| PATCH | /users/1 | 200 | ✅ 성공 |
| DELETE | /users/1 | 200 | ✅ 성공 |
| DELETE | /users/999 | 404 | ✅ 성공 |

### 멀티스레딩 테스트

- **동시 접속**: 10개 클라이언트 동시 접속 → ✅ 성공
- **응답 시간**: 평균 < 100ms
- **안정성**: 장시간 실행 → 메모리 누수 없음

### 네트워크 간 테스트

- **같은 Wi-Fi**: 다른 노트북에서 접속 → ✅ 성공
- **IP 주소**: 172.30.1.59:8080 → ✅ 접속 가능
- **Wireshark 캡처**: 네트워크 패킷 확인 → ✅ 성공

---

## 🔍 문제 해결 및 개선 사항

### 1. 파일 경로 문제

**문제**: 상대 경로 사용으로 인한 `FileNotFoundError`

**해결**:
```python
# HTTPHandler.py
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')
```

### 2. DNS 조회 실패

**문제**: 클라이언트가 `0.0.0.0`으로 접속 시도

**해결**:
```python
# HTTPConstants.py
SERVER_HOST = '0.0.0.0'  # 서버용
CLIENT_HOST = 'localhost'  # 클라이언트용
```

### 3. 정적 파일 코드 중복

**문제**: 파일마다 if-elif 블록 필요

**해결**: 파일 시스템 기반 자동 라우팅 구현

---

## 📚 참고 자료

- [HTTP/1.1 RFC 2616](https://www.rfc-editor.org/rfc/rfc2616)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Wireshark User Guide](https://www.wireshark.org/docs/)

---

## 👨‍💻 개발자 정보

- **프로젝트명**: HTTP 소켓 프로그래밍
- **개발 기간**: 2026년 1월
- **개발 환경**: macOS, Python 3.x
- **버전**: 1.0

---

## 📝 라이선스

본 프로젝트는 교육 목적으로 개발되었습니다.
