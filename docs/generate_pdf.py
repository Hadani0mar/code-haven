"""
منصتي — توثيق شامل لمشروع التخرج
Comprehensive graduation project documentation PDF
"""
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# ── Fonts ──────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Amiri",     "/tmp/Amiri-Regular.ttf"))
pdfmetrics.registerFont(TTFont("AmiriBold", "/tmp/Amiri-Bold.ttf"))

# ── Colors ─────────────────────────────────────────────────────────────────
NAVY      = HexColor("#1a2e52")
BLUE      = HexColor("#1d4ed8")
LIGHT_BG  = HexColor("#eff6ff")
CARD_BG   = HexColor("#f8fafc")
BORDER    = HexColor("#cbd5e1")
GREEN     = HexColor("#16a34a")
GREEN_BG  = HexColor("#f0fdf4")
RED       = HexColor("#dc2626")
RED_BG    = HexColor("#fef2f2")
YELLOW    = HexColor("#ca8a04")
YELLOW_BG = HexColor("#fefce8")
PURPLE    = HexColor("#7c3aed")
PURPLE_BG = HexColor("#faf5ff")
CYAN      = HexColor("#0891b2")
GRAY      = HexColor("#64748b")
LGRAY     = HexColor("#94a3b8")
WHITE     = white

W, H = A4
MARGIN = 2.0 * cm
INNER_W = W - 2 * MARGIN

OUT = "/home/user/code-haven/docs/منصتي-توثيق-المشروع.pdf"
TOTAL_PAGES = 16


# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def txt(c, text, x, y, font="Amiri", size=11, color=black, align="right"):
    c.setFont(font, size)
    c.setFillColor(color)
    s = ar(text)
    if align == "right":
        c.drawRightString(x, y, s)
    elif align == "center":
        c.drawCentredString(x, y, s)
    else:
        c.drawString(x, y, s)

def rect(c, x, y, w, h, fill=None, stroke=None, radius=4):
    c.setFillColor(fill or WHITE)
    c.setStrokeColor(stroke or BORDER)
    c.roundRect(x, y, w, h, radius,
                fill=1 if fill else 0,
                stroke=1 if stroke else 0)

def hline(c, y, color=BORDER, lw=0.5, x1=None, x2=None):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1 or MARGIN, y, x2 or (W - MARGIN), y)

def section_bar(c, title, y, color=NAVY):
    """Draws a section header bar; returns new y below it."""
    rect(c, MARGIN, y - 0.38*cm, INNER_W, 0.88*cm,
         fill=LIGHT_BG, stroke=BORDER, radius=4)
    c.setFillColor(color)
    c.setLineWidth(4)
    c.line(W - MARGIN, y - 0.38*cm, W - MARGIN, y + 0.5*cm)
    txt(c, title, W - MARGIN - 0.25*cm, y + 0.08*cm,
        font="AmiriBold", size=13, color=color)
    return y - 1.25*cm

def bullet_line(c, text, y, indent=0, color=BLUE, size=10.5, bold=False):
    c.setFillColor(color)
    c.circle(W - MARGIN - indent - 0.3*cm, y + 0.18*cm, 3, fill=1)
    txt(c, text, W - MARGIN - indent - 0.55*cm, y,
        font="AmiriBold" if bold else "Amiri", size=size)
    return y - 0.65*cm

def check_line(c, text, y, color=GREEN, size=10.5):
    c.setFont("Amiri", size)
    c.setFillColor(color)
    c.drawRightString(W - MARGIN - 0.15*cm, y, "✓")
    txt(c, text, W - MARGIN - 0.6*cm, y, size=size)
    return y - 0.68*cm

def info_box(c, lines, y, bg=LIGHT_BG, border=BLUE, h_extra=0):
    total_h = len([l for l in lines if l is not None]) * 0.62*cm + 0.5*cm + h_extra
    rect(c, MARGIN, y - total_h, INNER_W, total_h,
         fill=bg, stroke=border, radius=6)
    ly = y - 0.45*cm
    for line in lines:
        if line is None:
            ly -= 0.25*cm
            continue
        is_bold = line.startswith("**") and line.endswith("**")
        t = line.strip("*")
        txt(c, t, W - MARGIN - 0.35*cm, ly,
            font="AmiriBold" if is_bold else "Amiri",
            size=10.5, color=NAVY if is_bold else black)
        ly -= 0.62*cm
    return y - total_h - 0.35*cm

def page_header(c, title=""):
    c.setFillColor(NAVY)
    c.rect(0, H - 0.8*cm, W, 0.8*cm, fill=1, stroke=0)
    if title:
        txt(c, title, W - MARGIN, H - 0.55*cm,
            font="AmiriBold", size=9, color=WHITE)
    txt(c, "منصتي — توثيق مشروع التخرج", MARGIN + 4*cm, H - 0.55*cm,
        font="Amiri", size=9, color=LGRAY, align="left")

def footer(c, page_num):
    hline(c, 1.6*cm, BORDER, 0.5)
    txt(c, "منصتي — منصة ليبية لمشاركة الأكواد البرمجية",
        W - MARGIN, 1.0*cm, size=8, color=GRAY)
    txt(c, f"صفحة {page_num} من {TOTAL_PAGES}",
        MARGIN + 1*cm, 1.0*cm, size=8, color=GRAY, align="left")
    txt(c, "جميع الحقوق محفوظة © 2026",
        W / 2, 1.0*cm, size=8, color=LGRAY, align="center")

def new_page(c, page_num, section_title_str=""):
    c.showPage()
    page_header(c, section_title_str)
    footer(c, page_num)
    return H - 1.5*cm

def table_row(c, cells, col_widths, y, row_h=0.5*cm, bg=CARD_BG,
              header=False, colors=None):
    x = W - MARGIN
    rect(c, MARGIN, y - row_h, INNER_W, row_h,
         fill=NAVY if header else bg,
         stroke=BORDER, radius=0)
    for i, (cell, cw) in enumerate(zip(cells, col_widths)):
        color = WHITE if header else (colors[i] if colors else black)
        font = "AmiriBold" if header else "Amiri"
        txt(c, cell, x - 0.15*cm, y - row_h + 0.13*cm,
            font=font, size=9, color=color)
        x -= cw
    return y - row_h


# ═══════════════════════════════════════════════════════════════════════════
#  DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("منصتي - توثيق شامل لمشروع التخرج")
c.setAuthor("منصتي")
c.setSubject("توثيق تقني وإداري شامل")


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Decorative gradient circles
for i, (cx_, cy_, r_, alpha) in enumerate([
    (W + 20, H + 20, 220, "#1e3a6e"),
    (-20, -20, 150, "#162447"),
    (W/2, H*0.35, 260, "#0f2140"),
]):
    c.setFillColor(HexColor(alpha))
    c.circle(cx_, cy_, r_, fill=1, stroke=0)

# Thin ring
c.setStrokeColor(BLUE)
c.setLineWidth(0.8)
c.circle(W/2, H*0.55, 195, fill=0, stroke=1)
c.setStrokeColor(HexColor("#1e3a6e"))
c.circle(W/2, H*0.55, 210, fill=0, stroke=1)

# Logo box
rect(c, W/2 - 2.3*cm, H - 10.5*cm, 4.6*cm, 4.6*cm,
     fill=HexColor("#0f2140"), stroke=BLUE, radius=16)
txt(c, "</> ", W/2, H - 8.6*cm,
    font="AmiriBold", size=32, color=WHITE, align="center")

# Title
txt(c, "منصتي", W/2, H - 12*cm,
    font="AmiriBold", size=48, color=WHITE, align="center")
txt(c, "منصة ليبية متخصصة في مشاركة الأكواد البرمجية",
    W/2, H - 13.3*cm, font="Amiri", size=15, color=HexColor("#93c5fd"), align="center")

# Divider
c.setStrokeColor(BLUE)
c.setLineWidth(1.5)
c.line(W/2 - 7*cm, H - 14.3*cm, W/2 + 7*cm, H - 14.3*cm)

# Subtitle
txt(c, "توثيق شامل لمشروع التخرج",
    W/2, H - 15.3*cm, font="AmiriBold", size=17, color=HexColor("#e2e8f0"), align="center")
txt(c, "يشمل: الدليل التقني · دليل الإدارة · قاعدة البيانات · البنية المعمارية · الأسئلة الشائعة",
    W/2, H - 16.3*cm, font="Amiri", size=10.5, color=HexColor("#94a3b8"), align="center")

# Bottom info bar
c.setFillColor(BLUE)
c.rect(0, 0, W, 3.5*cm, fill=1, stroke=0)

# Info chips
info_items = [("التقنية", "React + Supabase"), ("النوع", "مشروع تخرج"), ("السنة", "2026")]
chip_w = 4.5*cm
chip_x = W/2 + (len(info_items) - 1) * chip_w / 2
for label, value in info_items:
    rect(c, chip_x - chip_w + 0.2*cm, 1.6*cm, chip_w - 0.4*cm, 1.3*cm,
         fill=HexColor("#1e40af"), stroke=HexColor("#3b5bdb"), radius=6)
    txt(c, label, chip_x - 0.25*cm, 2.55*cm, font="Amiri", size=8, color=HexColor("#93c5fd"))
    txt(c, value, chip_x - 0.25*cm, 1.95*cm, font="AmiriBold", size=9.5, color=WHITE)
    chip_x -= chip_w

footer(c, 1)
c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 2 — TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "فهرس المحتويات")
footer(c, 2)
y = H - 1.8*cm

txt(c, "فهرس المحتويات", W - MARGIN, y,
    font="AmiriBold", size=20, color=NAVY)
y -= 0.4*cm
hline(c, y)
y -= 0.8*cm

