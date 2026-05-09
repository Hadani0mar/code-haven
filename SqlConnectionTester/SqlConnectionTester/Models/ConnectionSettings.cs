namespace SqlConnectionTester.Models;

public class ConnectionSettings
{
    public string ServerName { get; set; } = string.Empty;
    public string DatabaseName { get; set; } = string.Empty;
    public bool UseWindowsAuth { get; set; } = true;
    public string Username { get; set; } = string.Empty;
    public int Port { get; set; } = 1433;
    public bool UseCustomPort { get; set; } = false;
}
