# مختبر اتصال SQL Server

تطبيق WPF بـ .NET 8 لاختبار الاتصال بقاعدة بيانات SQL Server بواجهة عربية كاملة.

---

## المتطلبات

| الأداة | الإصدار |
|--------|--------|
| .NET 8 SDK | 8.0 أو أحدث |
| Visual Studio | 2022 (اختياري) |
| Windows | 10 / 11 (x64) |

---

## كيفية تشغيل المشروع في Visual Studio

1. افتح **Visual Studio 2022**
2. اختر **Open a project or solution**
3. انتقل إلى مجلد `SqlConnectionTester`
4. افتح ملف `SqlConnectionTester\SqlConnectionTester.csproj`
5. اضغط **F5** للتشغيل

---

## بناء ملف EXE واحد (Standalone)

### الطريقة السريعة — سكربت البناء

```bat
build.bat
```

بعد الانتهاء سيفتح المجلد تلقائياً على ملف `SqlConnectionTester.exe`.

### الطريقة اليدوية — سطر الأوامر

```bat
cd SqlConnectionTester
dotnet publish SqlConnectionTester.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -p:EnableCompressionInSingleFile=true -o ..\publish\win-x64
```

---

## مكان ملف الـ EXE النهائي

```
SqlConnectionTester\
└── publish\
    └── win-x64\
        └── SqlConnectionTester.exe   ← هذا هو الملف النهائي
```

> الملف مكتفٍ بذاته (**Self-contained**) ولا يحتاج تثبيت .NET على جهاز المستخدم.

---

## إرسال الملف للمستخدم

1. انسخ ملف `SqlConnectionTester.exe` فقط
2. أرسله عبر واتساب / إيميل / أي وسيلة
3. المستخدم يشغله مباشرة بدون أي تثبيت

> **ملاحظة:** حجم الملف حوالي 60-80 ميجابايت بسبب احتواء .NET runtime بداخله.

---

## مميزات التطبيق

- دعم **Windows Authentication** و **SQL Server Authentication**
- عرض **إصدار SQL Server** و **وقت الاستجابة** عند النجاح
- رسائل خطأ **واضحة بالعربية** عند الفشل
- **حفظ الإعدادات** تلقائياً في `settings.json` (بدون كلمة مرور)
- **تحديد المنفذ** اختيارياً (افتراضي: 1433)
- واجهة **RTL عربية** بتصميم حديث

---

## هيكل المشروع

```
SqlConnectionTester/
├── SqlConnectionTester/
│   ├── Models/
│   │   └── ConnectionSettings.cs
│   ├── Services/
│   │   ├── ConnectionService.cs
│   │   └── SettingsService.cs
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── MainWindow.xaml
│   ├── MainWindow.xaml.cs
│   └── SqlConnectionTester.csproj
├── build.bat
└── README.md
```
