# نموذج البيانات النهائي (ERD) — الباك اند العام

هذا المستند يعكس النماذج **الفعلية** بعد اكتمال المراحل 0-7 (`apps/*/models.py`)، وليس نسخة تخطيطية أولية. أي تعديل على النماذج يجب أن يُحدَّث هنا بالتوازي.

كل النماذج (باستثناء `accounts.User` الذي يرث من `AbstractUser`) ترث من `apps.core.models.BaseModel` (مفتاح أساسي UUID + `created_at`/`updated_at`).

## accounts

- **User** (`AUTH_USER_MODEL`): username, email, password, full_name, phone, national_id, employee_id, hire_date, is_active, is_staff, is_superuser
  - الأدوار = عضوية `django.contrib.auth.models.Group` (Admin, Doctor, Nurse, Pharmacist, WarehouseKeeper, LabTech, Receptionist)

## patients

- **Patient**: mrn (تلقائي `MRN######`), first_name, father_name, grandfather_name, family_name, national_id, date_of_birth, gender, blood_type, phone, address, emergency_contact_name/phone, registration_date, is_active, created_by → User
  - سجل تدقيق كامل عبر `django-simple-history` (`HistoricalPatient`)
- **MedicalHistory** (1:1 → Patient): comorbidities, allergies, cause_of_kidney_failure, dialysis_start_date, bloodborne_virus_status, notes
- **VascularAccess** (N:1 → Patient): access_type, site, creation_date, status
- **ClinicalNote** (N:1 → Patient, author → User): note_type, content
- **VitalSign** (N:1 → Patient, N:1 → scheduling.DialysisSession اختياري, recorded_by → User): weight_pre/post_kg, blood_pressure_pre/post, pulse, temperature_c

## scheduling

- **Machine**: code, room, status
- **Shift**: name, start_time, end_time
- **DialysisSchedule** (القالب المتكرر، N:1 → Patient): days_of_week (JSON)، preferred_shift → Shift، session_duration_minutes، start_date، end_date، status — **بلا تعيين جهاز/سرير ثابت**
- **DialysisSession** (الجلسة الفعلية، N:1 → Patient, N:1 → DialysisSchedule اختياري): machine → Machine، shift → Shift (تُعيَّن ديناميكيًا عند تسجيل الحضور عبر `DialysisSchedule.check_in()`)، scheduled_date، check_in_time، actual_start/end_time، status، assigned_nurse/assigned_doctor → User
- **DialysisParameters** (1:1 → DialysisSession): blood_flow_rate_ml_min، dialysate_flow_rate_ml_min، uf_target/actual_ml، anticoagulant، duration_minutes، notes

## warehouse

- **Supplier**: name, contact_person, phone, email, address
- **SupplyItem**: name, category (medical_supply / medication_bulk / consumable / equipment), unit_of_measure, reorder_level
- **SupplyStock** (N:1 → SupplyItem): batch_number, expiry_date, quantity_on_hand, location
- **StockMovement** (N:1 → SupplyItem, N:1 → Supplier اختياري, performed_by → User): movement_type (in/out/adjustment), quantity, movement_date, reference

## pharmacy

- **Drug** (N:1 → warehouse.SupplyItem اختياري عبر `warehouse_item`): name, generic_name, form, strength, category, requires_prescription
- **DrugStock** (N:1 → Drug): batch_number, expiry_date, quantity_on_hand, location
- **Prescription** (N:1 → Patient, prescribing_doctor → User, N:1 → Drug): dosage, frequency, route, start_date, end_date, status — سجل تدقيق كامل
- **DispenseRecord** (N:1 → Prescription, pharmacist → User, N:1 → DrugStock): quantity_dispensed, dispensed_at — سجل تدقيق كامل
- **PharmacyStockRequest** (requested_by → User, N:1 → Drug, approved_by → User اختياري): quantity_requested, status (pending/approved/rejected/fulfilled), requested_at, decided_at, fulfilled_at, notes — سجل تدقيق كامل
  - **منطق العمل (`approve()`)**: يخصم من دفعات `warehouse.SupplyStock` المرتبطة بـ `Drug.warehouse_item` (FIFO حسب تاريخ الانتهاء)، ينشئ `warehouse.StockMovement` (خروج)، وينشئ دفعة `DrugStock` جديدة في الصيدلية بنفس الكمية — كل ذلك ضمن معاملة قاعدة بيانات واحدة (`transaction.atomic`)

## nursing

- **Attendance** (N:1 → User, N:1 → scheduling.Shift اختياري): date, check_in/out_time, status
- **MedicationAdministrationRecord (MAR)** (N:1 → pharmacy.Prescription, N:1 → Patient, N:1 → scheduling.DialysisSession اختياري, administered_by → User اختياري): scheduled_time, administered_at, status (pending/given/refused/missed/held), dose_given, notes
  - **يُنشأ تلقائيًا** عبر `post_save` على `Prescription` نشِطة جديدة (`apps/nursing/signals.py`) — هذا هو الرابط التلقائي بين وصفة الطبيب ومهمة الممرض

## lab

- **LabTestType**: name, code (فريد), category, unit, reference_range_low/high, sample_type
- **LabOrder** (N:1 → Patient, ordering_doctor → User, N:1 → LabTestType, N:1 → scheduling.DialysisSession اختياري): order_date, status (ordered/sample_collected/resulted/cancelled), priority
- **LabResult** (1:1 → LabOrder, performed_by/verified_by → User اختياري): result_value, unit, is_abnormal, **source** (manual/instrument — يدوي افتراضيًا الآن، جاهز للربط الآلي لاحقًا دون تغيير البنية), result_date, notes
  - إدخال نتيجة يحدّث `LabOrder.status` تلقائيًا إلى `resulted`

## خريطة الاعتماديات بين التطبيقات

```
accounts (User, Roles)
   │
   ▼
patients (Patient) ──────────────┐
   │                              │
   ▼                              ▼
scheduling (Machine, Shift,    lab (LabOrder → LabResult)
  DialysisSchedule,               │
  DialysisSession) ◄──────────────┘ (dialysis_session FK اختياري)
   │
   ▼
warehouse (SupplyItem, SupplyStock) ◄── pharmacy (Drug.warehouse_item)
                                          │
                                          ▼
                                    pharmacy (Prescription, DispenseRecord,
                                       PharmacyStockRequest)
                                          │
                                          ▼
                                    nursing (MedicationAdministrationRecord)
                                       — يُنشأ تلقائيًا من Prescription
```
