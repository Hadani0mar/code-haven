@echo off
chcp 65001 > nul
echo ============================================
echo   بناء مختبر اتصال SQL Server
echo   SQL Connection Tester - Build Script
echo ============================================
echo.

set PROJECT=SqlConnectionTester\SqlConnectionTester.csproj
set OUTPUT=publish\win-x64

echo [1/3] تنظيف ملفات البناء السابقة...
if exist publish rmdir /s /q publish
echo       تم.
echo.

echo [2/3] بناء ونشر التطبيق...
dotnet publish "%PROJECT%" ^
    -c Release ^
    -r win-x64 ^
    --self-contained true ^
    -p:PublishSingleFile=true ^
    -p:IncludeNativeLibrariesForSelfExtract=true ^
    -p:EnableCompressionInSingleFile=true ^
    -o "%OUTPUT%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [خطأ] فشل عملية البناء!
    echo تأكد من تثبيت .NET 8 SDK
    pause
    exit /b 1
)

echo.
echo [3/3] اكتمل البناء بنجاح!
echo.
echo ============================================
echo   ملف الـ EXE جاهز في:
echo   %OUTPUT%\SqlConnectionTester.exe
echo ============================================
echo.
explorer "%OUTPUT%"
pause
