from django.shortcuts import get_object_or_404, render

from .models import AboutPage, PromotionPost


def about(request):
    page = AboutPage.objects.first()
    return render(request, 'about.html', {'page': page})


def promotion(request):
    posts = PromotionPost.objects.filter(is_active=True)
    return render(request, 'promotion.html', {'posts': posts})


def promotion_detail(request, slug):
    post = get_object_or_404(PromotionPost, slug=slug, is_active=True)
    return render(request, 'promotion_detail.html', {'post': post})

# Create your views here.
