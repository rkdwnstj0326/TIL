from django.shortcuts import redirect, render

from .forms import ArticleForm
from .models import Article


# Create your views here.
def index(request):
    """
    [메인 페이지]
    - 메인 페이지에는 전체 게시글 목록이 출력됨
    - 따라서 DB에서 전체 게시글을 가져와야 함
    - CRUD 중 READ : 전체 게시글 조회
    """
    # 1. DB에서 전체 게시글 조회
    #    - Article.objects.all() 의 결과는 QuerySet (게시글 객체들의 묶음)
    articles = Article.objects.all()

    # 2. 템플릿에 넘겨줄 데이터를 딕셔너리로 묶기
    #    - key('articles') => 템플릿에서 사용할 변수 이름
    #    - value(articles) => 실제로 전달되는 데이터
    context = {
        'articles': articles,
    }

    # 3. 템플릿(index.html)에 데이터(context)를 채워 HTML을 만들고, 응답으로 반환
    return render(request, 'articles/index.html', context)


def detail(request, article_pk):
    """
    [단일 게시글 조회]
    - URL에서 넘겨받은 article_pk로 몇 번 게시글을 볼지 결정
    - DB에서 해당 게시글 1개를 조회한 뒤 템플릿에 전달
    - CRUD 중 READ : 단일 게시글 조회
    """
    # 1. pk가 article_pk인 게시글 1개 조회
    #    - get()의 결과는 QuerySet이 아닌 Article 객체 1개
    article = Article.objects.get(pk=article_pk)

    # 2. 템플릿에 넘겨줄 데이터를 딕셔너리로 묶기
    context = {
        'article': article,
    }

    # 3. 템플릿(detail.html)에 데이터를 채워 HTML을 만들고, 응답으로 반환
    return render(request, 'articles/detail.html', context)


def create(request):
    """
    [게시글 작성 페이지 + 저장] - 기존 new와 create를 하나로 통합
    - GET  : 빈 form 페이지 응답 (기존 new 역할)
    - POST : 유효성 검사 후 DB 저장 (기존 create 역할)
    - CRUD 중 CREATE
    """
    # 1. POST 요청 => 데이터를 저장하려는 요청
    if request.method == 'POST':
        # 1-1. 사용자 입력 데이터를 ArticleForm에 담기
        form = ArticleForm(request.POST)
        # 1-2. 유효성 검사 통과 시에만 저장 후 상세 페이지로 redirect
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
        # 1-3. 유효성 검사 실패 시 => if 블록을 빠져나가 아래 render로 이동
        #      (form에는 입력값 + 에러 메시지가 담겨 있음)

    # 2. POST가 아닌 모든 요청 => 빈 form 준비 (기존 new 역할)
    else:
        # [왜 'GET이면?'이 아니라 'POST면?'을 먼저 확인할까?]
        # - DB를 변경하는 중요한 작업(저장)은 POST일 때만 확실하게 실행
        # - 그 외의 요청은 무엇이 오든 '페이지 보여주기'만 하므로 안전
        form = ArticleForm()

    # 3. 아래 render는 두 가지 경우가 함께 사용
    #    - GET 요청             => 빈 form
    #    - 유효성 검사 실패 POST => 입력값 + 에러 메시지가 담긴 form
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def delete(request, article_pk):
    """
    [게시글 삭제]
    - 삭제할 게시글을 먼저 조회한 뒤 삭제
    - CRUD 중 DELETE
    """
    # 1. 삭제할 게시글 조회
    article = Article.objects.get(pk=article_pk)

    # 2. DB에서 삭제
    article.delete()

    # 3. 삭제된 글의 상세 페이지는 더 이상 없으므로 메인 페이지로 redirect
    return redirect('articles:index')


def update(request, article_pk):
    """
    [게시글 수정 페이지 + 수정 저장] - 기존 edit과 update를 하나로 통합
    - GET  : 기존 값이 채워진 form 페이지 응답 (기존 edit 역할)
    - POST : 유효성 검사 후 DB 갱신 (기존 update 역할)
    - CRUD 중 UPDATE
    """
    # 0. 수정할 게시글 조회
    #    - GET/POST 모두 수정 대상이 필요하므로 if문보다 먼저 조회
    article = Article.objects.get(pk=article_pk)

    # 1. POST 요청 => 수정 내용을 저장하려는 요청
    if request.method == 'POST':
        # 1-1. 새로 입력된 값 + 수정 대상(instance)을 함께 전달
        form = ArticleForm(request.POST, instance=article)
        # 1-2. 유효성 검사 통과 시 갱신 후 상세 페이지로 redirect
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
        # 1-3. 유효성 검사 실패 시 => 아래 render로 이동

    # 2. POST가 아닌 모든 요청 => 기존 값이 채워진 form 준비 (기존 edit 역할)
    else:
        form = ArticleForm(instance=article)

    # 3. 아래 render는 두 가지 경우가 함께 사용
    #    - GET 요청             => 기존 값이 채워진 form
    #    - 유효성 검사 실패 POST => 수정 중이던 입력값 + 에러 메시지가 담긴 form
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)