toc_items = [
    ("١. نظرة عامة على المشروع",                  "3"),
    ("   • وصف المشروع وأهدافه",                   "3"),
    ("   • الجمهور المستهدف",                       "3"),
    ("   • مشكلة المشروع والحل المقترح",            "3"),
    ("٢. المميزات الرئيسية",                        "4"),
    ("   • مميزات الزائر العام",                    "4"),
    ("   • مميزات لوحة الإدارة",                   "4"),
    ("٣. التقنيات المستخدمة",                       "5"),
    ("   • الواجهة الأمامية",                       "5"),
    ("   • الخدمات الخلفية",                        "5"),
    ("   • أدوات التطوير والنشر",                   "5"),
    ("٤. لماذا Supabase؟",                          "6"),
    ("٥. الأمان وآلية المصادقة",                   "7"),
    ("٦. قاعدة البيانات",                           "8"),
    ("   • جدول الأكواد (snippets)",                "8"),
    ("   • دوال SQL المخصصة",                      "8"),
    ("   • سياسات الأمان (RLS)",                   "8"),
    ("٧. بنية النظام (Architecture)",               "9"),
    ("   • تدفق القراءة العامة",                    "9"),
    ("   • تدفق العمليات الإدارية",                 "9"),
    ("٨. واجهة الزائر العام",                       "10"),
    ("٩. دليل لوحة الإدارة — الأساسيات",           "11"),
    ("   • الدخول ونشر كود جديد",                  "11"),
    ("   • أنواع الأكواد",                          "11"),
    ("١٠. دليل لوحة الإدارة — الإدارة والتحكم",    "12"),
    ("    • إجراءات الأكواد",                       "12"),
    ("    • البحث والتصفية والترقيم",               "12"),
    ("    • لوحة الإحصائيات",                       "12"),
    ("١١. نوع 'كاملة' — مشاريع HTML+CSS+JS",       "13"),
    ("١٢. الاستضافة والنشر التلقائي",               "14"),
    ("١٣. الأسئلة الشائعة",                         "15"),
    ("١٤. الخاتمة والتطوير المستقبلي",              "16"),
]

for item, page in toc_items:
    is_section = item[0] in "١٢٣٤٥٦٧٨٩" or (len(item) > 2 and item[1] in "٠١٢٣٤٥٦٧٨٩")
    is_sub = item.startswith("   ")

    if is_section and not is_sub:
        y -= 0.15*cm
        txt(c, item.strip(), W - MARGIN, y,
            font="AmiriBold", size=11, color=NAVY)
        # Dotted leader
        dots_x = MARGIN + 1.8*cm
        c.setStrokeColor(LGRAY)
        c.setLineWidth(0.5)
        c.setDash([1, 4])
        c.line(dots_x, y + 0.15*cm, W - MARGIN - len(item.strip())*4.5 - 0.5*cm, y + 0.15*cm)
        c.setDash([])
        txt(c, page, MARGIN + 1.5*cm, y, font="AmiriBold", size=11, color=BLUE, align="left")
        y -= 0.68*cm
    else:
        txt(c, item.strip(), W - MARGIN - 0.5*cm, y,
            font="Amiri", size=10, color=GRAY)
        txt(c, page, MARGIN + 1.5*cm, y, font="Amiri", size=10, color=LGRAY, align="left")
        y -= 0.56*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 3 — PROJECT OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "نظرة عامة على المشروع")
footer(c, 3)
y = H - 1.8*cm

txt(c, "١. نظرة عامة على المشروع", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "وصف المشروع", y)
overview_lines = [
    "**منصتي** هي منصة ويب عربية تُتيح للمطورين العرب تبادل أكواد HTML و CSS و JavaScript",
    "بشكل منظّم وسهل الوصول. تتميز المنصة بدعمها الكامل للغة العربية وتصميمها الموجّه",
    "من اليمين إلى اليسار (RTL)، مما يجعلها الأولى من نوعها في البيئة العربية.",
    None,
    "**الفكرة الأساسية:** يتولى فريق المنصة اختيار الأكواد وفلترتها قبل نشرها، مما يضمن",
    "جودة المحتوى وملاءمته للمجتمع. ويستطيع الزوار تصفّح الأكواد ونسخها وتحميلها",
    "بدون أي تسجيل أو اشتراك.",
]
y = info_box(c, overview_lines, y, bg=LIGHT_BG, border=BLUE)
y -= 0.3*cm

y = section_bar(c, "مشكلة المشروع والحل المقترح", y)

# Problem vs Solution two columns
half = (INNER_W - 0.4*cm) / 2
rect(c, MARGIN, y - 3.8*cm, half, 4*cm, fill=RED_BG, stroke=RED, radius=6)
rect(c, MARGIN + half + 0.4*cm, y - 3.8*cm, half, 4*cm, fill=GREEN_BG, stroke=GREEN, radius=6)

txt(c, "المشكلة", W - MARGIN - 0.35*cm, y - 0.4*cm,
    font="AmiriBold", size=11, color=RED)
txt(c, "الحل المقترح", MARGIN + half + 0.4*cm + half - 0.35*cm, y - 0.4*cm,
    font="AmiriBold", size=11, color=GREEN)

problems = [
    "غياب منصة عربية متخصصة للأكواد",
    "صعوبة إيجاد أكواد موثوقة وجاهزة",
    "الحواجز اللغوية للمطورين العرب",
    "تشتت الأكواد عبر منصات متعددة",
    "عدم وجود تصنيف منظّم للأكواد",
]
solutions = [
    "منصة عربية موحدة ومتخصصة",
    "فريق متخصص يختار ويراجع الأكواد",
    "واجهة عربية RTL بالكامل",
    "مكان واحد يجمع أنواع الأكواد",
    "تصنيف بـ HTML / CSS / JS / كاملة",
]
py = y - 0.9*cm
for prob, sol in zip(problems, solutions):
    c.setFillColor(RED)
    c.circle(W - MARGIN - 0.4*cm, py + 0.18*cm, 3, fill=1)
    txt(c, prob, W - MARGIN - 0.65*cm, py, size=9.5, color=HexColor("#991b1b"))
    c.setFillColor(GREEN)
    c.circle(MARGIN + half + 0.4*cm + half - 0.4*cm, py + 0.18*cm, 3, fill=1)
    txt(c, sol, MARGIN + half + 0.4*cm + half - 0.65*cm, py, size=9.5, color=HexColor("#14532d"))
    py -= 0.62*cm
y -= 4.4*cm

y = section_bar(c, "الجمهور المستهدف", y)
audiences = [
    ("المطورون المبتدئون", "يبحثون عن أكواد جاهزة للتعلم والتطبيق", BLUE),
    ("مطورو الويب المحترفون", "يحتاجون إلى مرجع سريع للأكواد الشائعة", NAVY),
    ("طلاب البرمجة", "يستفيدون من الأكواد في مشاريعهم الدراسية", GREEN),
    ("مصممو الويب", "يبحثون عن مقاطع CSS جاهزة للتنسيق", PURPLE),
]
aw = (INNER_W - 0.6*cm) / 4
ax = W - MARGIN
for title_a, desc_a, color_a in audiences:
    rect(c, ax - aw, y - 1.8*cm, aw, 1.9*cm, fill=CARD_BG, stroke=BORDER, radius=6)
    c.setFillColor(color_a)
    c.circle(ax - aw/2, y - 0.45*cm, 12, fill=1)
    txt(c, title_a, ax - 0.2*cm, y - 0.38*cm,
        font="AmiriBold", size=8.5, color=color_a)
    txt(c, desc_a, ax - 0.2*cm, y - 1.1*cm, size=8, color=GRAY)
    ax -= aw + 0.2*cm
y -= 2.4*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 4 — KEY FEATURES
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "المميزات الرئيسية")
footer(c, 4)
y = H - 1.8*cm

txt(c, "٢. المميزات الرئيسية", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "مميزات الزائر العام", y, color=BLUE)

visitor_features = [
    ("تصفح الأكواد بدون تسجيل", "أي زائر يستطيع مشاهدة الأكواد المنشورة فور دخوله الموقع دون أي حساب"),
    ("نسخ الكود بضغطة واحدة", "زر 'نسخ الكود' ينقل الكود مباشرة إلى الحافظة مع عداد يتتبع عدد النسخ"),
    ("تحميل ملفات مرفقة", "بعض الأكواد تأتي مع ملفات قابلة للتحميل المباشر"),
    ("تحميل مشاريع كاملة", "أكواد النوع 'كاملة' تُحمَّل كملف HTML واحد جاهز للتشغيل في المتصفح"),
    ("التفاعل والإعجاب", "كل زائر يستطيع التفاعل مع الأكواد مرة واحدة لكل كود من نفس الجهاز"),
    ("تصفية حسب النوع", "أزرار تصفية سريعة: الكل / HTML / CSS / JS / كاملة"),
    ("واجهة عربية كاملة", "تصميم RTL بخط Cairo العربي مع ألوان وأنماط مخصصة"),
    ("شاشة ترحيب", "شاشة بداية أنيمشن جاري التحميل مدة 10 ثواني"),
    ("تأثير الهيكل (Skeleton)", "أثناء تحميل الأكواد تظهر بطاقات هيكلية متحركة بدل الفراغ"),
]
for i, (feat, desc) in enumerate(visitor_features):
    bg = CARD_BG if i % 2 == 0 else WHITE
    rect(c, MARGIN, y - 0.6*cm, INNER_W, 0.68*cm, fill=bg, stroke=BORDER, radius=3)
    c.setFillColor(BLUE)
    c.circle(W - MARGIN - 0.3*cm, y - 0.24*cm, 4, fill=1)
    txt(c, feat, W - MARGIN - 0.6*cm, y - 0.35*cm,
        font="AmiriBold", size=10, color=NAVY)
    txt(c, desc, W / 2 + 0.5*cm, y - 0.35*cm, size=9.5, color=GRAY)
    y -= 0.68*cm
