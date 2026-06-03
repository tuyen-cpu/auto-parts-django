from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('tên danh mục', max_length=140)
    slug = models.SlugField('slug', max_length=160, unique=True)
    description = models.TextField('mo ta SEO/danh muc', blank=True)
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.CharField('SEO description', max_length=255, blank=True)
    parent = models.ForeignKey(
        'self',
        verbose_name='danh mục cha',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField('ảnh/icon', upload_to='categories/', blank=True)
    is_active = models.BooleanField('hiển thị', default=True)
    sort_order = models.PositiveIntegerField('thứ tự', default=0)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'danh mục'
        verbose_name_plural = 'danh mục'

    def __str__(self):
        return f'{self.parent.name} / {self.name}' if self.parent else self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField('tên sản phẩm', max_length=180)
    slug = models.SlugField('slug', max_length=200, unique=True)
    sku = models.CharField('mã sản phẩm/SKU', max_length=80, unique=True)
    category = models.ForeignKey(Category, verbose_name='danh mục', related_name='products', on_delete=models.PROTECT)
    image = models.ImageField('ảnh sản phẩm', upload_to='products/', blank=True)
    price = models.DecimalField('giá', max_digits=12, decimal_places=0, null=True, blank=True)
    sale_price = models.DecimalField('giá khuyến mãi', max_digits=12, decimal_places=0, null=True, blank=True)
    rating = models.DecimalField('rating', max_digits=2, decimal_places=1, null=True, blank=True)
    short_description = models.CharField('mô tả ngắn', max_length=255, blank=True)
    description = models.TextField('mô tả', blank=True)
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.CharField('SEO description', max_length=255, blank=True)
    is_featured = models.BooleanField('sản phẩm nổi bật', default=False)
    is_active = models.BooleanField('hiển thị', default=True)
    created_at = models.DateTimeField('ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('ngày cập nhật', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'sản phẩm'
        verbose_name_plural = 'sản phẩm'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def display_price(self):
        return self.sale_price or self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='sản phẩm', related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField('ảnh sản phẩm', upload_to='products/gallery/')
    alt_text = models.CharField('mô tả ảnh', max_length=180, blank=True)
    sort_order = models.PositiveIntegerField('thứ tự', default=0)
    created_at = models.DateTimeField('ngày tạo', auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'ảnh sản phẩm'
        verbose_name_plural = 'ảnh sản phẩm'

    def __str__(self):
        return self.alt_text or f'Ảnh {self.product.name}'

# Create your models here.
