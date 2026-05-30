from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField('họ tên', max_length=140)
    phone = models.CharField('số điện thoại', max_length=40)
    email = models.EmailField('email', blank=True)
    message = models.TextField('nội dung')
    created_at = models.DateTimeField('ngày gửi', auto_now_add=True)
    is_read = models.BooleanField('đã đọc', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'liên hệ khách gửi'
        verbose_name_plural = 'liên hệ khách gửi'

    def __str__(self):
        return f'{self.full_name} - {self.phone}'

# Create your models here.