y -= 0.5*cm

y = section_bar(c, "مميزات لوحة الإدارة", y, color=NAVY)

admin_features = [
    ("نشر أكواد بأنواع متعددة", "HTML / CSS / JS / كاملة (مشاريع ثلاثية مدمجة)", NAVY),
    ("معاينة قبل النشر", "نافذة Preview تعرض الكود كما يراه الزائر تماماً", BLUE),
    ("محرر كود متقدم", "محرر مع أرقام الأسطر ودعم مفتاح Tab لمسافة الإدراج", PURPLE),
    ("رفع الملفات", "رفع أي ملف مرفق يُخزَّن في Supabase Storage وينتج رابطاً دائماً", CYAN),
    ("التحكم في النشر", "تبديل حالة أي كود بين منشور / مخفي بنقرة واحدة", GREEN),
    ("تصفير العدادات", "إعادة عدادات النسخ والتفاعل لأي كود إلى الصفر", YELLOW),
    ("حذف آمن", "نافذة تأكيد تمنع الحذف العرضي مع تحذير واضح", RED),
    ("البحث متعدد الحقول", "يبحث في العنوان والوصف والتصنيف في آن واحد", NAVY),
    ("الترقيم (8 لكل صفحة)", "قائمة مرقمة تعرض 8 أكواد لكل صفحة مع أزرار تنقل", BLUE),
    ("لوحة إحصائيات", "تعرض الأكواد الكلية والمنشورة ومجموع النسخ والتفاعلات", GREEN),
]
for i, (feat, desc, color) in enumerate(admin_features):
    bg = CARD_BG if i % 2 == 0 else WHITE
    rect(c, MARGIN, y - 0.6*cm, INNER_W, 0.68*cm, fill=bg, stroke=BORDER, radius=3)
    c.setFillColor(color)
    c.circle(W - MARGIN - 0.3*cm, y - 0.24*cm, 4, fill=1)
    txt(c, feat, W - MARGIN - 0.6*cm, y - 0.35*cm,
        font="AmiriBold", size=10, color=color)
    txt(c, desc, W / 2 + 0.5*cm, y - 0.35*cm, size=9.5, color=GRAY)
    y -= 0.68*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 5 — TECH STACK
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "التقنيات المستخدمة")
footer(c, 5)
y = H - 1.8*cm

txt(c, "٣. التقنيات المستخدمة", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "الواجهة الأمامية (Frontend)", y, color=BLUE)

