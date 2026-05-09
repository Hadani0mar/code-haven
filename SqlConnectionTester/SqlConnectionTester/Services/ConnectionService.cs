using System.Diagnostics;
using Microsoft.Data.SqlClient;
using SqlConnectionTester.Models;

namespace SqlConnectionTester.Services;

public record ConnectionResult(bool Success, string Message, string? ServerVersion = null, long ResponseMs = 0);

public static class ConnectionService
{
    public static async Task<ConnectionResult> TestAsync(ConnectionSettings settings, string password)
    {
        var connectionString = BuildConnectionString(settings, password);
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await using var connection = new SqlConnection(connectionString);
            await connection.OpenAsync();
            stopwatch.Stop();

            var version = connection.ServerVersion ?? "غير معروف";
            return new ConnectionResult(true, "تم الاتصال بنجاح", version, stopwatch.ElapsedMilliseconds);
        }
        catch (SqlException ex)
        {
            stopwatch.Stop();
            return new ConnectionResult(false, TranslateSqlError(ex));
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            return new ConnectionResult(false, $"خطأ غير متوقع: {ex.Message}");
        }
    }

    private static string BuildConnectionString(ConnectionSettings settings, string password)
    {
        var builder = new SqlConnectionStringBuilder
        {
            DataSource = settings.UseCustomPort && settings.Port != 1433
                ? $"{settings.ServerName},{settings.Port}"
                : settings.ServerName,
            InitialCatalog = settings.DatabaseName,
            ConnectTimeout = 10,
            TrustServerCertificate = true
        };

        if (settings.UseWindowsAuth)
        {
            builder.IntegratedSecurity = true;
        }
        else
        {
            builder.IntegratedSecurity = false;
            builder.UserID = settings.Username;
            builder.Password = password;
        }

        return builder.ConnectionString;
    }

    private static string TranslateSqlError(SqlException ex)
    {
        return ex.Number switch
        {
            -2 => "انتهت مهلة الاتصال. تأكد من أن السيرفر يعمل وأن الشبكة متاحة.",
            2 or 53 => "تعذر الوصول للسيرفر. تأكد من صحة IP/اسم السيرفر وأن الشبكة تعمل.",
            10060 => "انتهت مهلة الاتصال بالشبكة. تأكد من إعدادات الجدار الناري والشبكة.",
            10061 => "رُفض الاتصال. تأكد من أن خدمة SQL Server تعمل وأن المنفذ صحيح.",
            18456 => "اسم المستخدم أو كلمة المرور خاطئة. تأكد من بيانات الدخول.",
            18452 => "المستخدم غير مصرح له بالدخول. تحقق من صلاحيات الحساب.",
            4060 => "اسم قاعدة البيانات غير موجود أو لا توجد صلاحية للوصول إليها.",
            4064 => "لا يمكن فتح قاعدة البيانات المطلوبة. تحقق من الاسم والصلاحيات.",
            233 => "خدمة SQL Server متوقفة أو لا تقبل الاتصالات حالياً.",
            40 => "تعذر فتح الاتصال بـ SQL Server. تأكد من تشغيل الخدمة.",
            20 => "خطأ في الاتصال الآمن (SSL/TLS). جرب تفعيل 'Trust Server Certificate'.",
            _ => $"خطأ SQL رقم {ex.Number}: {ex.Message}"
        };
    }
}
