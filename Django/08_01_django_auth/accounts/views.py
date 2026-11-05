from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def login(request):
    """
    [로그인] = 세션(Session)을 Create 하는 로직
    - GET  : 로그인 form 페이지 응답
    - POST : ID/PW 확인(인증) 후 세션 생성
    """
    # 1. POST 요청 => 로그인 시도
    if request.method == 'POST':
        # 1-1. 사용자 입력(ID/PW)을 AuthenticationForm에 담기
        #      - 일반 Form/ModelForm은 첫 번째 인자가 data(request.POST)
        #      - AuthenticationForm은 예외적으로 request를 첫 번째로 받음
        #        => 인증 과정에서 요청 정보가 필요하기 때문 (생성자를 재정의함)
        form = AuthenticationForm(request, request.POST)

        # 1-2. 유효성 검사 = 인증
        #      - 입력한 ID/PW가 DB의 유저 정보와 일치하는지 확인
        if form.is_valid():
            # 1-3. 인증에 성공한 유저 객체 꺼내기
            #      - get_user() : AuthenticationForm이 제공하는 메서드
            user = form.get_user()

            # 1-4. 세션 생성 (실제 '로그인'이 일어나는 순간)
            #      - auth_login(요청 객체, 인증된 유저 객체)
            #      - 서버 DB에 세션 데이터 저장 + 브라우저에 sessionid 쿠키 발급
            #      - view 함수 이름(login)과 겹치지 않도록 auth_login으로 import
            auth_login(request, user)
            return redirect('articles:index')
        # 1-5. 인증 실패 시 => 아래 render로 이동
        #      (form에 "아이디 또는 비밀번호가 올바르지 않음" 에러 메시지가 담김)

    # 2. POST가 아닌 모든 요청 => 빈 로그인 form 준비
    else:
        form = AuthenticationForm()

    # 3. GET 요청 / 인증 실패 POST 두 경우가 함께 사용
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
