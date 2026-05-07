INSERT INTO public.snippets (title, description, language, category, code, author_name, published)
VALUES
  (
    'بطاقة مستخدم متجاوبة',
    'واجهة بطاقة مستخدم أنيقة باستخدام CSS Grid.',
    'HTML',
    'واجهة',
    '<div class="profile-card">\n  <img src="https://i.pravatar.cc/120" alt="avatar"/>\n  <h3>مطور عربي</h3>\n  <p>Frontend Developer</p>\n</div>',
    'منصتي',
    true
  ),
  (
    'تبديل الوضع الليلي',
    'كود JavaScript بسيط لتبديل الثيم مع localStorage.',
    'JS',
    'تفاعل',
    'const modeBtn = document.querySelector("#modeBtn");\nmodeBtn?.addEventListener("click", () => {\n  document.body.classList.toggle("dark");\n  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");\n});',
    'منصتي',
    true
  ),
  (
    'ستايل جدول إدارة',
    'تنسيق جاهز لجدول لوحة الإدارة.',
    'CSS',
    'لوحة تحكم',
    '.admin-table {\n  width: 100%;\n  border-collapse: collapse;\n}\n.admin-table th, .admin-table td {\n  border-bottom: 1px solid #e5e7eb;\n  padding: 10px;\n}',
    'منصتي',
    true
  );