front_techs = [
    ("React 18", BLUE,
     "مكتبة JavaScript لبناء واجهات مستخدم تفاعلية باستخدام المكونات (Components).",
     "تُستخدم لبناء جميع مكونات الصفحة: الكروت، الأزرار، لوحة الإدارة."),
    ("TypeScript", HexColor("#3178c6"),
     "إضافة الأنواع الثابتة إلى JavaScript لمنع الأخطاء وتحسين تجربة التطوير.",
     "يضمن أن بيانات قاعدة البيانات تُستخدم بالشكل الصحيح في كل مكوّن."),
    ("Vite", HexColor("#646cff"),
     "أداة بناء حديثة تعتمد على ESM وتوفر تحديثاً فورياً أثناء التطوير (HMR).",
     "تُسرّع دورة التطوير وتولّد بنية إنتاج مُحسَّنة وصغيرة الحجم."),
    ("Tailwind CSS", CYAN,
     "إطار CSS مبني على الـ utility classes يُمكّن من التنسيق مباشرة في HTML.",
     "يُوفّر نظام ألوان وظلال وحركات مخصصة للمنصة."),
    ("shadcn/ui", PURPLE,
     "مكتبة مكونات UI قابلة للتخصيص مبنية على Radix UI + Tailwind CSS.",
     "تُوفّر أزرار، نوافذ حوار، نوافذ تنبيه، وغيرها من مكونات جاهزة وقابلة للوصول."),
    ("React Router v6", HexColor("#e11d48"),
     "مكتبة التوجيه الجانب العميل (Client-Side Routing) لصفحة الإدارة والصفحة الرئيسية.",
     "تُمكّن التنقل بين الصفحات دون إعادة تحميل كاملة للصفحة."),
    ("Lucide React", GRAY,
     "مكتبة أيقونات SVG مفتوحة المصدر مع أكثر من 1000 أيقونة.",
     "تُستخدم لأيقونات النسخ والتحميل والإعجاب وأزرار الإدارة."),
]
for name, color, what, how in front_techs:
    rect(c, MARGIN, y - 1.0*cm, INNER_W, 1.1*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(color)
    c.rect(W - MARGIN - 0.3*cm, y - 1.0*cm, 0.3*cm, 1.1*cm, fill=1, stroke=0)
    txt(c, name, W - MARGIN - 0.6*cm, y - 0.33*cm,
        font="AmiriBold", size=10.5, color=color)
    txt(c, what, W - MARGIN - 0.6*cm, y - 0.68*cm, size=9, color=NAVY)
    txt(c, how,  W/2 - 0.2*cm, y - 0.68*cm, size=9, color=GRAY)
    y -= 1.18*cm
y -= 0.4*cm

y = section_bar(c, "الخدمات الخلفية (Backend & Infrastructure)", y, color=GREEN)

back_techs = [
    ("Supabase", GREEN,
     "منصة Backend-as-a-Service تُوفّر PostgreSQL + Auth + Storage + Edge Functions",
     "تُعفي المشروع من الحاجة لسيرفر مخصص أو إعداد قاعدة بيانات من الصفر"),
    ("Supabase Edge Functions", HexColor("#059669"),
     "دوال سيرفر تعمل على Deno Runtime على شبكة CDN عالمية",
     "تُنفّذ عمليات الإدارة بصلاحية service role لتجاوز سياسات RLS"),
    ("PostgreSQL", HexColor("#336791"),
     "قاعدة بيانات علائقية قوية مع دعم JSON و Row Level Security",
     "تُخزّن الأكواد وبياناتها مع سياسات أمان على مستوى الصف"),
    ("Supabase Storage", HexColor("#10b981"),
     "خدمة تخزين الملفات بروابط عامة دائمة",
     "تُخزّن الملفات المرفقة مع الأكواد في bucket مخصص"),
    ("Vercel", black,
     "منصة استضافة وتوزيع تلقائية لتطبيقات الويب الحديثة",
     "تنشر التطبيق تلقائياً عند كل تحديث في فرع main في GitHub"),
]
for name, color, what, how in back_techs:
    rect(c, MARGIN, y - 0.85*cm, INNER_W, 0.95*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(color)
    c.rect(W - MARGIN - 0.3*cm, y - 0.85*cm, 0.3*cm, 0.95*cm, fill=1, stroke=0)
    txt(c, name, W - MARGIN - 0.6*cm, y - 0.28*cm, font="AmiriBold", size=10.5, color=color)
    txt(c, what, W - MARGIN - 0.6*cm, y - 0.6*cm, size=9, color=NAVY)
    txt(c, how, W/2 - 0.2*cm, y - 0.6*cm, size=9, color=GRAY)
    y -= 1.03*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 6 — WHY SUPABASE
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "لماذا Supabase؟")
footer(c, 6)
y = H - 1.8*cm

txt(c, "٤. لماذا Supabase؟", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

# Intro highlight
rect(c, MARGIN, y - 2.5*cm, INNER_W, 2.7*cm, fill=GREEN_BG, stroke=GREEN, radius=8)
c.setFillColor(GREEN)
c.setLineWidth(5)
c.line(W - MARGIN, y - 2.5*cm, W - MARGIN, y + 0.2*cm)
intro_ar = [
    "Supabase هو بديل مفتوح المصدر لـ Firebase يُوفّر باكيند جاهزاً بالكامل دون الحاجة",
    "لإعداد سيرفر أو كتابة كود خلفي من الصفر. باستخدام Supabase تمكّنّا من التركيز على",
    "بناء تجربة المستخدم بدلاً من إضاعة الوقت في ضبط البنية التحتية.",
]
ly = y - 0.55*cm
for ln in intro_ar:
    txt(c, ln, W - MARGIN - 0.45*cm, ly, size=11, color=HexColor("#14532d"))
    ly -= 0.62*cm
y -= 3.1*cm

reasons = [
    ("١", "قاعدة بيانات PostgreSQL جاهزة للاستخدام",
     GREEN, GREEN_BG,
     "لا حاجة لتثبيت PostgreSQL محلياً أو على سيرفر منفصل. Supabase يُوفّر قاعدة بيانات"
     " كاملة يمكن إدارتها عبر واجهة ويب أو SQL editor."),
    ("٢", "Row Level Security (RLS) — أمان على مستوى الصف",
     BLUE, LIGHT_BG,
     "تُمكّن سياسات RLS من السماح للزوار بقراءة الأكواد المنشورة فقط، ومنع أي"
     " تعديل مباشر من الـ anon key. هذا يحمي البيانات دون كتابة كود تحقق إضافي."),
    ("٣", "Edge Functions — دوال خادمية بدون سيرفر",
     PURPLE, PURPLE_BG,
     "دالة admin-snippets تعمل على Deno Runtime وتُعالج جميع عمليات الإدارة. تُوزَّع"
     " تلقائياً على شبكة CDN عالمية للحصول على أقل تأخير ممكن."),
    ("٤", "Storage — تخزين الملفات مدمج",
     CYAN, HexColor("#ecfeff"),
     "رفع الملفات المرفقة مع الأكواد يتم مباشرة إلى Supabase Storage مع توليد"
     " روابط عامة دائمة يمكن مشاركتها وتحميلها مباشرة."),
    ("٥", "مفاتيح API جاهزة — بدون تعقيد",
     YELLOW, YELLOW_BG,
     "مفتاح anon للقراءة العامة، ومفتاح service role للعمليات الإدارية. يُرسَل"
     " مفتاح الإدارة فقط من Edge Function دون كشفه للمتصفح."),
    ("٦", "الطبقة المجانية كافية للمشروع",
     GREEN, GREEN_BG,
     "حد 500MB لقاعدة البيانات، 1GB للملفات، و500K استدعاء للـ Edge Functions شهرياً"
     " — تكفي تماماً لمشروع التخرج والإطلاق الأولي بدون أي تكلفة."),
]
for num, title_r, color_r, bg_r, detail in reasons:
    rect(c, MARGIN, y - 2.0*cm, INNER_W, 2.15*cm, fill=bg_r, stroke=color_r, radius=6)
    c.setFillColor(color_r)
    c.circle(W - MARGIN - 0.5*cm, y - 0.65*cm, 12, fill=1)
    c.setFont("AmiriBold", 12)
    c.setFillColor(WHITE)
    c.drawCentredString(W - MARGIN - 0.5*cm, y - 0.72*cm, num)
    txt(c, title_r, W - MARGIN - 1.2*cm, y - 0.5*cm,
        font="AmiriBold", size=11, color=color_r)
    txt(c, detail, W - MARGIN - 0.45*cm, y - 1.15*cm, size=9.5, color=GRAY)
    y -= 2.35*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 7 — SECURITY & AUTH
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "الأمان وآلية المصادقة")
footer(c, 7)
y = H - 1.8*cm

txt(c, "٥. الأمان وآلية المصادقة", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "نموذج المصادقة الإدارية", y, color=NAVY)
y = info_box(c, [
    "**لا يوجد JWT أو جلسة مستخدم — نظام رمز مشترك مبسّط**",
    None,
    "يُخزَّن رمز الإدارة في localStorage تحت المفتاح admin_code.",
    "يُرسَل مع كل طلب إداري ضمن جسم JSON: { code, action, payload }.",
    "تتحقق Edge Function من الرمز قبل تنفيذ أي عملية.",
    "إذا كان الرمز خاطئاً تُرجع الدالة خطأ 401 Unauthorized فوراً.",
], y, bg=YELLOW_BG, border=YELLOW)
y -= 0.4*cm

# Auth flow diagram
y = section_bar(c, "مخطط تدفق المصادقة", y, color=NAVY)
flow_steps = [
    ("المدير يدخل رمز الإدارة في متصفحه", NAVY),
    ("يُخزَّن في localStorage ويُرسَل مع كل طلب", BLUE),
    ("Edge Function تستقبل { code, action, payload }", PURPLE),
    ("المقارنة مع ADMIN_CODE المخزون في متغيرات البيئة", YELLOW),
    ("مرفوض: ترجع 401", RED),
    ("مقبول: تُنفَّذ العملية بصلاحية service role", GREEN),
]
box_w2 = 7*cm
box_h2 = 0.65*cm
bx2 = W/2 + box_w2/2
for i, (step, color) in enumerate(flow_steps):
    rect(c, bx2 - box_w2, y - box_h2, box_w2, box_h2, fill=color, stroke=color, radius=5)
    txt(c, step, bx2 - 0.25*cm, y - box_h2 + 0.15*cm, font="AmiriBold", size=9, color=WHITE)
    if i < len(flow_steps) - 1 and i != 3:
        c.setStrokeColor(BORDER)
        c.setLineWidth(1.5)
        c.line(W/2, y - box_h2, W/2, y - box_h2 - 0.3*cm)
        c.setFillColor(BORDER)
        p = c.beginPath()
        p.moveTo(W/2 - 4, y - box_h2 - 0.28*cm)
        p.lineTo(W/2 + 4, y - box_h2 - 0.28*cm)
        p.lineTo(W/2, y - box_h2 - 0.42*cm)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    if i == 3:
        # Branch
        c.setStrokeColor(RED)
        c.setLineWidth(1.2)
        c.line(bx2 - box_w2, y - box_h2 - 0.12*cm,
               bx2 - box_w2 - 1.5*cm, y - box_h2 - 0.12*cm)
        rect(c, bx2 - box_w2 - 4.5*cm, y - box_h2 - 0.5*cm, 3*cm, 0.65*cm,
             fill=RED, stroke=RED, radius=5)
        txt(c, "مرفوض → 401", bx2 - box_w2 - 1.5*cm - 0.15*cm, y - box_h2 - 0.28*cm,
            font="AmiriBold", size=9, color=WHITE)
        c.setStrokeColor(BORDER)
        c.setLineWidth(1.5)
        c.line(W/2, y - box_h2, W/2, y - box_h2 - 0.3*cm)
    y -= box_h2 + 0.45*cm
y -= 0.5*cm

y = section_bar(c, "سياسات الأمان (RLS Policies)", y, color=GREEN)
rls_items = [
    ("قراءة الأكواد المنشورة (SELECT)",
     "مسموح للـ anon role بقراءة الصفوف التي published = true فقط",
     GREEN),
    ("منع الكتابة المباشرة (INSERT / UPDATE / DELETE)",
     "محظور تماماً على الـ anon role — العمليات تمر فقط عبر Edge Function",
     RED),
    ("صلاحية service role كاملة",
     "Edge Function تستخدم service key تتجاوز جميع سياسات RLS",
     BLUE),
    ("قراءة / كتابة Storage",
     "الـ bucket مضبوط كـ Public للقراءة، والكتابة فقط عبر service key",
     PURPLE),
]
for policy, desc, color in rls_items:
    rect(c, MARGIN, y - 0.85*cm, INNER_W, 0.95*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(color)
    c.rect(W - MARGIN - 0.3*cm, y - 0.85*cm, 0.3*cm, 0.95*cm, fill=1, stroke=0)
    txt(c, policy, W - MARGIN - 0.6*cm, y - 0.28*cm, font="AmiriBold", size=10, color=color)
    txt(c, desc, W - MARGIN - 0.6*cm, y - 0.6*cm, size=9, color=GRAY)
    y -= 1.03*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 8 — DATABASE SCHEMA
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "قاعدة البيانات")
footer(c, 8)
y = H - 1.8*cm

txt(c, "٦. قاعدة البيانات", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "جدول الأكواد الرئيسي — public.snippets", y)

# Table header
col_w = [INNER_W * 0.42, INNER_W * 0.16, INNER_W * 0.20, INNER_W * 0.22]
y = table_row(c, ["الوصف", "إلزامي؟", "النوع", "العمود"],
              col_w, y, row_h=0.55*cm, header=True)
schema_rows = [
    ("المعرف الفريد يُولَّد تلقائياً",                      "نعم", "UUID",        "id"),
    ("عنوان الكود — يظهر في البطاقة والقائمة",              "نعم", "TEXT",        "title"),
    ("وصف مختصر يظهر أسفل العنوان",                        "لا",  "TEXT",        "description"),
    ("نوع الكود: HTML أو CSS أو JS أو FULL",               "نعم", "TEXT",        "language"),
    ("تصنيف فرعي مثل: نماذج، قوائم، تأثيرات",             "لا",  "TEXT",        "category"),
    ("محتوى الكود أو JSON {html,css,js} للنوع FULL",       "لا",  "TEXT",        "code"),
    ("رابط الملف في Supabase Storage",                      "لا",  "TEXT",        "file_url"),
    ("اسم الملف الأصلي للعرض وعند التحميل",                "لا",  "TEXT",        "file_name"),
    ("عداد مرات النسخ والتحميل — يزيد عبر RPC",            "نعم", "INTEGER",     "views"),
    ("عداد الإعجابات — يزيد عبر RPC",                     "نعم", "INTEGER",     "likes"),
    ("تحديد إن كان الكود مرئياً للزوار أم لا",             "نعم", "BOOLEAN",     "published"),
    ("تاريخ ووقت الإنشاء — يُسجَّل تلقائياً",             "نعم", "TIMESTAMPTZ", "created_at"),
]
for i, (desc, req, typ, col) in enumerate(schema_rows):
    bg = CARD_BG if i % 2 == 0 else WHITE
    req_color = GREEN if req == "نعم" else GRAY
    y = table_row(c, [desc, req, typ, col], col_w, y,
                  row_h=0.48*cm, bg=bg,
                  colors=[black, req_color, BLUE, PURPLE])
y -= 0.5*cm

y = section_bar(c, "دوال SQL المخصصة (Stored Procedures)", y, color=BLUE)
procs = [
    ("increment_snippet_views(snippet_id UUID)",
     "تزيد حقل views بمقدار 1 للصف المحدد — تُستدعى عند النسخ أو التحميل"),
    ("increment_snippet_likes(snippet_id UUID)",
     "تزيد حقل likes بمقدار 1 للصف المحدد — تُستدعى مرة واحدة لكل جهاز"),
]
for proc, desc in procs:
    rect(c, MARGIN, y - 0.85*cm, INNER_W, 0.95*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFont("Amiri", 9.5)
    c.setFillColor(PURPLE)
    c.drawRightString(W - MARGIN - 0.35*cm, y - 0.28*cm, proc)
    txt(c, desc, W/2 - 0.2*cm, y - 0.28*cm, size=9.5, color=GRAY)
    y -= 1.03*cm
y -= 0.4*cm

y = section_bar(c, "ملاحظات تصميمية مهمة", y, color=YELLOW)
notes = [
    "عمود language من نوع TEXT (وليس ENUM) مما يسمح بإضافة أنواع جديدة دون تعديل المخطط",
    "عمود code يقبل JSON كنص عادي — النوع FULL يخزن {\"html\":\"...\",\"css\":\"...\",\"js\":\"...\"}",
    "جدول user_roles ودالة has_role() موجودان لكنهما غير مستخدمَين — بقايا من نظام مصادقة سابق",
    "سياسة RLS تجعل الـ anon key آمناً للاستخدام في المتصفح مباشرة بدون مخاطر أمنية",
]
for note in notes:
    y = bullet_line(c, note, y, color=YELLOW, size=10)

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 9 — ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "بنية النظام")
footer(c, 9)
y = H - 1.8*cm

txt(c, "٧. بنية النظام (System Architecture)", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "نظرة عامة على المكونات", y)
y = info_box(c, [
    "المنصة تتبع نمط Jamstack: واجهة أمامية ثابتة + خدمات خلفية API.",
    "لا يوجد سيرفر تقليدي — كل المنطق الإداري في Edge Function.",
    "القراءة العامة تتم مباشرة من المتصفح إلى Supabase باستخدام الـ anon key.",
], y, bg=LIGHT_BG, border=BLUE)
y -= 0.4*cm

# Two column architecture flows
half2 = (INNER_W - 0.6*cm) / 2

# Left: Public flow
y = section_bar(c, "تدفق القراءة العامة (Visitor Flow)", y, color=BLUE)
rect(c, MARGIN, y - 5.5*cm, half2, 5.7*cm, fill=HexColor("#f0f9ff"), stroke=BLUE, radius=8)
pub_steps = [
    ("المتصفح (React SPA)", BLUE),
    ("supabase-js client", CYAN),
    ("Supabase API Gateway", HexColor("#0284c7")),
    ("RLS: published = true", GREEN),
    ("PostgreSQL — جدول snippets", HexColor("#1e40af")),
]
py2 = y - 0.55*cm
bw4 = half2 - 0.8*cm
bx4 = MARGIN + half2 - 0.3*cm
for i, (label, color) in enumerate(pub_steps):
    rect(c, bx4 - bw4, py2 - 0.5*cm, bw4, 0.55*cm,
         fill=color, stroke=color, radius=4)
    txt(c, label, bx4 - 0.2*cm, py2 - 0.32*cm,
        font="AmiriBold", size=9, color=WHITE)
    if i < len(pub_steps) - 1:
        c.setStrokeColor(BORDER)
        c.setLineWidth(1.2)
        cy4 = bx4 - bw4/2
        c.line(cy4, py2 - 0.5*cm, cy4, py2 - 0.7*cm)
    py2 -= 0.95*cm
txt(c, "anon key فقط",
    MARGIN + half2/2, y - 5.3*cm, size=8.5, color=BLUE, align="center")

# Right: Admin flow
right_x = MARGIN + half2 + 0.6*cm
right_w = half2
rect(c, right_x, y - 5.5*cm, right_w, 5.7*cm, fill=HexColor("#faf5ff"), stroke=PURPLE, radius=8)
adm_steps = [
    ("لوحة الإدارة (Admin Panel)", NAVY),
    ("Edge Function: admin-snippets", PURPLE),
    ("التحقق من رمز الإدارة", YELLOW),
    ("service role key (bypass RLS)", RED),
    ("PostgreSQL — كتابة كاملة", HexColor("#7c3aed")),
]
py3 = y - 0.55*cm
bw5 = right_w - 0.8*cm
bx5 = right_x + right_w - 0.3*cm
for i, (label, color) in enumerate(adm_steps):
    rect(c, bx5 - bw5, py3 - 0.5*cm, bw5, 0.55*cm,
         fill=color, stroke=color, radius=4)
    txt(c, label, bx5 - 0.2*cm, py3 - 0.32*cm,
        font="AmiriBold", size=9, color=WHITE)
    if i < len(adm_steps) - 1:
        c.setStrokeColor(BORDER)
        c.setLineWidth(1.2)
        cy5 = bx5 - bw5/2
        c.line(cy5, py3 - 0.5*cm, cy5, py3 - 0.7*cm)
    py3 -= 0.95*cm
txt(c, "service key — محمي في Edge Function",
    right_x + right_w/2, y - 5.3*cm, size=8.5, color=PURPLE, align="center")

y -= 6.2*cm

y = section_bar(c, "مكونات التطبيق (Component Tree)", y, color=GREEN)
comp_items = [
    ("src/App.tsx",               "نقطة الدخول: splash screen + react-router routes"),
    ("src/pages/Index.tsx",       "الصفحة الرئيسية: تجمع مكونات site/"),
    ("src/pages/Admin.tsx",       "لوحة الإدارة الكاملة — مصادقة + CRUD"),
    ("src/components/SplashScreen.tsx", "شاشة البداية مع progress bar وأنيمشن"),
    ("src/components/site/SnippetsGrid.tsx", "شبكة الأكواد + تصفية + نسخ + تحميل"),
    ("src/integrations/supabase/client.ts", "singleton لـ Supabase client"),
    ("supabase/functions/admin-snippets/index.ts", "Edge Function — Deno runtime"),
]
for path, desc in comp_items:
    rect(c, MARGIN, y - 0.55*cm, INNER_W, 0.62*cm, fill=CARD_BG, stroke=BORDER, radius=3)
    c.setFont("Amiri", 9)
    c.setFillColor(PURPLE)
    c.drawRightString(W - MARGIN - 0.35*cm, y - 0.32*cm, path)
    txt(c, desc, W/2, y - 0.32*cm, size=9, color=GRAY)
    y -= 0.68*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 10 — VISITOR INTERFACE
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "واجهة الزائر العام")
footer(c, 10)
y = H - 1.8*cm

