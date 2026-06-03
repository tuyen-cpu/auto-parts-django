from django.db import models
from django.urls import reverse

from core.slug_utils import unique_slug


class AboutPage(models.Model):
    title = models.CharField('tiêu đề', max_length=180, default='Giới thiệu công ty')
    content = models.TextField('nội dung')
    image = models.ImageField('ảnh', upload_to='pages/', blank=True)
    updated_at = models.DateTimeField('cập nhật lúc', auto_now=True)

    class Meta:
        verbose_name = 'trang giới thiệu'
        verbose_name_plural = 'trang giới thiệu'

    def __str__(self):
        return self.title


class PromotionPage(models.Model):
    title = models.CharField('tiêu đề', max_length=180, default='Khuyến mãi')
    content = models.TextField('nội dung')
    image = models.ImageField('ảnh', upload_to='pages/promotions/', blank=True)
    updated_at = models.DateTimeField('cập nhật lúc', auto_now=True)

    class Meta:
        verbose_name = 'trang khuyến mãi'
        verbose_name_plural = 'trang khuyến mãi'

    def __str__(self):
        return self.title


class PromotionPost(models.Model):
    title = models.CharField('tiêu đề', max_length=180)
    slug = models.SlugField('slug', max_length=200, unique=True, blank=True)
    summary = models.CharField('mô tả ngắn', max_length=255, blank=True)
    content = models.TextField('nội dung')
    image = models.ImageField('ảnh', upload_to='promotions/', blank=True)
    is_active = models.BooleanField('hiển thị', default=True)
    sort_order = models.PositiveIntegerField('thứ tự', default=0)
    created_at = models.DateTimeField('ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('ngày cập nhật', auto_now=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = 'bài khuyến mãi'
        verbose_name_plural = 'bài khuyến mãi'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title, max_length=200, fallback='khuyen-mai')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('promotion_detail', kwargs={'slug': self.slug})

# Create your models here.
