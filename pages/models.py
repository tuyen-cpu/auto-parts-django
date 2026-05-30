from django.db import models


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

# Create your models here.
