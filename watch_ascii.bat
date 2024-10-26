@echo off
setlocal enabledelayedexpansion

where curl >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo curl is not installed. Please install it first.
    exit /b 1
)

set "URL=%~1"
if "%URL%"=="" set "URL=http://localhost:5000"

cls

echo [?25l

:handle_cleanup
echo [?25h

curl -N "%URL%"

echo [?25h
exit /b 0