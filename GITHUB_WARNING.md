# ⚠️ WARNING: TOKEN SECURITY ⚠️

## قبل رفع المشروع على GitHub:

### ✅ تأكد من أن:
1. **`config.py` موجود في `.gitignore`** ✓ (تم التحقق)
2. **`config.py` لن يُرفع على GitHub** ✓
3. **`config.example.py` فقط سيُرفع** ✓ (آمن - لا يحتوي على Token حقيقي)

### 🔒 الملفات المحمية (لن تُرفع):
- `config.py` - يحتوي على Token الحقيقي
- `.env` - ملفات البيئة
- `*.log` - ملفات السجلات

### ✅ الملفات الآمنة للرفع:
- `config.example.py` - قالب بدون Token حقيقي
- جميع ملفات `.py` الأخرى
- `requirements.txt`
- `README.md`
- `.gitignore`

## ⚠️ تحذير مهم:

**إذا رفعت `config.py` بالخطأ:**

1. **غير Token فوراً** في Discord Developer Portal
2. **احذف الملف من Git history** (إذا كان موجوداً)
3. **تأكد من أن `.gitignore` يحتوي على `config.py`**

## كيفية التحقق قبل الرفع:

```bash
# تحقق من الملفات التي سيتم رفعها
git status

# تأكد من أن config.py غير موجود في القائمة
# إذا ظهر، أضفه إلى .gitignore:
git rm --cached config.py
```

## ✅ الحالة الحالية:

- ✓ `config.py` موجود في `.gitignore`
- ✓ Token محمي ولن يُرفع
- ✓ `config.example.py` جاهز للرفع (آمن)

**أنت آمن للرفع على GitHub! 🎉**