txt(c, "٨. واجهة الزائر العام", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "شاشة البداية (Splash Screen)", y, color=BLUE)
y = info_box(c, [
    "عند فتح الموقع لأول مرة تظهر شاشة ترحيب مدة 10 ثواني تعرض:",
    "• شعار المنصة في المنتصف مع خلفية متدرجة",
    "• شريط تقدم (Progress Bar) يملأ الشاشة تدريجياً",
    "• نقاط متحركة (Bouncing Dots) مع نص 'جاري التحميل...'",
    "• تتلاشى الشاشة تدريجياً (Fade Out) قبل ظهور المحتوى الرئيسي",
], y, bg=LIGHT_BG, border=BLUE)
y -= 0.4*cm

y = section_bar(c, "الصفحة الرئيسية ومكوناتها", y, color=NAVY)
sections = [
    ("Hero Section", "قسم الترحيب الرئيسي مع عنوان المنصة وزر للانتقال لمكتبة الأكواد", BLUE),
    ("SnippetsGrid", "شبكة الأكواد المنشورة مع أزرار تصفية وبطاقات لكل كود", GREEN),
    ("Footer", "تذييل الصفحة مع معلومات المنصة والروابط", GRAY),
]
for sec, desc, color in sections:
    rect(c, MARGIN, y - 0.75*cm, INNER_W, 0.85*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(color)
    c.rect(W - MARGIN - 0.3*cm, y - 0.75*cm, 0.3*cm, 0.85*cm, fill=1, stroke=0)
    txt(c, sec, W - MARGIN - 0.6*cm, y - 0.3*cm, font="AmiriBold", size=10.5, color=color)
    txt(c, desc, W/2, y - 0.3*cm, size=10, color=GRAY)
    y -= 0.95*cm
y -= 0.3*cm

y = section_bar(c, "بطاقة الكود — تفاصيل العناصر", y, color=BLUE)
card_elements = [
    ("Header شريط العنوان", "خلفية زرقاء مع ثلاث نقاط (أحمر/أصفر/أخضر) وشارة نوع اللغة", NAVY),
    ("منطقة الكود", "كود مُنسَّق بخط JetBrains Mono مع تمرير أفقي (max-height 176px)", BLUE),
    ("للنوع FULL", "يعرض أول سطر من كل قسم (HTML/CSS/JS) مع تمييز لوني", GREEN),
    ("عنوان ووصف", "العنوان بخط ثقيل والوصف بخط رفيع مقطوع عند سطرين", GRAY),
    ("إحصائيات", "أيقونة نسخ + عدد النسخ / أيقونة قلب + عدد التفاعلات", CYAN),
    ("زر العمل", "نسخ الكود / تحميل الملف / تحميل كاملاً للنوع FULL", RED),
]
for elem, desc, color in card_elements:
    rect(c, MARGIN, y - 0.62*cm, INNER_W, 0.7*cm, fill=CARD_BG, stroke=BORDER, radius=3)
    c.setFillColor(color)
    c.circle(W - MARGIN - 0.3*cm, y - 0.25*cm, 4, fill=1)
    txt(c, elem, W - MARGIN - 0.6*cm, y - 0.35*cm, font="AmiriBold", size=10, color=color)
    txt(c, desc, W/2, y - 0.35*cm, size=9.5, color=GRAY)
    y -= 0.78*cm
y -= 0.4*cm

y = section_bar(c, "سكيلتون التحميل (Skeleton Loading)", y, color=PURPLE)
y = info_box(c, [
    "أثناء جلب الأكواد من Supabase تظهر 6 بطاقات هيكلية متحركة (Pulse Animation).",
    "كل بطاقة تُحاكي شكل البطاقة الحقيقية: شريط أعلى + منطقة كود + عنوان + وصف + زر.",
    "هذا يمنع الصفحة من الظهور فارغة ويُحسّن تجربة المستخدم أثناء الانتظار.",
    "عند اكتمال التحميل تُستبدَل البطاقات الهيكلية بالأكواد الحقيقية بتأثير Fade Up.",
], y, bg=PURPLE_BG, border=PURPLE)

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 11 — ADMIN PANEL BASICS
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "دليل لوحة الإدارة — الأساسيات")
footer(c, 11)
y = H - 1.8*cm

