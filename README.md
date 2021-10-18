# 🎆 H&M Clone Project
- 합리적인 가격, 패션 & 퀄리티 의류 - H&M 사이트 클론
- 프론트엔드와 백엔드가 각자의 기술 구현에 초점을 두고 
  원들 각자가 원하는 기능이나 페이지를 역할 분담하여 진행하였고 애자일한 스크럼 방식으로 구현하기 위해 노력했습니다 


## 👩‍👩‍👧‍👦 팀 소개
- 팀명 : HandWash 
- 개발 기간 : 2021.10.05 ~ 2021.10.15
- 개발 인원
  - [FrontEnd](https://github.com/xodid157/25-1st-HandWash-frontend) 4명 : [전태양](), [신혜리](), [서동혁](), [조윤희]()
  - [BackEnd](https://github.com/wecode-bootcamp-korea/25-1st-HandWash-backend) 2명 : [이다빈](), [김민호]()

## 🎬 프로젝트 구현 영상(사진 클릭시 유투브 링크로 연결)
[![](https://user-images.githubusercontent.com/80348575/137651483-3af5a602-d906-44fb-b416-074c43ad0b7b.gif)](https://youtu.be/tvOq2XdUw_M)

## ⚙️ 적용기술
- FrontEnd : React, Html5, Css3
- BackEnd : Python@3.8.11, Django@3.2.8, PostgreSQL@14.0, JWT, bcrypt
- Communication : Git, GitHub, Trello, Slack, Notion

## 💾 데이터베이스 
![Untitled (3)](https://user-images.githubusercontent.com/80348575/137650648-fe50bc9e-2ed6-4cc9-abfb-8253c3ba3013.png)


## 📒 구현기능

### Front-end

#### 전태양
- 상품 상세 페이지 레이아웃 구현
- 조건부 랜더링을 사용해 버튼 클릭시 모달창 나오도록 구현
- 하트(좋아요) 기능 구현 및 즐겨찾기로 데이터 보내기 구현
- 즐겨찾기 페이지 레이아웃 구현
- 즐겨찾기에서 사이즈를 선택해 장바구니로 보내기 구현
- 쓰레기통 아이콘 클릭시 즐겨찾기 데이터 베이스에서 지워지게 구현
#### 신혜리

#### 서동혁
- 로그인, 회원가입 페이지 레이아웃 구현
- 조건부 렌더링을 통해 회원정보 추가 창 구현
- 장바구니 페이지 레이아웃 구현
- 즐겨찾기에서 받은 제품을 리스트로 구현
#### 조윤희

### Back-end

## 공통
- modeling
- CSV 파일 샘플 데이터 작성

#### 이다빈
- CSV데이터 백업용 db_uploader.py 작성
- 카테고리별 상품 나열
- Query String으로 들어온 상품 조건 별 필터링 & 정렬
- 제품 상세 페이지
- 장바구니 제품 등록, 조회, 업데이트, 삭제

#### 김민호
- bcrypt를 사용한 회원가입 기능
- JWT를 사용한 로그인 기능
- decorator를 통한 로그인 유효성 검사 기능
- 로그인한 유저의 즐겨찾기 상품 추가, 제거, 조회 기능


## ⌨️ EndPoint
- SignUpView : `POST` /users/signup
- SignInView : `POST` /users/signin
- CategoryView : `GET` /products/categories
- ProductListView : `GET` /products/
- ProductDetailView : `GET` /products/<int:product_id>
- LikeView : `POST`, `GET` /likes/like
- CartView : `POST`, `GET` /carts
- CartView : `PATCH`, `DELETE` /carts?<int:cart_id>




## ❗️ Reference
- 이 프로젝트는 [H&M](https://www2.hm.com/ko_kr/index.html) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
