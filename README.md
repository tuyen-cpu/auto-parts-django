# AutoParts

Website giới thiệu và bán phụ tùng ô tô, xây dựng bằng Django. Project có trang chủ, danh mục sản phẩm, chi tiết sản phẩm, trang giới thiệu, form liên hệ và trang quản trị Django Admin.

## Công nghệ

- Python 3
- Django 5.2
- SQLite cho môi trường local mặc định
- PostgreSQL cho production qua `DATABASE_URL`
- HTML template Django
- CSS thuần
- Google Font Inter

## Cấu trúc chính

```text
autoparts_site/     cấu hình Django project
core/               trang chủ, cấu hình website, banner
products/           danh mục và sản phẩm
pages/              trang giới thiệu
contacts/           form liên hệ
templates/          template HTML
static/             CSS, ảnh tĩnh như logo
media/              ảnh upload từ Django Admin
```

## Cài đặt local

Tạo và kích hoạt virtual environment nếu chưa có:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Cài dependencies:

```powershell
pip install -r requirements.txt
```

Tạo file env local:

```powershell
copy .env.local.example .env.local
```

Mặc định `.env.local` để trống `DATABASE_URL`, Django sẽ dùng SQLite:

```text
db.sqlite3
```

Chạy migrate:

```powershell
python manage.py migrate
```

Tạo tài khoản admin:

```powershell
python manage.py createsuperuser
```

Chạy server:

```powershell
python manage.py runserver
```

Mở website:

```text
http://127.0.0.1:8000/
```

Mở Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## Chạy bằng PyCharm

1. Mở thư mục project `D:\canhan\autoparts`.
2. Chọn interpreter:

```text
D:\canhan\autoparts\.venv\Scripts\python.exe
```

3. Vào `Run > Edit Configurations`.
4. Tạo cấu hình `Django Server`.
5. Chọn port `8000`.
6. Chạy cấu hình vừa tạo.

Nếu PyCharm chưa nhận Django:

```text
Settings > Languages & Frameworks > Django
```

Cấu hình:

```text
Django project root: D:\canhan\autoparts
Settings: autoparts_site/settings.py
Manage script: D:\canhan\autoparts\manage.py
```

## Env files

Project có 2 loại file env:

```text
.env.local              file dùng thật khi chạy local, không commit
.env.local.example      file mẫu local, có thể commit
.env.production         file production thật, không commit
.env.production.example file mẫu production, có thể commit
```

Các biến quan trọng:

```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
DATABASE_URL=
```

Nếu `DATABASE_URL` rỗng, Django dùng SQLite. Nếu có `DATABASE_URL`, Django dùng database trong URL đó.

## PostgreSQL

Ví dụ cấu hình PostgreSQL local hoặc production:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/autoparts
```

Sau khi cấu hình PostgreSQL:

```powershell
python manage.py migrate
```

Nếu muốn chuyển dữ liệu từ SQLite sang PostgreSQL:

Export từ SQLite:

```powershell
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```

Đổi `DATABASE_URL` sang PostgreSQL, migrate, rồi import:

```powershell
python manage.py migrate
python manage.py loaddata data.json
```

## Dữ liệu demo

Project có command seed dữ liệu demo:

```powershell
python manage.py seed_demo
```

Command này tạo dữ liệu mẫu cho:

- cấu hình website
- banner
- trang giới thiệu
- danh mục sản phẩm
- sản phẩm mẫu
- liên hệ mẫu

## Upload ảnh

Ảnh upload từ Django Admin được lưu trong thư mục:

```text
media/
```

Một số đường dẫn cụ thể:

```text
media/products/     ảnh sản phẩm
media/categories/   ảnh danh mục
media/banners/      ảnh banner
media/site/         logo upload trong admin
media/pages/        ảnh trang giới thiệu
```

Lưu ý: database chỉ lưu đường dẫn ảnh, không lưu trực tiếp file ảnh.

## Static files

CSS và ảnh tĩnh nằm trong:

```text
static/
```

Logo hiện tại nằm ở:

```text
static/images/logi.jpg
```

Khi deploy production cần chạy:

```powershell
python manage.py collectstatic
```

## Các URL chính

```text
/                       trang chủ
/san-pham/              danh sách sản phẩm
/san-pham/danh-muc/.../ danh mục sản phẩm
/san-pham/.../          chi tiết sản phẩm
/gioi-thieu/            trang giới thiệu
/lien-he/               trang liên hệ
/admin/                 Django Admin
```

## Deploy production

GitHub chỉ dùng để lưu code, không tự chạy được Django. Để người khác xem website, cần deploy lên hosting hỗ trợ Django như Render, Railway, PythonAnywhere, VPS hoặc nền tảng tương tự.

Production cần cấu hình tối thiểu:

```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME
```

Các lệnh thường chạy khi deploy:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Với ảnh upload, production nên có chiến lược lưu `media/` rõ ràng:

- VPS nhỏ: lưu `media/` trên ổ đĩa server và backup định kỳ.
- Render/Railway hoặc môi trường filesystem không bền: dùng Cloudinary, S3 hoặc storage riêng.
- Production ổn định: dùng object storage/CDN.

## Git ignore

Không commit các file dữ liệu và secret:

```text
.venv/
db.sqlite3
media/
.env
.env.*
```

Các file `.env.*.example` được phép commit để làm mẫu cấu hình.

## Ghi chú vận hành

- Không xoá sản phẩm/danh mục nếu chỉ muốn ẩn khỏi website. Hãy bỏ tick `hiển thị` trong Django Admin.
- Cột `thứ tự` trong admin dùng để sắp xếp hiển thị, số nhỏ hiện trước.
- Search sản phẩm hỗ trợ tìm không dấu tiếng Việt, ví dụ `dau` vẫn tìm được `dầu`.
