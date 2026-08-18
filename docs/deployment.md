# دليل النشر المحلي (On-Premise Deployment)

دليل خطوة بخطوة لتثبيت النظام على خادم داخل مركز الديلزة، بدون افتراض معرفة مسبقة بـ Docker.

## المتطلبات على الخادم

- جهاز خادم (فيزيائي أو VM) يعمل بنظام Linux، متصل بشبكة المركز المحلية (LAN)
- تثبيت [Docker Engine](https://docs.docker.com/engine/install/) و Docker Compose (يأتي مدمجًا في إصدارات Docker الحديثة كـ `docker compose`)
- مساحة تخزين كافية (يُفضّل قرص منفصل للنسخ الاحتياطية عن قرص قاعدة البيانات — انظر قسم النسخ الاحتياطي أدناه)

## خطوات التثبيت الأولى

### 1. نسخ المستودع على الخادم

```bash
git clone <repository-url> dialysis
cd dialysis
```

### 2. إعداد ملف البيئة `.env`

```bash
cp .env.example .env
```

عدّل الملف `.env` وضع قيمًا حقيقية (وليس القيم الافتراضية للتطوير):

- `DJANGO_SETTINGS_MODULE=config.settings.prod`
- `DJANGO_SECRET_KEY`: نص عشوائي طويل (يمكن توليده بـ `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`: عنوان/اسم الخادم على الشبكة المحلية (مثال: `dialysis.local,192.168.1.10`)
- `POSTGRES_PASSWORD`: كلمة مرور قوية (وليس `dialysis` الافتراضية)
- `DATABASE_URL`: يجب أن تشير إلى `db` كاسم مضيف داخل شبكة Docker: `postgres://dialysis:<كلمة_المرور>@db:5432/dialysis`

**لا تستخدم القيم الافتراضية الموجودة في `.env.example` في بيئة الإنتاج.**

### 3. توليد شهادة TLS محلية

```bash
./deploy/nginx/generate_self_signed_cert.sh dialysis.local 192.168.1.10
```

استبدل `dialysis.local` و`192.168.1.10` باسم/عنوان الخادم الفعلي على شبكة المركز.

### 4. بناء وتشغيل الحزمة الكاملة

```bash
docker compose -f deploy/docker-compose.yml --env-file .env up -d --build
```

هذا يشغّل 4 خدمات:
- `db`: قاعدة بيانات PostgreSQL
- `app`: تطبيق Django (يُطبّق الـ migrations تلقائيًا عند الإقلاع عبر `deploy/entrypoint.sh`)
- `nginx`: يستقبل الطلبات عبر HTTPS ويوجهها للتطبيق
- `backup`: يشغّل نسخة احتياطية تلقائية يوميًا الساعة 2:00 صباحًا

تحقق من أن كل الخدمات تعمل:

```bash
docker compose -f deploy/docker-compose.yml ps
```

### 5. إنشاء حساب المدير الأول وتوزيع الأدوار

```bash
docker compose -f deploy/docker-compose.yml exec app python manage.py createsuperuser
docker compose -f deploy/docker-compose.yml exec app python manage.py seed_roles
docker compose -f deploy/docker-compose.yml exec app python manage.py seed_scheduling
docker compose -f deploy/docker-compose.yml exec app python manage.py seed_lab
```

### 6. تثبيت الشهادة على أجهزة الموظفين والآيباد

بما أن الشهادة موقّعة ذاتيًا (وليست من جهة إصدار معروفة)، يجب تثبيتها كـ "موثوقة" مرة واحدة على كل جهاز سيصل للنظام:

- انسخ ملف `deploy/nginx/certs/dialysis.crt` إلى كل جهاز (عبر AirDrop، بريد داخلي، أو USB)
- **iPad/iPhone**: افتح الملف → Settings → General → VPN & Device Management → ثبّت الملف الشخصي، ثم فعّل الثقة الكاملة من Settings → General → About → Certificate Trust Settings
- **Windows/Mac**: استورد الشهادة إلى مخزن الشهادات الموثوقة للنظام (Trusted Root Certification Authorities)

بدون هذه الخطوة سيظهر تحذير أمان في المتصفح عند كل دخول للنظام.

### 7. التحقق من التثبيت

- افتح `https://dialysis.local/admin/` من متصفح على الشبكة المحلية وسجّل دخول بحساب المدير
- افتح `https://dialysis.local/api/docs/` للتأكد من ظهور توثيق Swagger لكل الوحدات
- سجّل دخول تجريبي بمستخدم من كل دور (بعد إنشائه من الأدمن) وتأكد أن الصلاحيات تطابق `docs/permissions.md`

## النسخ الاحتياطي والاستعادة

### النسخ التلقائي

خدمة `backup` تُشغّل `deploy/backup/backup.sh` يوميًا الساعة 2:00 صباحًا داخل الحاوية، وتحفظ النسخ في ثلاث مجلدات فرعية ضمن الـ volume `dialysis_backups`:
- `daily/`: يُحتفظ بآخر 14 نسخة (قابل للتعديل عبر `BACKUP_RETENTION_DAILY` في `docker-compose.yml`)
- `weekly/`: نسخة كل يوم أحد، يُحتفظ بآخر 8
- `monthly/`: نسخة أول يوم من كل شهر، يُحتفظ بآخر 6

**يُنصح بشدة** بنقل نسخة دورية (أسبوعية على الأقل) إلى وسيط خارجي (USB) أو موقع فيزيائي آخر، لأن الخادم المحلي نقطة فشل وحيدة بدون نسخة احتياطية سحابية:

```bash
docker compose -f deploy/docker-compose.yml cp backup:/backups/daily/. ./local-backup-copy/
```

### اختبار الاستعادة (Restore Drill)

نسخة احتياطية لم تُختبر استعادتها **لا تُعتبر نسخة موثوقة**. نفّذ هذا الاختبار عند التثبيت الأول، ثم بشكل دوري (يُنصح شهريًا):

```bash
docker compose -f deploy/docker-compose.yml exec backup \
  sh /usr/local/bin/restore.sh /backups/daily/<اسم_الملف>.dump dialysis_restore_test
```

ثم تحقق من عدد السجلات في قاعدة الاستعادة التجريبية ومطابقتها للمتوقع، كما هو موضح في مخرجات السكربت. احذف قاعدة الاختبار بعد التحقق:

```bash
docker compose -f deploy/docker-compose.yml exec db \
  psql -U dialysis -d postgres -c "DROP DATABASE dialysis_restore_test;"
```

> تم تنفيذ هذا الاختبار فعليًا أثناء بناء النظام (خارج بيئة Docker، مباشرة عبر `pg_dump`/`pg_restore` على نفس قاعدة البيانات) للتأكد من صحة منطق النسخ والاستعادة قبل اعتماد هذه الخطة.

### الاستعادة الفعلية عند كارثة

```bash
docker compose -f deploy/docker-compose.yml exec backup \
  sh /usr/local/bin/restore.sh /backups/daily/<اسم_الملف>.dump dialysis
```

**تحذير**: هذا يستبدل قاعدة البيانات الحالية بالكامل بمحتوى النسخة الاحتياطية. تأكد من إيقاف خدمة `app` أولًا لمنع كتابة بيانات جديدة أثناء الاستعادة.

## التحديثات اللاحقة

```bash
git pull
docker compose -f deploy/docker-compose.yml up -d --build
```

الـ migrations تُطبَّق تلقائيًا عند إعادة تشغيل `app` (عبر `deploy/entrypoint.sh`).

## استكشاف الأخطاء

- **الحاوية `app` لا تبدأ**: تحقق من السجلات `docker compose -f deploy/docker-compose.yml logs app` — غالبًا مشكلة في `.env` (خاصة `DATABASE_URL` أو `DJANGO_SECRET_KEY`)
- **تحذير أمان في المتصفح**: الشهادة غير مثبّتة كموثوقة على هذا الجهاز — راجع الخطوة 6
- **`docker compose` غير موجود**: تأكد من تثبيت Docker بإصدار حديث يدعم Compose V2، أو استخدم `docker-compose` (بشرطة) إذا كان مثبتًا بشكل منفصل
