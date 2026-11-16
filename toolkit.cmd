@echo off
"%~dp0runtime\python\python.exe" "%~dp0toolkit.py" %*
exit /b %errorlevel%
