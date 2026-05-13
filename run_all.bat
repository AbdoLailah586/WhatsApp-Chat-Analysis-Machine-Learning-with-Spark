@echo off
echo ==========================================
echo WhatsApp Big Data Project Runner
echo ==========================================

echo [1/2] Checking Spark Environment...
python check_spark.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Spark environment check failed. Please check your installation.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Running WhatsApp Analysis ^& ML Training...
python spark_processor.py

echo.
echo ==========================================
echo Project execution complete!
echo ==========================================
pause
