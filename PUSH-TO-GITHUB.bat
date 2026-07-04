@echo off
REM Ticket Agent - Push to GitHub Script
REM This script pushes your project to GitHub automatically

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║     🎫 TICKET AGENT - PUSH TO GITHUB 🎫              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✓ Git found
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Please run this script from the project root directory
    echo.
    pause
    exit /b 1
)

echo ✓ Project directory confirmed
echo.

REM Initialize git if not already done
if not exist ".git" (
    echo 📝 Initializing git repository...
    git init
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to initialize git
        pause
        exit /b 1
    )
    echo ✓ Git repository initialized
    echo.
)

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo 📝 Creating .gitignore...
    (
        echo # Environment variables
        echo .env
        echo .env.local
        echo .env.*.local
        echo.
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo venv/
        echo ENV/
        echo dist/
        echo build/
        echo *.egg-info/
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # Database
        echo *.sqlite3
        echo chroma_data/
    ) > .gitignore
    echo ✓ .gitignore created
    echo.
)

REM Check git config
echo 📋 Checking git configuration...
git config --global user.name >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Git user not configured
    echo.
    echo Please configure git first:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "your@email.com"
    echo.
    pause
    exit /b 1
)
echo ✓ Git user configured
echo.

REM Get current remote
git remote get-url origin >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🔗 Setting up remote repository...
    set /p REPO_URL="Enter your GitHub repository URL (or press Enter for default): "
    
    if "!REPO_URL!"=="" (
        set REPO_URL=https://github.com/DHARSAN777/AI-Ticket-Routing-Agent.git
    )
    
    git remote add origin !REPO_URL!
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to add remote
        pause
        exit /b 1
    )
    echo ✓ Remote repository configured
    echo.
) else (
    echo ✓ Remote repository already configured
    echo.
)

REM Stage all files
echo 📦 Staging files...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to stage files
    pause
    exit /b 1
)
echo ✓ Files staged
echo.

REM Show status
echo 📊 Git status:
echo.
git status
echo.

REM Get commit message
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "!COMMIT_MSG!"=="" (
    set COMMIT_MSG=Initial commit: Ticket Agent AI-powered support system
)

REM Commit
echo.
echo 💾 Creating commit...
git commit -m "!COMMIT_MSG!"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Commit failed (files may already be committed)
    echo.
) else (
    echo ✓ Commit created
    echo.
)

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Push failed
    echo.
    echo Possible reasons:
    echo  1. Authentication failed - check your credentials
    echo  2. No internet connection
    echo  3. Remote not configured properly
    echo.
    echo Try manual push:
    echo   git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║     ✅ SUCCESSFULLY PUSHED TO GITHUB! ✅              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Get the URL
for /f "tokens=2" %%i in ('git remote get-url origin') do set REPO_URL=%%i

echo Your repository is now on GitHub:
echo.
echo %REPO_URL%
echo.

REM Offer to open browser
set /p OPEN_BROWSER="Open repository in browser? (Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    start %REPO_URL:.git=%
)

echo.
echo Next steps:
echo   1. Visit your GitHub repository
echo   2. Review your files
echo   3. Update README.md on GitHub
echo   4. Share the link with others
echo.

pause
exit /b 0
