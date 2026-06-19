# Deploy Guide — LyomasTech Salon ERP

دليل رفع عميل جديد على السيرفر (مثال: **sweb** → `sweb.erpbylyomastech.com`) مع **HTTPS**.

---
   
## جدول المتغيرات لكل عميل

| البند | مثال ahmedatef | مثال sweb |
|--------|----------------|-----------|
| Client slug | `ahmedatef` | `sweb` |
| الدومين | `ahmedatef.erpbylyomastech.com` | `sweb.erpbylyomastech.com` |
| مجلد المشروع | `/var/www/ahmedatef` | `/var/www/sweb` |
| قاعدة البيانات | `ahmedatefdb` | `swebdb` |
| مستخدم PostgreSQL | `ahmedatef_user` | `sweb_user` |
| خدمة Gunicorn | `ahmedatef.service` | `sweb.service` |
| سوبر يوزر | `LyomasTech@Ahmedatef` | `LyomasTech@Sweb` |
| الباسورد الافتراضي | `Lyo@22999` | `Lyo@22999` |

> **كل عميل = مجلد + DB + service + nginx + `.env` منفصل.**

---

## توليد ملفات جاهزة (اختياري — من جهاز التطوير)

```bash
bash deploy/new-client.sh sweb Sweb 'Lyo@22999'
```

ينشئ مجلد `deploy/generated/sweb/` يحتوي:

- `.env` — إعدادات Django وقاعدة البيانات
- `nginx.conf` — إعداد Nginx
- `gunicorn.service` — خدمة systemd
- `README.txt` — ملخص النسخ

القوالب الأصلية في: `deploy/templates/`

---

## الخطوة 1 — DNS

أضف **A Record** في لوحة الدومين:

```
sweb  →  IP_السيرفر
```

تحقق:

```bash
ping sweb.erpbylyomastech.com
```

---

## الخطوة 2 — PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE USER sweb_user WITH PASSWORD 'Lyo@22999';
CREATE DATABASE swebdb OWNER sweb_user;
GRANT ALL PRIVILEGES ON DATABASE swebdb TO sweb_user;
\q
```

---

## الخطوة 3 — نسخ المشروع على السيرفر

```bash
sudo mkdir -p /var/www/sweb
sudo chown softwarehouse:softwarehouse /var/www/sweb
cd /var/www/sweb

git clone https://github.com/Abdo-Nayel/salon_project.git .
python3 -m venv .venv
source .venv/bin/activate
pip install -r Requirements.txt
```

**مكتبات النظام لـ WeasyPrint** (مرة واحدة على السيرفر إن لم تكن مثبتة):

```bash
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

---

## الخطوة 4 — ملف `.env`

```bash
cp .env.example .env
nano .env
```

أو انسخ الملف المُولَّد من `deploy/generated/sweb/.env`.

```env
DJANGO_SECRET_KEY=مفتاح-فريد-لكل-عميل
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=sweb.erpbylyomastech.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://sweb.erpbylyomastech.com
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True

DB_NAME=swebdb
DB_USER=sweb_user
DB_PASSWORD=Lyo@22999
DB_HOST=127.0.0.1
DB_PORT=5432

DEPLOY_CLIENT_NAME=Sweb
DEPLOY_SUPERUSER_PASSWORD=Lyo@22999
```

> قبل HTTPS مؤقتاً: استخدم `http://` في `CSRF_TRUSTED_ORIGINS` واجعل `DJANGO_SESSION_COOKIE_SECURE=False` و `DJANGO_CSRF_COOKIE_SECURE=False`.

---

## الخطوة 5 — Migrate + Superuser + Static

```bash
cd /var/www/sweb
source .venv/bin/activate
bash scripts/deploy.sh
```

أو يدوياً:

```bash
python manage.py migrate --noinput
python manage.py ensure_deploy_superuser
python manage.py collectstatic --noinput
```

**تسجيل الدخول بعد النشر:**

| | |
|---|---|
| Username | `LyomasTech@Sweb` |
| Password | `Lyo@22999` |

---

## الخطوة 6 — Gunicorn (systemd)

انسخ القالب أو الملف المُولَّد:

```bash
sudo cp deploy/generated/sweb/gunicorn.service /etc/systemd/system/sweb.service
# أو من القالب: deploy/templates/gunicorn.service.template
sudo nano /etc/systemd/system/sweb.service
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable sweb
sudo systemctl start sweb
sudo systemctl status sweb
```

---

## الخطوة 7 — Nginx (HTTP أولاً)

```bash
sudo cp deploy/generated/sweb/nginx.conf /etc/nginx/sites-available/sweb
sudo ln -sf /etc/nginx/sites-available/sweb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

تحقق: `http://sweb.erpbylyomastech.com/login/`

---

## الخطوة 8 — HTTPS (Let's Encrypt)

```bash
sudo certbot --nginx -d sweb.erpbylyomastech.com
```

بعد نجاح SSL، حدّث `.env`:

```env
DJANGO_CSRF_TRUSTED_ORIGINS=https://sweb.erpbylyomastech.com
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

```bash
sudo systemctl restart sweb
```

تحقق: `https://sweb.erpbylyomastech.com/login/`

---

## Checklist سريع

```
[ ] DNS → IP السيرفر
[ ] PostgreSQL (db + user)
[ ] git clone في /var/www/<client>
[ ] venv + pip install
[ ] .env (SECRET_KEY فريد)
[ ] bash scripts/deploy.sh
[ ] gunicorn service
[ ] nginx HTTP يعمل
[ ] certbot HTTPS
[ ] CSRF + secure cookies = https
[ ] تسجيل دخول LyomasTech@<Client>
```

---

## صيانة

```bash
# إعادة تشغيل عميل واحد فقط
sudo systemctl restart sweb

# لوجات
sudo journalctl -u sweb -n 50 --no-pager

# تحديث كود
cd /var/www/sweb
git pull
source .venv/bin/activate
bash scripts/deploy.sh
sudo systemctl restart sweb
```

---

## أوامر مفيدة

```bash
# إنشاء سوبر يوزر يدوياً
python manage.py ensure_deploy_superuser --client Sweb

# تحديث باسورد السوبر يوزر
python manage.py ensure_deploy_superuser --reset-password

# حالة migrations
python manage.py showmigrations salon
```

---

## ملاحظات أمان

1. **`DJANGO_SECRET_KEY` مختلف** لكل عميل.
2. غيّر **`DEPLOY_SUPERUSER_PASSWORD`** بعد أول دخول في الإنتاج.
3. لا تشارك `.env` بين العملاء.
4. السيرفر فيه مشاريع أخرى — أعد تشغيل **خدمة العميل فقط** (`systemctl restart sweb`).
5. تجديد شهادة SSL تلقائي عبر certbot timer: `sudo systemctl status certbot.timer`

---

## هيكل الملفات

```
deploy/
  DEPLOY.md              ← هذا الملف
  new-client.sh          ← توليد ملفات عميل جديد
  templates/
    env.client.template
    gunicorn.service.template
    nginx-http.conf.template
  generated/             ← مخرجات new-client.sh (غير مرفوع لـ git)
scripts/
  deploy.sh              ← migrate + superuser + collectstatic
salon/management/commands/
  ensure_deploy_superuser.py
```
