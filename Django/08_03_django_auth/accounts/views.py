from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, render

from .forms import CustomUserChangeForm, CustomUserCreationForm


def login(request):
    # 인증된 사용자는 login 뷰함수를 사용하지 못하게 처리
    if request.user.is_authenticated:
        return redirect('articles:index')

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


@login_required
def logout(request):
    """
    [로그아웃] = 세션(Session)을 Delete 하는 로직
    - 로그인한 사용자만 접근 가능 (@login_required)
    """
    # 1. 서버의 세션 데이터 삭제 => request.user가 비로그인 사용자(AnonymousUser)로 바뀜
    #    - view 함수 이름(logout)과 겹치지 않도록 auth_logout으로 import
    auth_logout(request)
    return redirect('articles:index')


def signup(request):
    """
    [회원가입] = User 데이터를 Create 하는 로직
    - GET  : 빈 회원가입 form 페이지 응답
    - POST : 유효성 검사 후 User 저장
    """
    # 0. 이미 로그인한 사용자는 회원가입할 이유가 없으므로 메인 페이지로 돌려보냄
    if request.user.is_authenticated:
        return redirect('articles:index')

    # 1. POST 요청 => 회원가입 시도
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # 1-1. 유효성 검사 (아이디 중복, 비밀번호 일치/규칙 등)
        if form.is_valid():
            # 1-2. User 저장 (비밀번호는 암호화되어 저장됨)
            form.save()
            return redirect('articles:index')

    # 2. POST가 아닌 모든 요청 => 빈 회원가입 form 준비
    else:
        form = CustomUserCreationForm()

    # 3. GET 요청 / 유효성 검사 실패 POST 두 경우가 함께 사용
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    """
    [회원 탈퇴] = User 데이터를 Delete 하는 로직
    - 로그인한 사용자 '본인'만 탈퇴 가능
    """
    # 1. 현재 로그인한 유저 객체를 DB에서 삭제
    #    - request.user : 브라우저의 세션 쿠키를 보고 Django가 요청 객체에 넣어준 '로그인한 유저'
    request.user.delete()
    return redirect('articles:index')


@login_required
def update(request):
    """
    [회원 정보 수정] = User 데이터를 Update 하는 로직
    - 수정 대상은 항상 '현재 로그인한 사용자 본인'
      => URL로 pk를 받지 않고 request.user를 수정 대상으로 사용
      => pk를 받으면 주소만 바꿔서 남의 계정을 수정하는 문제가 생길 수 있음
    """
    # 1. POST 요청 => 수정 내용 저장
    if request.method == 'POST':
        # 1-1. 새 입력값 + 수정 대상(request.user)을 함께 전달
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    # 2. POST가 아닌 모든 요청 => 기존 회원 정보가 채워진 form 준비
    else:
        form = CustomUserChangeForm(instance=request.user)

    # 3. GET 요청 / 유효성 검사 실패 POST 두 경우가 함께 사용
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def password(request):
    """
    [비밀번호 변경]
    - 로그인한 사용자 본인의 비밀번호만 변경 가능
    """
    # 1. POST 요청 => 비밀번호 변경 시도
    if request.method == 'POST':
        # 1-1. PasswordChangeForm은 첫 번째 인자로 user를 받음
        #      - 일반 Form의 첫 번째 인자는 data
        #      - 기존 비밀번호가 맞는지 확인하려면 '누구의' 비밀번호인지 알아야 하기 때문
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # 1-2. 새 비밀번호 저장 (변경된 유저 객체 반환)
            user = form.save()
            # 1-3. 세션 정보 갱신
            #      - 비밀번호가 바뀌면 기존 세션이 무효화되어 자동 로그아웃됨
            #      - 이 함수로 현재 세션을 새 비밀번호 기준으로 갱신해 로그인 상태 유지
            update_session_auth_hash(request, user)
            return redirect('articles:index')

    # 2. POST가 아닌 모든 요청 => 빈 비밀번호 변경 form 준비
    else:
        form = PasswordChangeForm(request.user)

    # 3. GET 요청 / 유효성 검사 실패 POST 두 경우가 함께 사용
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)