txt(c, "٩. دليل لوحة الإدارة — الأساسيات", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "الدخول إلى لوحة الإدارة", y, color=NAVY)
rect(c, MARGIN, y - 1.6*cm, INNER_W, 1.75*cm, fill=CARD_BG, stroke=BORDER, radius=6)
txt(c, "الرابط:", W - MARGIN - 0.35*cm, y - 0.45*cm,
    font="AmiriBold", size=11, color=NAVY)
c.setFont("Amiri", 11)
c.setFillColor(BLUE)
c.drawRightString(W - MARGIN - 1.8*cm, y - 0.45*cm, "yoursite.vercel.app/admin")
txt(c, "أدخل رمز الإدارة المحدد في خانة كلمة المرور ثم اضغط 'دخول' أو Enter.",
    W - MARGIN - 0.35*cm, y - 0.95*cm, size=10.5, color=GRAY)
txt(c, "الرمز يُحفظ في المتصفح حتى تُغلق التبويب — لا حاجة لإعادة الإدخال.",
    W - MARGIN - 0.35*cm, y - 1.35*cm, size=10.5, color=GRAY)
y -= 2.1*cm

y = section_bar(c, "خطوات نشر كود جديد", y, color=GREEN)
steps = [
    ("١", "أدخل العنوان",
     "العنوان إلزامي ويظهر في بطاقة الكود. يمكن إضافة تصنيف فرعي (category) اختياري."),
    ("٢", "اختر نوع اللغة",
     "HTML أو CSS أو JS أو كاملة (FULL). اختيار النوع يُغيّر واجهة المحرر."),
    ("٣", "اكتب أو الصق الكود",
     "المحرر يدعم أرقام الأسطر ومفتاح Tab للإدراج. للنوع FULL ستظهر 3 محررات."),
    ("٤", "أضف وصفاً (اختياري)",
     "الوصف يظهر أسفل العنوان ويُستخدم في البحث."),
    ("٥", "ارفع ملفاً مرفقاً (اختياري)",
     "اختر أي ملف من جهازك. سيُرفع إلى Supabase Storage وينتج رابط تحميل."),
    ("٦", "حدد حالة النشر واضغط 'نشر'",
     "مفعّل: يظهر للزوار فوراً. مُعطَّل: يُحفَظ كمسودة."),
]
box_cols = 2
box_w3 = (INNER_W - 0.4*cm) / box_cols
bx3 = W - MARGIN
for i, (num, title_s, body_s) in enumerate(steps):
    if i % box_cols == 0:
        if i > 0:
            y -= 2.25*cm
        bx3 = W - MARGIN
    rect(c, bx3 - box_w3, y - 2.1*cm, box_w3, 2.2*cm, fill=CARD_BG, stroke=BORDER, radius=6)
    c.setFillColor(BLUE)
    c.circle(bx3 - 0.55*cm, y - 0.55*cm, 12, fill=1)
    c.setFont("AmiriBold", 13)
    c.setFillColor(WHITE)
    c.drawCentredString(bx3 - 0.55*cm, y - 0.62*cm, num)
    txt(c, title_s, bx3 - 1.3*cm, y - 0.48*cm, font="AmiriBold", size=10.5, color=NAVY)
    txt(c, body_s, bx3 - 0.35*cm, y - 1.1*cm, size=9, color=GRAY)
    txt(c, body_s.split(".")[0] if "." in body_s else body_s,
        bx3 - 0.35*cm, y - 1.5*cm, size=9, color=GRAY)
    bx3 -= box_w3 + 0.4*cm
y -= 2.5*cm

y = section_bar(c, "أنواع الأكواد المدعومة", y, color=BLUE)
lang_types = [
    ("HTML", "هيكل الصفحة", HexColor("#dc2626"), HexColor("#fef2f2"),
     "أكواد HTML لبناء هيكل صفحات الويب. تُعرض وتُنسخ كنص."),
    ("CSS", "التنسيق والتصميم", HexColor("#1d4ed8"), LIGHT_BG,
     "أكواد CSS لتنسيق العناصر. تُعرض وتُنسخ كنص."),
    ("JS", "التفاعلية", HexColor("#ca8a04"), YELLOW_BG,
     "أكواد JavaScript لإضافة التفاعل. تُعرض وتُنسخ كنص."),
    ("FULL", "مشروع متكامل", GREEN, GREEN_BG,
     "HTML + CSS + JS مجتمعة. تُحمَّل كملف HTML واحد جاهز للتشغيل."),
]
lw3 = (INNER_W - 0.6*cm) / 4
lx3 = W - MARGIN
for lang, subtitle, color, bg, desc in lang_types:
    rect(c, lx3 - lw3, y - 2.2*cm, lw3, 2.35*cm, fill=bg, stroke=color, radius=6)
    rect(c, lx3 - lw3, y - 0.75*cm, lw3, 0.85*cm, fill=color, stroke=color, radius=4)
    txt(c, lang, lx3 - 0.2*cm, y - 0.5*cm, font="AmiriBold", size=14, color=WHITE)
    txt(c, subtitle, lx3 - 0.2*cm, y - 1.1*cm, size=9, color=color)
    txt(c, desc, lx3 - 0.2*cm, y - 1.6*cm, size=8.5, color=GRAY)
    lx3 -= lw3 + 0.2*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 12 — ADMIN PANEL MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "دليل لوحة الإدارة — الإدارة والتحكم")
footer(c, 12)
y = H - 1.8*cm

txt(c, "١٠. دليل لوحة الإدارة — الإدارة والتحكم", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "إجراءات إدارة الأكواد", y, color=NAVY)
actions = [
    ("معاينة", "يفتح نافذة Dialog تعرض الكود بنفس الشكل الذي يراه الزوار — مفيد للتحقق قبل النشر", BLUE),
    ("تعديل", "يملأ نموذج الإدراج ببيانات الكود المختار للتعديل عليه وإعادة الحفظ", HexColor("#0891b2")),
    ("إخفاء / نشر", "يُبدّل حالة published للكود — يظهر للزوار أو يُخفى بنقرة واحدة", GREEN),
    ("تصفير", "يُعيد عدادات views و likes إلى 0 بعد نافذة تأكيد AlertDialog", PURPLE),
    ("حذف", "يحذف الكود نهائياً من قاعدة البيانات بعد تأكيد في نافذة تحذير حمراء", RED),
]
for act, desc, color in actions:
    rect(c, MARGIN, y - 0.95*cm, INNER_W, 1.05*cm, fill=CARD_BG, stroke=BORDER, radius=5)
    rect(c, W - MARGIN - 2.2*cm, y - 0.95*cm, 2.2*cm, 1.05*cm, fill=color, stroke=color, radius=5)
    txt(c, act, W - MARGIN - 0.2*cm, y - 0.42*cm,
        font="AmiriBold", size=11, color=WHITE)
    txt(c, desc, W - MARGIN - 2.5*cm, y - 0.42*cm, size=10, color=GRAY)
    y -= 1.2*cm
y -= 0.4*cm

y = section_bar(c, "البحث والتصفية والترقيم", y, color=BLUE)
search_items = [
    ("حقل البحث النصي",
     "يبحث في عناوين الأكواد + الأوصاف + التصنيفات في آن واحد لحظياً"),
    ("أزرار التصفية حسب النوع",
     "الكل / HTML / CSS / JS / كاملة — عند الضغط تُصفَّر نتائج البحث ويُعاد التحديد"),
    ("الترقيم (Pagination)",
     "تُعرض 8 أكواد في كل صفحة مع أزرار السابق/التالي ورقم الصفحة الحالية"),
    ("الفلترة المدمجة",
     "البحث النصي والتصفية حسب النوع يعملان معاً — يمكن البحث في HTML فقط مثلاً"),
]
for title_si, desc_si in search_items:
    rect(c, MARGIN, y - 0.82*cm, INNER_W, 0.92*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(BLUE)
    c.circle(W - MARGIN - 0.3*cm, y - 0.4*cm, 4, fill=1)
    txt(c, title_si, W - MARGIN - 0.65*cm, y - 0.48*cm,
        font="AmiriBold", size=10, color=NAVY)
    txt(c, desc_si, W/2, y - 0.48*cm, size=9.5, color=GRAY)
    y -= 1.0*cm
y -= 0.4*cm

y = section_bar(c, "لوحة الإحصائيات (Stats Dashboard)", y, color=GREEN)
stats_cards = [
    ("إجمالي الأكواد", "جميع الأكواد\n(منشورة + مسودات)", NAVY),
    ("الأكواد المنشورة", "المرئية للزوار\nحالياً", GREEN),
    ("إجمالي النسخ", "مجموع مرات\nالنسخ والتحميل", BLUE),
    ("إجمالي التفاعل", "مجموع الإعجابات\nعلى جميع الأكواد", RED),
]
sw = (INNER_W - 0.6*cm) / 4
sx = W - MARGIN
for title_c, desc_c, color_c in stats_cards:
    rect(c, sx - sw, y - 2.2*cm, sw, 2.35*cm, fill=CARD_BG, stroke=BORDER, radius=8)
    c.setFillColor(color_c)
    c.circle(sx - sw/2, y - 0.7*cm, 18, fill=1)
    c.setFont("AmiriBold", 9)
    c.setFillColor(WHITE)
    c.drawCentredString(sx - sw/2, y - 0.78*cm, "99")
    txt(c, title_c, sx - 0.2*cm, y - 1.35*cm, font="AmiriBold", size=9, color=color_c)
    for di, dline in enumerate(desc_c.split("\n")):
        txt(c, dline, sx - 0.2*cm, y - 1.75*cm + di * (-0.4*cm), size=8, color=GRAY)
    sx -= sw + 0.2*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 13 — FULL TYPE
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "نوع 'كاملة' — مشاريع HTML+CSS+JS")
footer(c, 13)
y = H - 1.8*cm

