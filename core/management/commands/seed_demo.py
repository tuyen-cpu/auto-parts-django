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
                'site_name': 'AutoParts Viá»‡t',
                'hotline': '0901 234 567',
                'email': 'sales@autoparts.test',
                'address': '123 Nguyá»…n VÄƒn Linh, Quáº­n 7, TP.HCM',
                'facebook_url': 'https://facebook.com/',
                'zalo_url': 'https://zalo.me/0901234567',
                'tiktok_url': 'https://www.tiktok.com/',
            },
        )
        Banner.objects.update_or_create(
            title='Phá»¥ tÃ¹ng Ã´ tÃ´ chÃ­nh hÃ£ng',
            defaults={
                'subtitle': 'Lá»c dáº§u, phanh, Ä‘Ã¨n, áº¯c quy vÃ  linh kiá»‡n báº£o dÆ°á»¡ng cho gara vÃ  chá»§ xe.',
                'button_text': 'Xem sáº£n pháº©m',
                'button_url': '/san-pham/',
                'is_active': True,
                'sort_order': 1,
            },
        )
        about, _ = AboutPage.objects.update_or_create(
            id=1,
            defaults={
                'title': 'Giới thiệu',
                'content': 'ChÃºng tÃ´i cung cáº¥p phá»¥ tÃ¹ng Ã´ tÃ´ chá»n lá»c cho gara, Ä‘áº¡i lÃ½ vÃ  khÃ¡ch hÃ ng cÃ¡ nhÃ¢n. Danh má»¥c sáº£n pháº©m rÃµ rÃ ng, giÃ¡ minh báº¡ch vÃ  Ä‘á»™i ngÅ© tÆ° váº¥n sáºµn sÃ ng há»— trá»£ chá»n Ä‘Ãºng mÃ£ phá»¥ tÃ¹ng.',
            },
        )

        category_tree = {
            ('Äá»™ng cÆ¡', 'dong-co'): [('Lá»c dáº§u', 'loc-dau'), ('Bugi', 'bugi'), ('DÃ¢y curoa', 'day-curoa')],
            ('Há»‡ thá»‘ng phanh', 'he-thong-phanh'): [('Bá»‘ tháº¯ng', 'bo-thang'), ('ÄÄ©a phanh', 'dia-phanh'), ('Dáº§u phanh', 'dau-phanh')],
            ('Äiá»‡n - Ä‘Ã¨n', 'dien-den'): [('áº®c quy', 'ac-quy'), ('ÄÃ¨n pha', 'den-pha'), ('Cáº£m biáº¿n', 'cam-bien')],
            ('ChÄƒm sÃ³c xe', 'cham-soc-xe'): [('Dung dá»‹ch vá»‡ sinh', 'dung-dich-ve-sinh'), ('Gáº¡t mÆ°a', 'gat-mua'), ('Phá»¥ kiá»‡n', 'phu-kien')],
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
            ('Lá»c dáº§u Ä‘á»™ng cÆ¡ Bosch', 'AP-LOCD-001', 'Lá»c dáº§u', 180000, 150000, True, 4.8),
            ('Bugi Iridium NGK', 'AP-BUGI-002', 'Bugi', 260000, None, True, 4.7),
            ('DÃ¢y curoa tá»•ng há»£p Mitsuboshi', 'AP-DAY-003', 'DÃ¢y curoa', 420000, 390000, False, 4.6),
            ('Bá»™ mÃ¡ phanh trÆ°á»›c Bendix', 'AP-PHANH-004', 'Bá»‘ tháº¯ng', 850000, 790000, True, 4.9),
            ('ÄÄ©a phanh trÆ°á»›c OEM', 'AP-DIA-005', 'ÄÄ©a phanh', 1250000, None, False, 4.5),
            ('áº®c quy khÃ´ 12V 60Ah', 'AP-AQ-006', 'áº®c quy', 1650000, 1520000, True, 4.8),
            ('BÃ³ng Ä‘Ã¨n pha LED H4', 'AP-DEN-007', 'ÄÃ¨n pha', 520000, 480000, False, 4.4),
            ('Cáº£m biáº¿n Ã¡p suáº¥t lá»‘p', 'AP-CB-008', 'Cáº£m biáº¿n', 980000, None, False, 4.3),
            ('Gáº¡t mÆ°a silicon 24 inch', 'AP-GM-009', 'Gáº¡t mÆ°a', 220000, 190000, True, 4.7),
            ('Dung dá»‹ch vá»‡ sinh kim phun', 'AP-DD-010', 'Dung dá»‹ch vá»‡ sinh', 160000, None, False, 4.2),
            ('Dáº§u phanh DOT4', 'AP-DP-011', 'Dáº§u phanh', 145000, 120000, False, 4.5),
            ('Bá»™ phá»¥ kiá»‡n cá»©u há»™ mini', 'AP-PK-012', 'Phá»¥ kiá»‡n', 350000, None, True, 4.6),
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
                    'short_description': 'Sáº£n pháº©m phá»¥ tÃ¹ng Ã´ tÃ´ phá»• biáº¿n, phÃ¹ há»£p nhiá»u dÃ²ng xe.',
                    'description': 'ThÃ´ng tin chi tiáº¿t sáº£n pháº©m, thÃ´ng sá»‘ ká»¹ thuáº­t vÃ  tÆ° váº¥n láº¯p Ä‘áº·t cÃ³ thá»ƒ cáº­p nháº­t trong Django Admin.',
                    'is_featured': featured,
                    'is_active': True,
                },
            )

        ContactMessage.objects.get_or_create(
            phone='0912345678',
            defaults={
                'full_name': 'KhÃ¡ch hÃ ng demo',
                'email': 'demo@example.com',
                'message': 'TÃ´i cáº§n tÆ° váº¥n lá»c dáº§u cho xe gia Ä‘Ã¬nh.',
            },
        )
        self.stdout.write(self.style.SUCCESS('Demo data is ready.'))
