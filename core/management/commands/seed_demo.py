from decimal import Decimal

from django.core.management.base import BaseCommand
from contacts.models import ContactMessage
from core.models import Banner, SiteSetting
from pages.models import AboutPage
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed demo data for the auto parts catalog.'

    def handle(self, *args, **options):
        SiteSetting.objects.update_or_create(
            id=1,
            defaults={
                'site_name': 'AutoParts Việt',
                'hotline': '0901 234 567',
                'email': 'sales@autoparts.test',
                'address': '123 Nguyễn Văn Linh, Quận 7, TP.HCM',
                'facebook_url': 'https://facebook.com/',
                'zalo_url': 'https://zalo.me/0901234567',
            },
        )
        Banner.objects.update_or_create(
            title='Phụ tùng ô tô chính hãng',
            defaults={
                'subtitle': 'Lọc dầu, phanh, đèn, ắc quy và linh kiện bảo dưỡng cho gara và chủ xe.',
                'button_text': 'Xem sản phẩm',
                'button_url': '/san-pham/',
                'is_active': True,
                'sort_order': 1,
            },
        )
        about, _ = AboutPage.objects.update_or_create(
            id=1,
            defaults={
                'title': 'Đối tác phụ tùng đáng tin cậy',
                'content': 'Chúng tôi cung cấp phụ tùng ô tô chọn lọc cho gara, đại lý và khách hàng cá nhân. Danh mục sản phẩm rõ ràng, giá minh bạch và đội ngũ tư vấn sẵn sàng hỗ trợ chọn đúng mã phụ tùng.',
            },
        )

        category_tree = {
            ('Động cơ', 'dong-co'): [('Lọc dầu', 'loc-dau'), ('Bugi', 'bugi'), ('Dây curoa', 'day-curoa')],
            ('Hệ thống phanh', 'he-thong-phanh'): [('Bố thắng', 'bo-thang'), ('Đĩa phanh', 'dia-phanh'), ('Dầu phanh', 'dau-phanh')],
            ('Điện - đèn', 'dien-den'): [('Ắc quy', 'ac-quy'), ('Đèn pha', 'den-pha'), ('Cảm biến', 'cam-bien')],
            ('Chăm sóc xe', 'cham-soc-xe'): [('Dung dịch vệ sinh', 'dung-dich-ve-sinh'), ('Gạt mưa', 'gat-mua'), ('Phụ kiện', 'phu-kien')],
        }
        categories = {}
        for (parent_name, parent_slug), child_items in category_tree.items():
            parent, _ = Category.objects.update_or_create(
                slug=parent_slug,
                defaults={'name': parent_name, 'is_active': True},
            )
            categories[parent_name] = parent
            for child_name, child_slug in child_items:
                child, _ = Category.objects.update_or_create(
                    slug=child_slug,
                    defaults={'name': child_name, 'parent': parent, 'is_active': True},
                )
                categories[child_name] = child

        products = [
            ('Lọc dầu động cơ Bosch', 'AP-LOCD-001', 'Lọc dầu', 180000, 150000, True, 4.8),
            ('Bugi Iridium NGK', 'AP-BUGI-002', 'Bugi', 260000, None, True, 4.7),
            ('Dây curoa tổng hợp Mitsuboshi', 'AP-DAY-003', 'Dây curoa', 420000, 390000, False, 4.6),
            ('Bộ má phanh trước Bendix', 'AP-PHANH-004', 'Bố thắng', 850000, 790000, True, 4.9),
            ('Đĩa phanh trước OEM', 'AP-DIA-005', 'Đĩa phanh', 1250000, None, False, 4.5),
            ('Ắc quy khô 12V 60Ah', 'AP-AQ-006', 'Ắc quy', 1650000, 1520000, True, 4.8),
            ('Bóng đèn pha LED H4', 'AP-DEN-007', 'Đèn pha', 520000, 480000, False, 4.4),
            ('Cảm biến áp suất lốp', 'AP-CB-008', 'Cảm biến', 980000, None, False, 4.3),
            ('Gạt mưa silicon 24 inch', 'AP-GM-009', 'Gạt mưa', 220000, 190000, True, 4.7),
            ('Dung dịch vệ sinh kim phun', 'AP-DD-010', 'Dung dịch vệ sinh', 160000, None, False, 4.2),
            ('Dầu phanh DOT4', 'AP-DP-011', 'Dầu phanh', 145000, 120000, False, 4.5),
            ('Bộ phụ kiện cứu hộ mini', 'AP-PK-012', 'Phụ kiện', 350000, None, True, 4.6),
        ]
        for name, sku, category_name, price, sale_price, featured, rating in products:
            Product.objects.update_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'slug': sku.lower(),
                    'category': categories[category_name],
                    'price': Decimal(price),
                    'sale_price': Decimal(sale_price) if sale_price else None,
                    'rating': Decimal(str(rating)),
                    'short_description': 'Sản phẩm phụ tùng ô tô phổ biến, phù hợp nhiều dòng xe.',
                    'description': 'Thông tin chi tiết sản phẩm, thông số kỹ thuật và tư vấn lắp đặt có thể cập nhật trong Django Admin.',
                    'is_featured': featured,
                    'is_active': True,
                },
            )

        ContactMessage.objects.get_or_create(
            phone='0912345678',
            defaults={
                'full_name': 'Khách hàng demo',
                'email': 'demo@example.com',
                'message': 'Tôi cần tư vấn lọc dầu cho xe gia đình.',
            },
        )
        self.stdout.write(self.style.SUCCESS('Demo data is ready.'))