txt(c, "١١. نوع 'كاملة' — مشاريع HTML+CSS+JS", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "ما هو النوع 'كاملة'؟", y, color=GREEN)
y = info_box(c, [
    "النوع 'كاملة' مُصمَّم لنشر مشاريع ويب متكاملة تجمع الثلاثة لغات في مكان واحد.",
    "بدلاً من نشر أكواد HTML و CSS و JS بشكل منفصل، يمكن نشرها معاً ككتلة واحدة",
    "متكاملة. الزائر يحصل على ملف HTML واحد يعمل مباشرة عند فتحه في المتصفح.",
], y, bg=GREEN_BG, border=GREEN)
y -= 0.4*cm

# Three columns for the editors
y = section_bar(c, "واجهة المحرر عند اختيار 'كاملة'", y, color=GREEN)
editors = [
    ("HTML", "بنية الصفحة", HexColor("#dc2626"), HexColor("#fef2f2"),
     "<!DOCTYPE html>\n<html>\n<body>\n  <h1>مرحباً</h1>\n</body>\n</html>"),
    ("CSS", "تنسيق العناصر", HexColor("#1d4ed8"), LIGHT_BG,
     "body {\n  font-family: Cairo;\n  direction: rtl;\n  color: #1a2e52;\n}"),
    ("JS", "التفاعلية", HexColor("#ca8a04"), YELLOW_BG,
     "document.querySelector('h1')\n  .addEventListener('click',\n  () => alert('مرحباً!'));"),
]
ew = (INNER_W - 0.8*cm) / 3
ex = W - MARGIN
for lang, subtitle, color, bg, code_ex in editors:
    rect(c, ex - ew, y - 3.8*cm, ew, 4.0*cm, fill=bg, stroke=color, radius=6)
    rect(c, ex - ew, y - 0.7*cm, ew, 0.78*cm, fill=color, stroke=color, radius=4)
    txt(c, lang, ex - 0.2*cm, y - 0.45*cm, font="AmiriBold", size=12, color=WHITE)
    txt(c, subtitle, ex - 0.2*cm, y - 1.15*cm, size=9, color=color)
    # Code preview
    c.setFont("Amiri", 7.5)
    c.setFillColor(HexColor("#334155"))
    for li, line in enumerate(code_ex.split("\n")):
        c.drawRightString(ex - 0.25*cm, y - 1.6*cm - li * 0.38*cm, line)
    ex -= ew + 0.4*cm
y -= 4.5*cm

y = section_bar(c, "كيف يُخزَّن ويُولَّد الملف", y, color=NAVY)
flow_full = [
    ("عند النشر من لوحة الإدارة", NAVY,
     "يُحوَّل HTML + CSS + JS إلى JSON: {\"html\":\"...\",\"css\":\"...\",\"js\":\"...\"} ويُخزَّن في عمود code"),
    ("عند عرض الكود للزائر", BLUE,
     "تُقرأ قيمة code وتُحلَّل بـ JSON.parse() ويُعرض أول سطر من كل قسم كمعاينة"),
    ("عند الضغط على 'تحميل كاملاً'", GREEN,
     "يُولَّد ملف HTML كامل مدمج (HTML في body + CSS في style + JS في script) ويُحمَّل مباشرة"),
]
for title_f, color_f, desc_f in flow_full:
    rect(c, MARGIN, y - 1.1*cm, INNER_W, 1.2*cm, fill=CARD_BG, stroke=BORDER, radius=5)
    c.setFillColor(color_f)
    c.circle(W - MARGIN - 0.4*cm, y - 0.52*cm, 8, fill=1)
    txt(c, title_f, W - MARGIN - 0.85*cm, y - 0.38*cm,
        font="AmiriBold", size=10.5, color=color_f)
    txt(c, desc_f, W - MARGIN - 0.85*cm, y - 0.78*cm, size=9.5, color=GRAY)
    y -= 1.35*cm
y -= 0.3*cm

y = section_bar(c, "بنية ملف HTML الناتج", y, color=BLUE)
rect(c, MARGIN, y - 3.8*cm, INNER_W, 4.0*cm, fill=HexColor("#0f172a"), stroke=NAVY, radius=6)
html_code = [
    ("<!DOCTYPE html>", HexColor("#94a3b8")),
    ("<html lang=\"ar\">", HexColor("#60a5fa")),
    ("<head>", HexColor("#60a5fa")),
    ("  <meta charset=\"UTF-8\">", HexColor("#6ee7b7")),
    ("  <title>عنوان المشروع</title>", HexColor("#fcd34d")),
    ("  <style>  /* CSS الخاص بك */  </style>", HexColor("#f9a8d4")),
    ("</head><body>", HexColor("#60a5fa")),
    ("  <!-- HTML الخاص بك -->", HexColor("#64748b")),
    ("  <script>  /* JS الخاص بك */  </script>", HexColor("#fcd34d")),
    ("</body></html>", HexColor("#60a5fa")),
]
ly = y - 0.45*cm
for line, color in html_code:
    c.setFont("Amiri", 9)
    c.setFillColor(color)
    c.drawRightString(W - MARGIN - 0.4*cm, ly, line)
    ly -= 0.35*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 14 — DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "الاستضافة والنشر التلقائي")
footer(c, 14)
y = H - 1.8*cm

txt(c, "١٢. الاستضافة والنشر التلقائي (CI/CD)", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "إعداد الاستضافة على Vercel", y, color=NAVY)
y = info_box(c, [
    "**Vercel** هي منصة استضافة مخصصة لتطبيقات React / Next.js / Vite الحديثة.",
    None,
    "الإعداد يتم مرة واحدة فقط:",
    "١. ربط حساب GitHub بحساب Vercel",
    "٢. اختيار المستودع (Repository) من القائمة",
    "٣. إضافة متغيرات البيئة: VITE_SUPABASE_URL و VITE_SUPABASE_PUBLISHABLE_KEY",
    "٤. الضغط على Deploy — ينتهي كل شيء!",
], y, bg=LIGHT_BG, border=BLUE)
y -= 0.4*cm

y = section_bar(c, "دورة النشر التلقائي", y, color=GREEN)
deploy_steps = [
    ("تعديل الكود", "المطور يُعدّل ملفاً ويُرفعه إلى GitHub", BLUE),
    ("GitHub يُشعر Vercel", "Vercel يستقبل إشعار push تلقائياً", HexColor("#0891b2")),
    ("npm run build", "Vercel يُشغّل أمر البناء ويولّد الملفات الثابتة", PURPLE),
    ("نشر فوري", "الملفات تُوزَّع على CDN عالمي خلال دقيقة", GREEN),
    ("رابط فريد", "كل نشر يحصل على رابط معاينة، و main يُحدّث الموقع الرئيسي", NAVY),
]
for i, (title_d, desc_d, color_d) in enumerate(deploy_steps):
    rect(c, MARGIN, y - 0.85*cm, INNER_W, 0.95*cm, fill=CARD_BG, stroke=BORDER, radius=5)
    c.setFillColor(color_d)
    c.circle(W - MARGIN - 0.4*cm, y - 0.4*cm, 10, fill=1)
    c.setFont("AmiriBold", 10)
    c.setFillColor(WHITE)
    c.drawCentredString(W - MARGIN - 0.4*cm, y - 0.47*cm, str(i + 1))
    txt(c, title_d, W - MARGIN - 1.1*cm, y - 0.28*cm, font="AmiriBold", size=10.5, color=color_d)
    txt(c, desc_d, W/2, y - 0.28*cm, size=10, color=GRAY)
    y -= 1.1*cm
y -= 0.4*cm

y = section_bar(c, "إصلاح مشكلة 404 على Vercel", y, color=YELLOW)
y = info_box(c, [
    "**المشكلة:** عند الدخول المباشر لرابط /admin يُعيد Vercel خطأ 404.",
    "**السبب:** التطبيق SPA (Single Page App) — التوجيه يتم في المتصفح وليس السيرفر.",
    None,
    "**الحل:** ملف vercel.json في جذر المشروع يُوجّه كل الطلبات إلى index.html:",
    "    { \"rewrites\": [{ \"source\": \"/(.*)\", \"destination\": \"/index.html\" }] }",
    None,
    "React Router يستلم من هناك ويعرض الصفحة الصحيحة بناءً على الرابط.",
], y, bg=YELLOW_BG, border=YELLOW)
y -= 0.4*cm

y = section_bar(c, "متغيرات البيئة المطلوبة", y, color=BLUE)
env_vars = [
    ("VITE_SUPABASE_URL", "رابط مشروع Supabase — يجد في Settings > API في لوحة Supabase",
     "https://xxxxxxxx.supabase.co"),
    ("VITE_SUPABASE_PUBLISHABLE_KEY", "المفتاح العام (anon/public key) — آمن للاستخدام في المتصفح",
     "eyJhbGciOiJIUzI1NiIs..."),
]
for name, desc, example in env_vars:
    rect(c, MARGIN, y - 1.2*cm, INNER_W, 1.32*cm, fill=CARD_BG, stroke=BORDER, radius=5)
    c.setFont("Amiri", 9.5)
    c.setFillColor(PURPLE)
    c.drawRightString(W - MARGIN - 0.35*cm, y - 0.32*cm, name)
    txt(c, desc, W - MARGIN - 0.35*cm, y - 0.65*cm, size=9.5, color=GRAY)
    c.setFont("Amiri", 8.5)
    c.setFillColor(HexColor("#64748b"))
    c.drawRightString(W - MARGIN - 0.35*cm, y - 0.98*cm, f"مثال: {example}")
    y -= 1.45*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 15 — FAQ
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "الأسئلة الشائعة")
footer(c, 15)
y = H - 1.8*cm

