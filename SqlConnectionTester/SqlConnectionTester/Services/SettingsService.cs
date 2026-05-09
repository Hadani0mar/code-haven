using System.IO;
using System.Text.Json;
using SqlConnectionTester.Models;

namespace SqlConnectionTester.Services;

public static class SettingsService
{
    private static readonly string SettingsPath = Path.Combine(
        AppDomain.CurrentDomain.BaseDirectory, "settings.json");

    public static void Save(ConnectionSettings settings)
    {
        var options = new JsonSerializerOptions { WriteIndented = true };
        var json = JsonSerializer.Serialize(settings, options);
        File.WriteAllText(SettingsPath, json);
    }

    public static ConnectionSettings? Load()
    {
        if (!File.Exists(SettingsPath))
            return null;

        try
        {
            var json = File.ReadAllText(SettingsPath);
            return JsonSerializer.Deserialize<ConnectionSettings>(json);
        }
        catch
        {
            return null;
        }
    }
}
