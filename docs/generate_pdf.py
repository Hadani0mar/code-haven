import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os

# ── Fonts ──────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Amiri", "/tmp/Amiri-Regular.ttf"))
try:
    pdfmetrics.registerFont(TTFont("AmiriBold", "/tmp/Amiri-Bold.ttf"))
except:
    pdfmetrics.registerFont(TTFont("AmiriBold", "/tmp/Amiri-Regular.ttf"))

# ── Colors ─────────────────────────────────────────────────────────────────
NAVY     = HexColor("#1a2e52")
BLUE     = HexColor("#1d4ed8")
LIGHT_BG = HexColor("#f0f4ff")
CARD_BG  = HexColor("#f8fafc")
BORDER   = HexColor("#cbd5e1")
GREEN    = HexColor("#16a34a")
RED      = HexColor("#dc2626")
YELLOW   = HexColor("#ca8a04")
GRAY     = HexColor("#64748b")
WHITE    = white

W, H = A4  # 595 x 842

OUT = "/home/user/code-haven/docs/منصتي-توثيق-المشروع.pdf"

# ── Helpers ────────────────────────────────────────────────────────────────
def ar(text):
    """Reshape + bidi Arabic text for ReportLab."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def draw_text(c, text, x, y, font="Amiri", size=11, color=black, align="right"):
    c.setFont(font, size)
    c.setFillColor(color)
    shaped = ar(text)
    if align == "right":
        c.drawRightString(x, y, shaped)
    elif align == "center":
        c.drawCentredString(x, y, shaped)
    else:
        c.drawString(x, y, shaped)

def draw_rect(c, x, y, w, h, fill=None, stroke=None, radius=4):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    else:
        c.setStrokeColor(fill or BORDER)
    c.roundRect(x, y, w, h, radius, fill=1 if fill else 0, stroke=1 if stroke else 0)

def h_line(c, y, color=BORDER, width=0.5, x1=2*cm, x2=W-2*cm):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)

def new_page(c):
    c.showPage()
    # subtle header line
    c.setStrokeColor(NAVY)
    c.setLineWidth(3)
    c.line(0, H-0.5*cm, W, H-0.5*cm)
    return H - 1.5*cm

def footer(c, page_num, total):
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(2*cm, 1.5*cm, W-2*cm, 1.5*cm)
    draw_text(c, "منصتي — منصة ليبية لتبادل الأكواد", W-2*cm, 0.9*cm, size=8, color=GRAY)
    draw_text(c, f"{total} / {page_num}", 2*cm+1*cm, 0.9*cm, size=8, color=GRAY, align="left")

def section_title(c, title, y, color=NAVY):
    draw_rect(c, 1.8*cm, y-0.35*cm, W-3.6*cm, 0.85*cm, fill=LIGHT_BG, stroke=BORDER)
    c.setStrokeColor(color)
    c.setLineWidth(4)
    c.line(W-1.8*cm, y-0.35*cm, W-1.8*cm, y+0.5*cm)
    draw_text(c, title, W-2.2*cm, y+0.05*cm, font="AmiriBold", size=14, color=color)
    return y - 1.3*cm

def bullet(c, text, x, y, color=NAVY, size=10.5):
    c.setFillColor(color)
    c.circle(x+0.25*cm, y+0.18*cm, 3, fill=1)
    draw_text(c, text, x, y, size=size, color=black)
    return y - 0.65*cm

def step_box(c, num, title, body, x, y, w):
    draw_rect(c, x, y-1.8*cm, w, 1.9*cm, fill=CARD_BG, stroke=BORDER)
    # circle number
    c.setFillColor(BLUE)
    c.circle(x+w-0.6*cm, y-0.55*cm, 10, fill=1)
    c.setFont("AmiriBold", 11)
    c.setFillColor(WHITE)
    c.drawCentredString(x+w-0.6*cm, y-0.62*cm, str(num))
    draw_text(c, title, x+w-1.3*cm, y-0.5*cm, font="AmiriBold", size=10.5, color=NAVY)
    draw_text(c, body,  x+w-1.3*cm, y-1.1*cm, size=9, color=GRAY)
    return y - 2.2*cm

def tag(c, text, x, y, bg=BLUE, fg=WHITE):
    tw = len(text)*5 + 16
    draw_rect(c, x, y-2, tw, 16, fill=bg, radius=3)
    c.setFont("Amiri", 8)
    c.setFillColor(fg)
    shaped = ar(text)
    c.drawCentredString(x + tw/2, y+1, shaped)
    return tw + 6

# ═══════════════════════════════════════════════════════════════════════════
#  BUILD PDF
# ═══════════════════════════════════════════════════════════════════════════
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("منصتي - توثيق المشروع")
c.setAuthor("منصتي")
c.setSubject("توثيق مشروع التخرج")
TOTAL_PAGES = 6

# ───────────────────────────────────────────────────
# PAGE 1  — COVER
# ───────────────────────────────────────────────────
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)

# decorative circles
c.setFillColor(HexColor("#1e3a6e"))
c.circle(W-1*cm, H-1*cm, 120, fill=1, stroke=0)
c.circle(1*cm, 1*cm, 80, fill=1, stroke=0)

c.setFillColor(BLUE)
c.circle(W/2, H/2+2*cm, 180, fill=0, stroke=1)
c.setLineWidth(0.5)

# Logo placeholder box
draw_rect(c, W/2-2*cm, H-10*cm, 4*cm, 4*cm, fill=HexColor("#1e3a6e"), stroke=HexColor("#3b5bdb"), radius=12)
draw_text(c, "</> ", W/2, H-8.4*cm, font="AmiriBold", size=28, color=WHITE, align="center")

draw_text(c, "منصتي", W/2, H-11.5*cm, font="AmiriBold", size=42, color=WHITE, align="center")
draw_text(c, "منصة ليبية لتبادل الأكواد", W/2, H-13*cm, font="Amiri", size=18, color=HexColor("#93c5fd"), align="center")

# divider
c.setStrokeColor(BLUE)
c.setLineWidth(1.5)
c.line(W/2-6*cm, H-14*cm, W/2+6*cm, H-14*cm)

draw_text(c, "توثيق مشروع التخرج", W/2, H-15*cm, font="AmiriBold", size=16, color=HexColor("#e2e8f0"), align="center")
draw_text(c, "يشمل: دليل الإدارة · التقنيات · قاعدة البيانات · الأسئلة الشائعة", W/2, H-16*cm, font="Amiri", size=11, color=HexColor("#94a3b8"), align="center")

# bottom bar
c.setFillColor(BLUE)
c.rect(0, 0, W, 3*cm, fill=1, stroke=0)
draw_text(c, "2026  ·  جامعة ليبية", W/2, 1.2*cm, font="Amiri", size=11, color=WHITE, align="center")

footer(c, 1, TOTAL_PAGES)
c.showPage()

# ───────────────────────────────────────────────────
# PAGE 2  — PROJECT OVERVIEW + TECH STACK
# ───────────────────────────────────────────────────
c.setStrokeColor(NAVY); c.setLineWidth(3)
c.line(0, H-0.5*cm, W, H-0.5*cm)
y = H - 1.8*cm

draw_text(c, "١. نظرة عامة على المشروع", W-2*cm, y, font="AmiriBold", size=18, color=NAVY)
y -= 0.4*cm
h_line(c, y)
y -= 0.8*cm

# Intro box
draw_rect(c, 1.8*cm, y-2.6*cm, W-3.6*cm, 2.8*cm, fill=LIGHT_BG, stroke=BORDER)
lines = [
    "منصتي هي منصة ويب عربية مخصصة لتبادل أكواد HTML و CSS و JavaScript بين المطورين.",
    "يتولى فريق المنصة نشر الأكواد عبر لوحة إدارة محمية، بينما يستطيع أي زائر تصفّح",
    "الأكواد ونسخها وتحميلها مباشرةً دون الحاجة إلى تسجيل حساب.",
]
ly = y - 0.55*cm
for ln in lines:
    draw_text(c, ln, W-2.2*cm, ly, size=11, color=NAVY)
    ly -= 0.62*cm
y -= 3.2*cm

# Features
y = section_title(c, "المميزات الرئيسية", y)
pairs = [
    ("نشر وإدارة الأكواد عبر لوحة تحكم محمية", "دعم ثلاثة أنواع: HTML و CSS و JavaScript"),
    ("نوع 'كاملة' يجمع HTML+CSS+JS في ملف واحد", "إحصائيات النسخ والتفاعل لكل كود"),
    ("بحث وتصفية حسب النوع والتصنيف", "رفع الملفات المرفقة مع الأكواد"),
    ("تصميم عربي RTL بالكامل", "واجهة متجاوبة مع جميع الأجهزة"),
]
for right_t, left_t in pairs:
    c.setFillColor(BLUE); c.circle(W-2.2*cm, y+0.18*cm, 3, fill=1)
    draw_text(c, right_t, W-2.35*cm, y, size=10.5)
    c.setFillColor(BLUE); c.circle(W/2+0.2*cm, y+0.18*cm, 3, fill=1)
    draw_text(c, left_t, W/2+0.05*cm, y, size=10.5)
    y -= 0.65*cm

y -= 0.3*cm
y = section_title(c, "٢. التقنيات المستخدمة", y)

techs = [
    ("React 18 + TypeScript", "بناء واجهة المستخدم بمكونات قابلة لإعادة الاستخدام مع أمان الأنواع", BLUE),
    ("Vite", "أداة بناء سريعة للتطوير والإنتاج", HexColor("#7c3aed")),
    ("Tailwind CSS + shadcn/ui", "تنسيق سريع باستخدام مكتبة مكونات جاهزة", HexColor("#0891b2")),
    ("Supabase", "قاعدة بيانات PostgreSQL + خدمات خلفية جاهزة", GREEN),
    ("Supabase Edge Functions", "دوال خادم لا تحتاج سيرفر (Deno Runtime)", HexColor("#059669")),
    ("Vercel", "نشر واستضافة تلقائية عند كل تحديث", black),
]

for name, desc, color in techs:
    draw_rect(c, 1.8*cm, y-0.65*cm, W-3.6*cm, 0.75*cm, fill=CARD_BG, stroke=BORDER)
    c.setFillColor(color); c.rect(W-1.8*cm, y-0.65*cm, 0.3*cm, 0.75*cm, fill=1, stroke=0)
    draw_text(c, name, W-2.3*cm, y-0.3*cm, font="AmiriBold", size=10, color=color)
    draw_text(c, desc, W/2+1*cm, y-0.3*cm, size=9.5, color=GRAY)
    y -= 0.9*cm

footer(c, 2, TOTAL_PAGES)
c.showPage()

# ───────────────────────────────────────────────────
# PAGE 3  — WHY SUPABASE + DATABASE
# ───────────────────────────────────────────────────
c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(0, H-0.5*cm, W, H-0.5*cm)
y = H - 1.8*cm

draw_text(c, "٣. لماذا Supabase؟", W-2*cm, y, font="AmiriBold", size=18, color=NAVY)
y -= 0.4*cm; h_line(c, y); y -= 0.8*cm

# Highlight box
draw_rect(c, 1.8*cm, y-2.2*cm, W-3.6*cm, 2.4*cm, fill=HexColor("#f0fdf4"), stroke=GREEN, radius=6)
c.setFillColor(GREEN); c.setLineWidth(4); c.line(W-1.8*cm, y-2.2*cm, W-1.8*cm, y+0.2*cm)
txt = "Supabase هو بديل مفتوح المصدر لـ Firebase يوفر باكيند جاهزاً بالكامل دون الحاجة"
txt2 = "لإعداد سيرفر أو كتابة كود خلفي من الصفر — مما وفّر وقتاً كبيراً في تطوير المشروع."
draw_text(c, txt,  W-2.3*cm, y-0.6*cm,  font="AmiriBold", size=11, color=HexColor("#14532d"))
draw_text(c, txt2, W-2.3*cm, y-1.3*cm, size=10.5, color=HexColor("#166534"))
y -= 2.8*cm

reasons = [
    ("قاعدة بيانات PostgreSQL جاهزة", "لا حاجة لإعداد قاعدة بيانات منفصلة أو صيانتها"),
    ("Row Level Security (RLS)", "سياسات أمان تمنع الوصول غير المصرح به مباشرة من قاعدة البيانات"),
    ("Edge Functions", "دوال خادمية تعمل على CDN العالمي دون الحاجة لسيرفر مخصص"),
    ("تخزين الملفات (Storage)", "رفع وتنزيل الملفات بسهولة مع روابط عامة أو خاصة"),
    ("مفاتيح API جاهزة", "مفتاح عام للقراءة ومفتاح سري للعمليات الإدارية بدون مصادقة معقدة"),
    ("الطبقة المجانية كافية", "تكفي لمشروع التخرج ومرحلة الإطلاق الأولى بدون أي تكلفة"),
]
for title_r, desc_r in reasons:
    draw_rect(c, 1.8*cm, y-0.7*cm, W-3.6*cm, 0.82*cm, fill=CARD_BG, stroke=BORDER)
    c.setFillColor(GREEN); c.circle(W-2.1*cm, y-0.27*cm, 4, fill=1)
    draw_text(c, title_r, W-2.5*cm, y-0.38*cm, font="AmiriBold", size=10, color=NAVY)
    draw_text(c, desc_r,  W/2+0.5*cm, y-0.38*cm, size=9.5, color=GRAY)
    y -= 1*cm

y -= 0.4*cm
y = section_title(c, "٤. قاعدة البيانات", y)

# Table schema
headers = ["الوصف", "النوع", "العمود"]
col_w   = [(W-3.6*cm)*0.5, (W-3.6*cm)*0.22, (W-3.6*cm)*0.28]
# Header row
draw_rect(c, 1.8*cm, y-0.5*cm, W-3.6*cm, 0.55*cm, fill=NAVY, radius=0)
hx = W - 1.8*cm
for i, (h_text, cw) in enumerate(zip(headers, col_w)):
    draw_text(c, h_text, hx - 0.15*cm, y-0.32*cm, font="AmiriBold", size=9.5, color=WHITE)
    hx -= cw
y -= 0.55*cm

rows = [
    ("المعرف الفريد للكود", "UUID", "id"),
    ("عنوان الكود", "TEXT", "title"),
    ("وصف مختصر", "TEXT", "description"),
    ("نوع الكود: HTML/CSS/JS/FULL", "TEXT", "language"),
    ("التصنيف (نماذج، قوائم...)", "TEXT", "category"),
    ("محتوى الكود أو JSON للنوع كاملة", "TEXT", "code"),
    ("رابط الملف المرفق في Storage", "TEXT", "file_url"),
    ("عداد النسخ والتحميلات", "INTEGER", "views"),
    ("عداد التفاعلات", "INTEGER", "likes"),
    ("هل الكود منشور للزوار؟", "BOOLEAN", "published"),
    ("تاريخ الإنشاء", "TIMESTAMPTZ", "created_at"),
]
for i, (desc_t, type_t, col_t) in enumerate(rows):
    bg = CARD_BG if i % 2 == 0 else WHITE
    draw_rect(c, 1.8*cm, y-0.42*cm, W-3.6*cm, 0.46*cm, fill=bg, stroke=BORDER, radius=0)
    rx = W - 1.8*cm
    draw_text(c, desc_t, rx-0.15*cm, y-0.27*cm, size=9)
    rx -= col_w[0]
    c.setFont("Amiri", 9); c.setFillColor(BLUE)
    c.drawRightString(rx-0.15*cm, y-0.27*cm, type_t)
    rx -= col_w[1]
    c.setFont("Amiri", 9); c.setFillColor(HexColor("#7c3aed"))
    c.drawRightString(rx-0.15*cm, y-0.27*cm, col_t)
    y -= 0.46*cm

footer(c, 3, TOTAL_PAGES)
c.showPage()

# ───────────────────────────────────────────────────
# PAGE 4  — ADMIN GUIDE (1)
# ───────────────────────────────────────────────────
c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(0, H-0.5*cm, W, H-0.5*cm)
y = H - 1.8*cm

draw_text(c, "٥. دليل لوحة الإدارة", W-2*cm, y, font="AmiriBold", size=18, color=NAVY)
y -= 0.4*cm; h_line(c, y); y -= 0.9*cm

# Access
y = section_title(c, "الدخول إلى اللوحة", y)
draw_rect(c, 1.8*cm, y-1.2*cm, W-3.6*cm, 1.35*cm, fill=CARD_BG, stroke=BORDER)
draw_text(c, "الرابط:", W-2.2*cm, y-0.4*cm, font="AmiriBold", size=11, color=NAVY)
c.setFont("Amiri", 11); c.setFillColor(BLUE)
c.drawRightString(W-4.5*cm, y-0.4*cm, "yoursite.vercel.app/admin")
draw_text(c, "أدخل رمز الحماية في الحقل ثم اضغط 'دخول' أو مفتاح Enter.", W-2.2*cm, y-0.9*cm, size=10.5)
y -= 1.7*cm

# Steps
y = section_title(c, "خطوات نشر كود جديد", y)
steps = [
    ("١", "أدخل العنوان والتصنيف", "العنوان إلزامي، التصنيف اختياري (مثال: نماذج)"),
    ("٢", "اختر نوع اللغة", "HTML أو CSS أو JS أو كاملة (HTML+CSS+JS معاً)"),
    ("٣", "أدخل الكود", "الصق الكود في المحرر مع دعم أرقام الأسطر ومفتاح Tab"),
    ("٤", "أرفق ملف (اختياري)", "يمكن رفع ملف مرفق بصيغة أي امتداد"),
    ("٥", "حدد حالة النشر", "✓ نشر مباشر: يظهر للزوار فور الحفظ"),
    ("٦", "اضغط 'نشر'", "سيظهر الكود في صفحة الزوار إذا كانت حالته 'منشور'"),
]
col = W/2 - 0.9*cm
for i, (num, t, b) in enumerate(steps):
    sx = 1.8*cm if i % 2 == 0 else col
    if i % 2 == 0 and i > 0:
        y -= 2.4*cm
    sw = col - 1.8*cm - 0.4*cm
    draw_rect(c, sx, y-1.95*cm, sw, 2.05*cm, fill=CARD_BG, stroke=BORDER)
    c.setFillColor(BLUE); c.circle(sx+sw-0.65*cm, y-0.6*cm, 11, fill=1)
    c.setFont("AmiriBold", 12); c.setFillColor(WHITE)
    c.drawCentredString(sx+sw-0.65*cm, y-0.67*cm, num)
    draw_text(c, t, sx+sw-1.4*cm, y-0.55*cm, font="AmiriBold", size=10, color=NAVY)
    draw_text(c, b, sx+sw-1.4*cm, y-1.15*cm, size=9, color=GRAY)
y -= 2.4*cm
y -= 0.5*cm

# Management actions
y = section_title(c, "إجراءات إدارة الأكواد", y)
actions = [
    ("معاينة", "يعرض الكود كما يبدو للزوار قبل النشر", BLUE),
    ("تعديل",  "تحميل بيانات الكود في الفورم للتعديل", YELLOW),
    ("إخفاء/نشر", "تبديل حالة النشر بضغطة واحدة", GREEN),
    ("تصفير",  "إعادة عدادات النسخ والتفاعل إلى الصفر", HexColor("#7c3aed")),
    ("حذف",    "حذف الكود نهائياً بعد تأكيد في نافذة تنبيه", RED),
]
bw = (W-3.6*cm) / len(actions) - 0.25*cm
bx = W - 1.8*cm
for act, desc, color in actions:
    draw_rect(c, bx-bw, y-1.5*cm, bw, 1.6*cm, fill=CARD_BG, stroke=color, radius=6)
    c.setFillColor(color); c.circle(bx-bw/2, y-0.45*cm, 8, fill=1)
    draw_text(c, act, bx-0.15*cm, y-0.4*cm, font="AmiriBold", size=9, color=color)
    draw_text(c, desc, bx-0.15*cm, y-1.05*cm, size=7.5, color=GRAY)
    bx -= bw + 0.25*cm
y -= 2*cm

footer(c, 4, TOTAL_PAGES)
c.showPage()

# ───────────────────────────────────────────────────
# PAGE 5  — ADMIN GUIDE (2) + FULL TYPE
# ───────────────────────────────────────────────────
c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(0, H-0.5*cm, W, H-0.5*cm)
y = H - 1.8*cm

draw_text(c, "٥. دليل لوحة الإدارة — تكملة", W-2*cm, y, font="AmiriBold", size=18, color=NAVY)
y -= 0.4*cm; h_line(c, y); y -= 0.9*cm

# FULL type
y = section_title(c, "نوع 'كاملة' (HTML + CSS + JS)", y)
draw_rect(c, 1.8*cm, y-3.5*cm, W-3.6*cm, 3.7*cm, fill=HexColor("#f0fdf4"), stroke=GREEN, radius=8)
intro_lines = [
    "النوع 'كاملة' مصمم لنشر مشاريع ويب متكاملة تجمع HTML و CSS و JavaScript في ملف واحد.",
    "",
    "كيف يعمل:",
    "١. اختر 'كاملة' من أزرار اللغة.",
    "٢. ستظهر ثلاثة محررات منفصلة: HTML (أحمر) · CSS (أزرق) · JS (أصفر).",
    "٣. بعد النشر، يُخزَّن الكود داخلياً بصيغة JSON.",
    "٤. الزائر يرى زر 'تحميل الكود كاملاً (.html)' ويحصل على ملف HTML جاهز للتشغيل.",
]
ly = y - 0.55*cm
for ln in intro_lines:
    color_l = GREEN if ln.startswith("كيف") else (NAVY if ln.startswith("١") or ln.startswith("٢") or ln.startswith("٣") or ln.startswith("٤") else black)
    fnt = "AmiriBold" if ln.startswith("كيف") else "Amiri"
    draw_text(c, ln, W-2.2*cm, ly, font=fnt, size=10.5, color=color_l)
    ly -= 0.55*cm
y -= 4.2*cm

# Stats dashboard
y = section_title(c, "لوحة الإحصائيات", y)
stats_items = [
    ("إجمالي الأكواد", "عدد جميع الأكواد (منشورة + مسودات)", NAVY),
    ("منشور", "عدد الأكواد المرئية للزوار حالياً", GREEN),
    ("مرات النسخ", "إجمالي عدد مرات نسخ/تحميل الأكواد", BLUE),
    ("تفاعل", "إجمالي الإعجابات على جميع الأكواد", RED),
]
sw2 = (W-3.6*cm)/4 - 0.2*cm
sx2 = W - 1.8*cm
for title_s, desc_s, color_s in stats_items:
    draw_rect(c, sx2-sw2, y-1.5*cm, sw2, 1.6*cm, fill=CARD_BG, stroke=BORDER, radius=6)
    c.setFillColor(color_s); c.rect(sx2-sw2, y-1.5*cm, 0.2*cm, 1.6*cm, fill=1, stroke=0)
    draw_text(c, title_s, sx2-0.4*cm, y-0.55*cm, font="AmiriBold", size=9.5, color=color_s)
    draw_text(c, desc_s, sx2-0.4*cm, y-1.1*cm, size=8.5, color=GRAY)
    sx2 -= sw2 + 0.2*cm
y -= 2.1*cm

# Search & Filter
y = section_title(c, "البحث والتصفية", y)
draw_rect(c, 1.8*cm, y-2*cm, W-3.6*cm, 2.15*cm, fill=CARD_BG, stroke=BORDER)
items_sf = [
    "حقل البحث: يبحث في العنوان والوصف والتصنيف معاً.",
    "أزرار التصفية: الكل · HTML · CSS · JS · كاملة — لعرض نوع محدد فقط.",
    "الترقيم: القائمة تعرض 8 أكواد لكل صفحة مع أزرار التنقل في الأسفل.",
]
ly = y - 0.55*cm
for itm in items_sf:
    c.setFillColor(BLUE); c.circle(W-2.2*cm, ly+0.18*cm, 3, fill=1)
    draw_text(c, itm, W-2.4*cm, ly, size=10.5)
    ly -= 0.65*cm
y -= 2.6*cm

footer(c, 5, TOTAL_PAGES)
c.showPage()

# ───────────────────────────────────────────────────
# PAGE 6  — SYSTEM ARCHITECTURE + FAQ
# ───────────────────────────────────────────────────
c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(0, H-0.5*cm, W, H-0.5*cm)
y = H - 1.8*cm

draw_text(c, "٦. بنية النظام والأسئلة الشائعة", W-2*cm, y, font="AmiriBold", size=18, color=NAVY)
y -= 0.4*cm; h_line(c, y); y -= 0.9*cm

y = section_title(c, "بنية النظام (Architecture)", y)

# Architecture diagram (simplified)
box_h = 1*cm; gap = 0.8*cm
boxes = [
    ("المتصفح (React)", BLUE, W-3*cm),
    ("Supabase Client (anon key)", HexColor("#0891b2"), W-3*cm),
    ("قاعدة البيانات PostgreSQL", GREEN, W-3*cm),
]
bw3 = 5.5*cm
# Left flow: public
draw_rect(c, W-3*cm-bw3, y, bw3, box_h, fill=BLUE, radius=5)
draw_text(c, "الزائر: قراءة الأكواد", W-3*cm-0.3*cm, y+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
c.setStrokeColor(BLUE); c.setLineWidth(1.5)
c.line(W-3*cm-bw3/2, y, W-3*cm-bw3/2, y-gap)
draw_rect(c, W-3*cm-bw3, y-gap-box_h, bw3, box_h, fill=HexColor("#0891b2"), radius=5)
draw_text(c, "Supabase JS Client", W-3*cm-0.3*cm, y-gap-box_h+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
c.line(W-3*cm-bw3/2, y-gap-box_h, W-3*cm-bw3/2, y-2*gap-box_h)
draw_rect(c, W-3*cm-bw3, y-2*gap-2*box_h, bw3, box_h, fill=GREEN, radius=5)
draw_text(c, "PostgreSQL (RLS)", W-3*cm-0.3*cm, y-2*gap-2*box_h+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
draw_text(c, "قراءة عامة (anon key)", W-3*cm-0.3*cm, y-3*gap-2*box_h-0.1*cm, size=8.5, color=GRAY)

# Right flow: admin
ax = W/2 - 1*cm
draw_rect(c, ax-bw3, y, bw3, box_h, fill=NAVY, radius=5)
draw_text(c, "المدير: لوحة الإدارة", ax-0.3*cm, y+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
c.setStrokeColor(NAVY); c.line(ax-bw3/2, y, ax-bw3/2, y-gap)
draw_rect(c, ax-bw3, y-gap-box_h, bw3, box_h, fill=HexColor("#7c3aed"), radius=5)
draw_text(c, "Edge Function (admin-snippets)", ax-0.3*cm, y-gap-box_h+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
c.line(ax-bw3/2, y-gap-box_h, ax-bw3/2, y-2*gap-box_h)
draw_rect(c, ax-bw3, y-2*gap-2*box_h, bw3, box_h, fill=GREEN, radius=5)
draw_text(c, "PostgreSQL (service role)", ax-0.3*cm, y-2*gap-2*box_h+0.28*cm, font="AmiriBold", size=9.5, color=WHITE)
draw_text(c, "كتابة بصلاحية كاملة (service key)", ax-0.3*cm, y-3*gap-2*box_h-0.1*cm, size=8.5, color=GRAY)

y -= 3*gap + 2*box_h + 1.2*cm

# FAQ
y = section_title(c, "الأسئلة الشائعة", y)
faqs = [
    ("كيف يعمل نظام المصادقة في الإدارة؟",
     "لا يوجد JWT أو جلسة. يُرسَل رمز ثابت مع كل طلب للـ Edge Function التي تتحقق منه قبل تنفيذ أي عملية."),
    ("كيف تُحسب مرات النسخ؟",
     "عند نسخ أو تحميل أي كود تُستدعى دالة SQL (increment_snippet_views) تزيد العداد بمقدار 1."),
    ("كيف يعمل نظام الإعجابات؟",
     "يُخزَّن معرّف الأكواد المُعجَب بها في localStorage. كل جهاز يمكنه الإعجاب مرة واحدة فقط بكل كود."),
    ("كيف تُحفظ الأكواد الكاملة (FULL)؟",
     "تُخزَّن كـ JSON: {\"html\":\"...\",\"css\":\"...\",\"js\":\"...\"} في حقل code. عند التحميل يُولَّد ملف HTML كامل."),
    ("كيف يُنشر الموقع تلقائياً؟",
     "Vercel يراقب فرع main في GitHub. عند كل دمج يُشغَّل بناء تلقائي ويُنشر خلال دقيقة."),
    ("لماذا لا تحتاج لإنشاء حساب لرؤية الأكواد؟",
     "سياسة RLS في Supabase تسمح للـ anon role بقراءة الأكواد المنشورة فقط، دون الحاجة لأي مصادقة."),
]
for q, a in faqs:
    draw_rect(c, 1.8*cm, y-1.45*cm, W-3.6*cm, 1.55*cm, fill=CARD_BG, stroke=BORDER, radius=5)
    c.setFillColor(BLUE); c.rect(W-1.8*cm, y-1.45*cm, 0.25*cm, 1.55*cm, fill=1, stroke=0)
    draw_text(c, q, W-2.2*cm, y-0.45*cm, font="AmiriBold", size=10, color=NAVY)
    draw_text(c, a, W-2.2*cm, y-1.05*cm, size=9.5, color=GRAY)
    y -= 1.7*cm

footer(c, 6, TOTAL_PAGES)
c.showPage()

c.save()
print(f"PDF saved: {OUT}")
