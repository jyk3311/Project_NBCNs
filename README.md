# 🎁 NBCN (Newbie Coding News)

NBCN(Newbie Coding News)은 IT 산업의 초보자들을 위한 **뉴스 및 커뮤니티 플랫폼**입니다. 이 프로젝트는 Django와 Django REST Framework(DRF)를 기반으로 구현되었으며, 사용자는 크롤링된 IT 관련 뉴스를 확인하고, AI 요약본을 통해 뉴스를 빠르게 파악할 수 있습니다. 또한 사용자 등급에 따라 질문 게시판, 자유 게시판, 홍보 게시판에 게시글을 작성하고 댓글을 달 수 있습니다.

---

## 🌟 주요 기능

- **회원가입 및 로그인**: JWT 기반 인증 시스템을 사용하여 사용자 관리.
- **프로필 관리**: 회원 프로필 조회 및 수정.
- **NBCN 뉴스**: AI가 크롤링된 뉴스를 요약하여 제공하며, 북마크 기능으로 뉴스를 저장.
- **게시판 시스템**: 자유, 질문, 홍보 게시판 제공 및 좋아요/북마크 기능.
- **댓글 및 좋아요**: 게시글에 대한 댓글 작성 및 좋아요 기능.
- **사용자 역할 관리**: 관리자, 마스터, 일반 사용자(뉴비)로 역할에 따른 권한 부여.

---

## 🛠️ 설치 방법

### 1️⃣ 저장소 클론

```bash
git clone https://github.com/strongdambi/spartanews11.git
cd NBCN
```

### 2️⃣ 가상 환경 설정 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Mac
source venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3️⃣ 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 4️⃣ 슈퍼유저 생성 (관리자 계정)

```bash
python manage.py createsuperuser
```

### 5️⃣ 개발 서버 실행

```bash
python manage.py runserver
```

---

## 🖇️ 와이어 프레임



---

## 📋 API 사용법

자세한 API 명세서는 [Postman API Documentation](https://documenter.getpostman.com/view/37990286/2sAXqs6Miq)에서 확인할 수 있습니다.

| 기능                    | HTTP 메서드 | 엔드포인트                                   | 설명                                      |
|-------------------------|-------------|---------------------------------------------|-------------------------------------------|
| **회원가입**            | POST        | `/api/v1/accounts/`                            | 사용자 정보를 입력해 회원가입 후 JWT 토큰 발급   |
| **회원 탈퇴**           | DELETE      | `/api/v1/accounts/`                            | 회원 탈퇴 (소프트 삭제)                         |
| **로그인**              | POST        | `/api/v1/accounts/login/`                      | 유저네임, 비밀번호로 로그인 후 JWT 토큰 발급     |
| **로그아웃**             | POST        | `/api/v1/accounts/logout/`                    | 소프트 삭제로 is_active 계정 비활성화           |
| **프로필 조회 및 수정**  | GET/POST     | `/api/v1/accounts/<str:username>/`           | 로그인한 사용자의 정보(북마크, 작성글 포함)를 조회|
| **게시글 목록 조회**     | GET         | `/api/v1/articles/(free/ask/company)/`        | 자유, 질문, 홍보 게시글 목록 조회                |
| **게시글 작성**         | POST        | `/api/v1/articles/`                            | 새로운 게시글 작성                              |
| **게시글 수정**         | PUT         | `/api/v1/articles/<int:pk>/`                   | 기존 게시글 수정                                |
| **게시글 삭제**         | DELETE      | `/api/v1/articles/<int:pk>/`                   | 게시글 삭제                                     |
| **게시글 좋아요**        | POST        | `/api/v1/articles/<int:pk>/like/`             | 게시글에 좋아요 추가/취소                        |
| **게시글 북마크**        | POST        | `/api/v1/articles/<int:pk>/bookmark/`         | 게시글을 북마크에 추가/제거                      |
| **뉴스 목록 조회**       | GET         | `/api/v1/nbcns/`                              | 크롤링된 뉴스 목록을 조회                        |
| **뉴스 생성**            | POST        | `/api/v1/nbcns/`                              | 새로운 뉴스 생성                                |
| **뉴스 상세 조회**       | GET        | `/api/v1/nbcns/<int:pk>/`                      | 선택한 뉴스 조회                                |
| **뉴스 삭제**          | DELETE       | `/api/v1/nbcns/<int:pk>/`                      | 선택한 뉴스 삭제                                |
| **뉴스 북마크**         | POST        | `/api/v1/nbcns/<int:pk>/bookmark/`             | 뉴스 북마크 추가/취소                           |
| **댓글 목록 조회**       | GET         | `/api/v1/articles/<int:pk>/comments/`         | 특정 게시글의 댓글 목록 조회                     |
| **댓글 작성**           | POST        | `/api/v1/articles/<int:pk>/comments/`          | 특정 게시글에 댓글 작성                         |
| **댓글 수정**           | PUT         | `/api/v1/comments/<int:pk>/`                   | 댓글 수정                                      |
| **댓글 삭제**           | DELETE      | `/api/v1/comments/<int:pk>/`                   | 댓글 삭제 (소프트 삭제)                         |

---

## 🖼️ ERD (Entity Relationship Diagram)

### ERD 이미지

![image (4)](https://github.com/user-attachments/assets/fb7fac6c-7069-4e67-a640-f62449ea8c3b)

### ERD 설명

- **User 모델**: 사용자는 게시글을 작성하고, 댓글을 남길 수 있으며, 좋아요 기능을 이용할 수 있고, 뉴스 및 게시글을 북마크할 수 있습니다.
- **Article 모델**: 게시글은 자유, 질문, 홍보 게시판으로 분류되며, 댓글 및 좋아요 기능을 제공합니다.
- **NBCN 모델**: 뉴스는 사용자에 의해 북마크될 수 있으며, AI가 요약한 콘텐츠가 제공됩니다.
- **Comment 모델**: 댓글은 특정 게시글과 연관되며, 사용자에 의해 작성됩니다.

---

## 🔑 역할 기반 접근 제어

- **관리자**: 모든 기능(뉴스 생성, 삭제, 게시글 관리)에 접근할 수 있습니다.
- **마스터**: 홍보 게시판에 글을 작성할 수 있습니다.
- **일반 사용자 (뉴비)**: 질문 및 자유 게시판에 글을 작성할 수 있습니다.

---

## 🛠️ 데이터베이스 관리

이 프로젝트는 **SQLite3**을 기본 데이터베이스로 사용합니다.

---

## 🌍 시스템 아키텍처

### 백엔드 구성

- **Django REST Framework**: API 설계를 위한 프레임워크.
- **SQLite3**: 데이터베이스 관리.
- **BeautifulSoup**: 뉴스 크롤링을 위한 라이브러리.
- **JWT**: 토큰 방식의 사용자 인증 시스템.

---

## 🛠️ 통합 및 인터페이스

- **크롤링 통합**: BeautifulSoup을 사용하여 IT 관련 뉴스 데이터를 주기적으로 크롤링합니다.
- **REST API**: JSON 형식으로 데이터를 주고받으며, Postman을 사용해 API를 문서화합니다.

---

## 🔐 보안

- **HTTPS 사용**: 모든 API 요청은 HTTPS를 통해 암호화되어 전송됩니다.
- **JWT 인증**: 사용자는 JWT 토큰을 통해 인증되며, 권한 관리가 이루어집니다.
- **비밀번호 암호화**: 사용자의 비밀번호는 해시화되어 안전하게 저장됩니다.
- **역할 기반 권한 관리**: 관리자만 뉴스 크롤링 및 관리 기능을 사용할 수 있습니다.

---
