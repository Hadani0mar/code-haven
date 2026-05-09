using System.Windows;
using System.Windows.Media;
using SqlConnectionTester.Models;
using SqlConnectionTester.Services;

namespace SqlConnectionTester;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        LoadSettings();
    }

    private void LoadSettings()
    {
        var settings = SettingsService.Load();
        if (settings is null) return;

        TxtServer.Text = settings.ServerName;
        TxtDatabase.Text = settings.DatabaseName;
        TxtPort.Text = settings.Port.ToString();
        ChkCustomPort.IsChecked = settings.UseCustomPort;

        if (settings.UseWindowsAuth)
        {
            RbWindowsAuth.IsChecked = true;
        }
        else
        {
            RbSqlAuth.IsChecked = true;
            TxtUsername.Text = settings.Username;
        }
    }

    private void AuthType_Changed(object sender, RoutedEventArgs e)
    {
        if (SqlAuthPanel is null || WindowsAuthNotice is null) return;

        bool isSql = RbSqlAuth.IsChecked == true;
        SqlAuthPanel.Visibility = isSql ? Visibility.Visible : Visibility.Collapsed;
        WindowsAuthNotice.Visibility = isSql ? Visibility.Collapsed : Visibility.Visible;
    }

    private void ChkCustomPort_Changed(object sender, RoutedEventArgs e)
    {
        if (TxtPort is null) return;

        bool custom = ChkCustomPort.IsChecked == true;
        TxtPort.IsEnabled = custom;
        TxtPort.Foreground = custom
            ? new SolidColorBrush(Color.FromRgb(26, 43, 60))
            : new SolidColorBrush(Color.FromRgb(158, 158, 158));
    }

    private async void BtnTest_Click(object sender, RoutedEventArgs e)
    {
        if (!ValidateInputs()) return;

        SetLoadingState(true);

        var settings = GetCurrentSettings();
        var password = RbSqlAuth.IsChecked == true ? PbPassword.Password : string.Empty;

        var result = await ConnectionService.TestAsync(settings, password);

        SetLoadingState(false);
        ShowResult(result);
    }

    private void BtnSave_Click(object sender, RoutedEventArgs e)
    {
        if (!ValidateInputs()) return;

        var settings = GetCurrentSettings();
        SettingsService.Save(settings);

        MessageBox.Show("تم حفظ الإعدادات بنجاح!\n(كلمة المرور لم تُحفظ لأسباب أمنية)",
                        "حفظ الإعدادات", MessageBoxButton.OK, MessageBoxImage.Information);
    }

    private bool ValidateInputs()
    {
        if (string.IsNullOrWhiteSpace(TxtServer.Text))
        {
            MessageBox.Show("يرجى إدخال اسم السيرفر أو IP.", "تحقق من المدخلات",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
            TxtServer.Focus();
            return false;
        }

        if (string.IsNullOrWhiteSpace(TxtDatabase.Text))
        {
            MessageBox.Show("يرجى إدخال اسم قاعدة البيانات.", "تحقق من المدخلات",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
            TxtDatabase.Focus();
            return false;
        }

        if (ChkCustomPort.IsChecked == true)
        {
            if (!int.TryParse(TxtPort.Text, out int port) || port < 1 || port > 65535)
            {
                MessageBox.Show("رقم المنفذ غير صحيح. يجب أن يكون بين 1 و 65535.", "تحقق من المدخلات",
                                MessageBoxButton.OK, MessageBoxImage.Warning);
                TxtPort.Focus();
                return false;
            }
        }

        if (RbSqlAuth.IsChecked == true && string.IsNullOrWhiteSpace(TxtUsername.Text))
        {
            MessageBox.Show("يرجى إدخال اسم المستخدم.", "تحقق من المدخلات",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
            TxtUsername.Focus();
            return false;
        }

        return true;
    }

    private ConnectionSettings GetCurrentSettings()
    {
        int.TryParse(TxtPort.Text, out int port);
        return new ConnectionSettings
        {
            ServerName = TxtServer.Text.Trim(),
            DatabaseName = TxtDatabase.Text.Trim(),
            UseWindowsAuth = RbWindowsAuth.IsChecked == true,
            Username = TxtUsername.Text.Trim(),
            Port = port > 0 ? port : 1433,
            UseCustomPort = ChkCustomPort.IsChecked == true
        };
    }

    private void SetLoadingState(bool loading)
    {
        BtnTest.IsEnabled = !loading;
        BtnSave.IsEnabled = !loading;
        LoadingPanel.Visibility = loading ? Visibility.Visible : Visibility.Collapsed;
        if (loading)
            ResultPanel.Visibility = Visibility.Collapsed;
    }

    private void ShowResult(Services.ConnectionResult result)
    {
        ResultPanel.Visibility = Visibility.Visible;

        if (result.Success)
        {
            ResultPanel.Background = new SolidColorBrush(Color.FromRgb(232, 245, 233));
            ResultPanel.BorderBrush = new SolidColorBrush(Color.FromRgb(76, 175, 80));
            ResultPanel.BorderThickness = new Thickness(2);

            TxtResultIcon.Text = "✅";
            TxtResultTitle.Text = "تم الاتصال بنجاح!";
            TxtResultTitle.Foreground = new SolidColorBrush(Color.FromRgb(27, 94, 32));

            TxtResultDetail.Text =
                $"🖥️  إصدار SQL Server:  {result.ServerVersion}\n" +
                $"⚡  وقت الاستجابة:       {result.ResponseMs} ميلي ثانية\n" +
                $"🗄️  قاعدة البيانات:      {TxtDatabase.Text.Trim()}\n" +
                $"🌐  السيرفر:              {TxtServer.Text.Trim()}";
        }
        else
        {
            ResultPanel.Background = new SolidColorBrush(Color.FromRgb(255, 235, 238));
            ResultPanel.BorderBrush = new SolidColorBrush(Color.FromRgb(244, 67, 54));
            ResultPanel.BorderThickness = new Thickness(2);

            TxtResultIcon.Text = "❌";
            TxtResultTitle.Text = "فشل الاتصال";
            TxtResultTitle.Foreground = new SolidColorBrush(Color.FromRgb(183, 28, 28));

            TxtResultDetail.Text = $"📋  تفاصيل الخطأ:\n\n{result.Message}";
        }
    }
}
