from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField('tên website', max_length=160, default='AutoParts')
    slogan = models.CharField('slogan', max_length=180, blank=True, default='Phụ tùng chính hãng - Đồng hành mọi hành trình')
    logo = models.ImageField('logo', upload_to='site/', blank=True)
    hotline = models.CharField('hotline', max_length=40, blank=True)
    email = models.EmailField('email', blank=True)
    address = models.CharField('địa chỉ', max_length=255, blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    zalo_url = models.URLField('Zalo', blank=True)
    tiktok_url = models.URLField('TikTok', blank=True)
    google_business_url = models.URLField('Google Business Profile', blank=True)
    seo_description = models.CharField('SEO description mac dinh', max_length=255, blank=True)
    google_map_iframe = models.TextField('Google Maps iframe', blank=True)

    class Meta:
        verbose_name = 'cấu hình website'
        verbose_name_plural = 'cấu hình website'

    def __str__(self):
        return self.site_name


class Banner(models.Model):
    eyebrow = models.CharField('dòng giới thiệu nhỏ', max_length=120, blank=True)
    title = models.CharField('tiêu đề', max_length=180)
    subtitle = models.CharField('mô tả ngắn', max_length=255, blank=True)
    image = models.ImageField('ảnh banner', upload_to='banners/', blank=True)
    button_text = models.CharField('chữ nút', max_length=80, blank=True)
    button_url = models.CharField('đường dẫn nút', max_length=255, blank=True)
    is_active = models.BooleanField('hiển thị', default=True)
    sort_order = models.PositiveIntegerField('thứ tự', default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'banner'
        verbose_name_plural = 'banner'

    def __str__(self):
        return self.title

# Create your models here.
