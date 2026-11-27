from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
    require_POST,
)
from django.contrib.auth.decorators import login_required

from .models import Book, Category, Thread, Comment
from .forms import ThreadForm, CommentForm
from .recommendations import recommend_books
from .utils import (
    generate_image_with_openai,
)


# Index 페이지
def books_in_category(category):
    books = Book.objects.order_by('pk')
    if category:
        books = books.filter(category__name=category)
    return books


@require_safe
def index(request):
    return render(request, 'books/index.html', {
        'categories': Category.objects.order_by('pk'),
        'books': books_in_category(request.GET.get('category')),
    })

# 장르별 필터링
@require_safe
def filter_category(request):
    books = books_in_category(request.GET.get('category'))
    return JsonResponse({'html': render_to_string('books/_book_list.html', {'books': books})})


@require_safe
def detail(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    context = {
        "book": book,
    }
    return render(request, "books/detail.html", context)


@require_POST
def recommendations(request, book_pk):
    book = get_object_or_404(Book.objects.select_related('category'), pk=book_pk)
    books, used_ai = recommend_books(book)
    html = render_to_string('books/_recommendations.html', {'books': books, 'used_ai': used_ai})
    return JsonResponse({'html': html})


@login_required
@require_http_methods(["GET", "POST"])
def thread_create(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.book = book
            thread.user = request.user
            thread.save()

            generated_image_path = generate_image_with_openai(thread.title, thread.content, book.title, book.author)
            if generated_image_path:
                thread.cover_img = generated_image_path
                thread.save()
                
            return redirect("books:thread_detail", book.pk, thread.pk)
    else:
        form = ThreadForm()
    context = {
        "form": form,
        "book": book,
    }
    return render(request, "books/thread_create.html", context)


@login_required
@require_safe
def thread_detail(request, book_pk, thread_pk):
    book = Book.objects.get(pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk, book=book)
    comment_form = CommentForm()
    context = {
        "book" : book,
        "thread": thread,
        "comment_form" : comment_form,
        "is_liked": thread.likes.filter(pk=request.user.pk).exists(),
    }
    return render(request, "books/thread_detail.html", context)



@login_required
@require_http_methods(["GET", "POST"])
def thread_update(request, book_pk, thread_pk):
    book = Book.objects.get(pk=book_pk)
    thread = Thread.objects.get(pk=thread_pk)
    comment_form = CommentForm(request.POST)
    if thread.user == request.user:
        if request.method == "POST":
            form = ThreadForm(request.POST, request.FILES, instance=thread)
            if form.is_valid():
                form.save()  
                return redirect('books:thread_detail', book_pk=book.pk, thread_pk=thread.pk)
        else:
            form = ThreadForm(instance=thread)
    else :
        return redirect('books:index') 
    context = {
        "form": form,
        "book": book,
        "comment_form" : comment_form,
    }
    return render(request, "books/thread_update.html", context)


@login_required
@require_POST
def thread_delete(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    if thread.user == request.user:
        thread.delete()
    return redirect("books:detail", book_pk)


# 쓰레드 좋아요 비동기 처리
@require_POST
def likes(request, book_pk, thread_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인해 주세요.'}, status=403)
    thread = get_object_or_404(Thread, pk=thread_pk, book_id=book_pk)
    is_liked = request.POST.get('active') == 'true'
    if is_liked:
        thread.likes.add(request.user)
    else:
        thread.likes.remove(request.user)
    return JsonResponse({'active': is_liked, 'count': thread.likes.count()})

# 쓰레드 댓글 비동기 처리
@require_POST
def create_comment(request, book_pk, thread_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인해 주세요.'}, status=403)
    thread = get_object_or_404(Thread, pk=thread_pk, book_id=book_pk)
    form = CommentForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': '댓글 내용을 1자 이상 100자 이하로 입력해 주세요.'}, status=400)
    comment = form.save(commit=False)
    comment.thread = thread
    comment.user = request.user
    comment.save()
    html = render_to_string('books/_comment.html', {'book': thread.book, 'comment': comment}, request=request)
    return JsonResponse({'html': html}, status=201)

@require_POST
def delete_comment(request, book_pk, comment_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인해 주세요.'}, status=403)
    comment = get_object_or_404(Comment, pk=comment_pk, thread__book_id=book_pk)
    if comment.user_id != request.user.pk:
        return JsonResponse({'error': '본인이 작성한 댓글만 삭제할 수 있습니다.'}, status=403)
    comment.delete()
    return JsonResponse({'deleted': comment_pk})
