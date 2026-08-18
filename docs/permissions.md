# مصفوفة الصلاحيات (RBAC Permission Matrix)

هذا المستند هو مصدر الحقيقة الذي يُترجم مباشرة إلى:
- عضوية `django.contrib.auth.models.Group` لكل دور (تُنشأ عبر `python manage.py seed_roles`)
- صلاحيات النماذج التلقائية في Django (`add_<model>` / `change_<model>` / `delete_<model>` / `view_<model>`) المُسندة لكل Group داخل `ROLE_MODEL_PERMISSIONS` في `apps/accounts/management/commands/seed_roles.py`
- DRF Permission classes في `apps/core/permissions.py` (`IsAdmin`, `IsDoctor`, `IsNurse`, `IsPharmacist`, `IsWarehouseKeeper`, `IsLabTech`, `IsReceptionist`) المستخدمة على مستوى الـ ViewSet/Endpoint
- Serializers متمايزة حسب الدور عند الحاجة (مثال: `PatientBasicSerializer` مقابل `PatientFullSerializer`)

`Admin` (وأي `is_superuser=True`) له وصول كامل لكل شيء دائمًا، ولا يظهر بشكل صريح في كل صف أدناه.

## الأدوار السبعة
`Admin` · `Doctor` · `Nurse` · `Pharmacist` · `WarehouseKeeper` · `LabTech` · `Receptionist`

## مصفوفة الوحدات

| الوحدة | Doctor | Nurse | Pharmacist | WarehouseKeeper | LabTech | Receptionist |
|---|---|---|---|---|---|---|
| المرضى/EMR (`patients`) | كامل | عرض + إضافة ملاحظات سريرية | عرض (ديموغرافي فقط) | لا شيء | عرض (ديموغرافي فقط) | عرض + تعديل البيانات الديموغرافية |
| الجدولة/الحضور (`scheduling`) | عرض | عرض + تحديث حالة الجلسة | لا شيء | لا شيء | لا شيء | كامل (إنشاء/تعديل) |
| الصيدلية (`pharmacy`) | إنشاء `Prescription` فقط | عرض (لأغراض MAR) | كامل + إنشاء `PharmacyStockRequest` | لا شيء | لا شيء | لا شيء |
| المخزن (`warehouse`) | لا شيء | لا شيء | عرض فقط (لتتبع طلباته) | كامل + موافقة/رفض `PharmacyStockRequest` | لا شيء | لا شيء |
| التمريض/MAR (`nursing`) | عرض | كامل | عرض | لا شيء | لا شيء | لا شيء |
| المختبر (`lab`) | إنشاء `LabOrder` + عرض `LabResult` | عرض | لا شيء | لا شيء | كامل | لا شيء |
| إدارة المستخدمين (`accounts`) | لا شيء | لا شيء | لا شيء | لا شيء | لا شيء | عرض فقط (`User`، للتحقق من الأسماء عند الجدولة) |

## ملاحظات تنفيذية
- **لا صلاحيات على مستوى الكائن الفردي** في هذه المرحلة (object-level permissions) — أي دور مصرّح له بـ "عرض" على وحدة يرى كل السجلات، وليس فقط سجلاته. يُعاد النظر في هذا لاحقًا إذا ظهرت حاجة فعلية (مثال: حصر الطبيب بمرضاه المعيّنين فقط).
- **الصيدلي مقابل مسؤول المخزن على `PharmacyStockRequest`**: الصيدلي يملك `add` فقط (يُنشئ الطلب)، بينما التحديث اللاحق لحالته (`approved`/`rejected`) محصور بمسؤول المخزن عبر منطق عمل مخصص في الـ ViewSet وليس صلاحية `change` عامة — لأن الصيدلي يجب أن يستطيع إنشاء طلب لكن لا يوافق على طلبه هو نفسه.
- **إدارة الأدوار والصلاحيات نفسها** (إنشاء مستخدمين، تعيين مجموعات) محصورة بـ `Admin` فقط عبر أدمن Django أو نقاط API مخصصة لاحقًا.
