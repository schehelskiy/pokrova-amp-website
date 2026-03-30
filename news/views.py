from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category

def news_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()

    if category_slug:
        # Шукаємо новини, які мають обрану категорію серед свого списку categories
        news = Post.objects.filter(is_published=True, categories__slug=category_slug).distinct().order_by('-created_at')
    else:
        news = Post.objects.filter(is_published=True).order_by('-created_at')

    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug
    }
    return render(request, 'news_list.html', context)

def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_text = request.POST.get('user_comment')
            if comment_text:
                Comment.objects.create(post=post, user=request.user, text=comment_text)
                return redirect('news_detail', pk=pk)
        else:
            return redirect('login')

    comments = post.comments.all().order_by('-created_at')
    return render(request, 'news_detail.html', {'post': post, 'comments': comments})