txt(c, "١٣. الأسئلة الشائعة (FAQ)", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

faqs = [
    ("كيف يعمل نظام المصادقة في الإدارة؟",
     "لا يوجد JWT أو جلسة مستخدم. يُرسَل رمز ثابت مع كل طلب إلى Edge Function."
     " الدالة تتحقق من الرمز وترفض الطلب بـ 401 إذا كان خاطئاً. الرمز يُخزَّن"
     " في localStorage ويبقى حتى إغلاق التبويب.",
     NAVY),
    ("هل يمكن للزائر العادي تعديل أو حذف الأكواد؟",
     "لا تماماً. سياسة RLS في Supabase تمنع الـ anon key من أي كتابة مباشرة."
     " والعمليات الإدارية تمر حصراً عبر Edge Function التي تتحقق من رمز الإدارة.",
     RED),
    ("كيف تُحسَب مرات النسخ والتفاعل؟",
     "عند نسخ أو تحميل أي كود تُستدعى دالة SQL (increment_snippet_views) تزيد"
     " العداد بمقدار 1. الإعجابات تُخزَّن في localStorage فلا يمكن التفاعل"
     " أكثر من مرة من نفس الجهاز.",
     BLUE),
    ("كيف يُخزَّن الكود الكامل (FULL)؟",
     "يُخزَّن كـ JSON في حقل code: {\"html\":\"...\",\"css\":\"...\",\"js\":\"...\"}."
     " عند التحميل يُفكَّك الـ JSON ويُولَّد ملف HTML مدمج (HTML + style + script)"
     " يُحمَّل مباشرة دون الحاجة لأي سيرفر.",
     GREEN),
    ("كيف يُنشر الموقع تلقائياً؟",
     "Vercel يراقب فرع main في GitHub. عند كل دمج يُشغَّل بناء npm run build تلقائياً"
     " وتُوزَّع الملفات الثابتة الناتجة على CDN عالمي. العملية تستغرق حوالي دقيقة.",
     PURPLE),
    ("لماذا لا يحتاج الزائر لإنشاء حساب؟",
     "سياسة RLS تسمح لأي طلب من anon role بقراءة الأكواد published = true دون"
     " أي مصادقة. هذا تصميم مقصود لتبسيط تجربة المستخدم.",
     CYAN),
    ("ماذا يحدث إذا انتهت حصة Supabase المجانية؟",
     "تُوقَف الطلبات الجديدة تدريجياً. الحل: ترقية الخطة إلى Pro ($25/شهر)"
     " أو تقليل استهلاك البيانات. حصة 500K Edge Function call شهرياً تكفي"
     " لآلاف الزيارات اليومية.",
     YELLOW),
    ("هل يمكن إضافة نوع لغة جديد مستقبلاً؟",
     "نعم بسهولة. عمود language من نوع TEXT وليس ENUM، فأضافة نوع جديد مثل"
     " 'Python' يتطلب فقط إضافته في قائمة الفلاتر والمحرر في الكود. لا تعديل"
     " في قاعدة البيانات.",
     GREEN),
    ("كيف تعمل ميزة رفع الملفات؟",
     "الملف يُقرأ في المتصفح كـ base64 ثم يُرسَل إلى Edge Function ضمن جسم الطلب."
     " الدالة تُفكّك base64 وترفع الملف إلى bucket snippet-files في Supabase Storage"
     " وتُعيد رابطاً عاماً دائماً.",
     BLUE),
    ("هل الموقع يعمل على الجوال؟",
     "نعم. التصميم متجاوب (Responsive) ويستخدم Tailwind CSS للتكيف مع جميع أحجام"
     " الشاشات. الشبكة تتحول من 3 أعمدة على الكمبيوتر إلى عمود واحد على الجوال.",
     NAVY),
]

for q, a, color in faqs:
    q_h = 0.55*cm
    a_lines = [a[i:i+85] for i in range(0, len(a), 85)]
    total_h = q_h + len(a_lines) * 0.48*cm + 0.4*cm
    if y - total_h < 2.5*cm:
        break
    rect(c, MARGIN, y - total_h, INNER_W, total_h, fill=CARD_BG, stroke=BORDER, radius=5)
    c.setFillColor(color)
    c.rect(W - MARGIN - 0.28*cm, y - total_h, 0.28*cm, total_h, fill=1, stroke=0)
    txt(c, q, W - MARGIN - 0.55*cm, y - 0.4*cm, font="AmiriBold", size=10.5, color=color)
    ly = y - 0.4*cm - q_h
    txt(c, a, W - MARGIN - 0.55*cm, ly, size=9.5, color=GRAY)
    y -= total_h + 0.35*cm

c.showPage()


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 16 — CONCLUSION & FUTURE
# ═══════════════════════════════════════════════════════════════════════════
page_header(c, "الخاتمة والتطوير المستقبلي")
footer(c, 16)
y = H - 1.8*cm

txt(c, "١٤. الخاتمة والتطوير المستقبلي", W - MARGIN, y,
    font="AmiriBold", size=18, color=NAVY)
y -= 0.45*cm
hline(c, y)
y -= 0.9*cm

y = section_bar(c, "ملخص ما تحقق في المشروع", y, color=GREEN)
achievements = [
    "منصة ويب عربية كاملة تعمل فعلياً على الإنترنت",
    "نظام نشر وإدارة أكواد متكامل بواجهتين: عامة وإدارية",
    "قاعدة بيانات محمية بسياسات RLS مع Edge Functions لإدارة آمنة",
    "دعم 4 أنواع أكواد: HTML / CSS / JS / كاملة مع ميزة التحميل الفوري",
    "تصميم عربي RTL احترافي مع تجربة مستخدم سلسة",
    "نشر تلقائي مستمر عبر Vercel + GitHub",
    "شاشة بداية وتأثيرات تحميل هيكلية لتجربة مستخدم محسّنة",
    "نظام بحث وتصفية وترقيم متكامل في لوحة الإدارة",
]
for ach in achievements:
    y = check_line(c, ach, y, color=GREEN, size=11)
y -= 0.5*cm

y = section_bar(c, "التحديات التقنية وحلولها", y, color=BLUE)
challenges = [
    ("توليف Arabic PDF بالعربية",
     "استخدام arabic_reshaper + python-bidi + خط Amiri لتوليد PDF عربي صحيح الاتجاه"),
    ("توجيه SPA على Vercel (404)",
     "ملف vercel.json مع rewrites يوجّه كل الطلبات لـ index.html ليتولى React Router التوجيه"),
    ("أمان الإدارة بدون Backend",
     "Edge Function بصلاحية service role تعزل المنطق الإداري عن المتصفح تماماً"),
    ("أكواد كاملة في حقل نصي واحد",
     "تخزين JSON في TEXT column يتيح دعم النوع FULL بدون أي تغيير في مخطط قاعدة البيانات"),
]
for chall, sol in challenges:
    rect(c, MARGIN, y - 0.9*cm, INNER_W, 1.0*cm, fill=CARD_BG, stroke=BORDER, radius=4)
    c.setFillColor(RED)
    c.circle(W - MARGIN - 0.35*cm, y - 0.43*cm, 5, fill=1)
    txt(c, chall, W - MARGIN - 0.7*cm, y - 0.3*cm, font="AmiriBold", size=10, color=NAVY)
    c.setFillColor(GREEN)
    c.circle(W - MARGIN - 0.35*cm, y - 0.72*cm, 4, fill=1)
    txt(c, sol, W - MARGIN - 0.7*cm, y - 0.63*cm, size=9.5, color=GRAY)
    y -= 1.12*cm
y -= 0.4*cm

y = section_bar(c, "اقتراحات للتطوير المستقبلي", y, color=PURPLE)
future = [
    ("نظام المستخدمين والملفات الشخصية", "تسجيل دخول للمطورين لنشر أكوادهم الخاصة مع ملف شخصي", BLUE),
    ("نظام التعليقات", "إضافة قسم تعليقات تحت كل كود للنقاش وطرح الأسئلة", GREEN),
    ("محرر كود مُحسَّن مع تمييز الصياغة", "استخدام CodeMirror أو Monaco Editor لتجربة كتابة احترافية", PURPLE),
    ("البحث الذكي", "بحث نصي كامل (Full-Text Search) في محتوى الأكواد وليس فقط العناوين", CYAN),
    ("إشعارات البريد الإلكتروني", "إشعار المدير عند وصول أكواد جديدة أو تفاعلات مميزة", YELLOW),
    ("تطبيق جوال", "تطبيق React Native يتيح تصفح الأكواد ونسخها من الجوال", NAVY),
]
fw = (INNER_W - 0.8*cm) / 3
fx = W - MARGIN
for i, (title_f2, desc_f2, color_f2) in enumerate(future):
    if i > 0 and i % 3 == 0:
        y -= 2.1*cm
        fx = W - MARGIN
    rect(c, fx - fw, y - 1.9*cm, fw, 2.05*cm, fill=CARD_BG, stroke=BORDER, radius=6)
    c.setFillColor(color_f2)
    c.circle(fx - fw/2, y - 0.55*cm, 12, fill=1)
    txt(c, title_f2, fx - 0.2*cm, y - 1.1*cm, font="AmiriBold", size=9, color=color_f2)
    txt(c, desc_f2, fx - 0.2*cm, y - 1.5*cm, size=8, color=GRAY)
    fx -= fw + 0.4*cm

c.showPage()

c.save()
print(f"PDF saved: {OUT}")
