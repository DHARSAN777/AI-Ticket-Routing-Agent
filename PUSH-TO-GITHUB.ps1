# Ticket Agent - Push to GitHub PowerShell Script
# This script automatically pushes your project to GitHub

param(
    [string]$RepoUrl = "https://github.com/DHARSAN777/AI-Ticket-Routing-Agent.git",
    [string]$CommitMessage = "Initial commit: Ticket Agent - AI-powered support system",
    [string]$GitHubToken = ""
)

# Colors for output
$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

Write-Host "`n$Blue╔════════════════════════════════════════════════════╗$Reset" 
Write-Host "$Blue║                                                    ║$Reset"
Write-Host "$Blue║   🎫 TICKET AGENT - PUSH TO GITHUB 🎫            ║$Reset"
Write-Host "$Blue║                                                    ║$Reset"
Write-Host "$Blue╚════════════════════════════════════════════════════╝$Reset`n"

# Function to execute command and check result
function Execute-Command {
    param(
        [string]$Description,
        [string]$Command
    )
    
    Write-Host "$Yellow➤ $Description...$Reset"
    
    try {
        Invoke-Expression $Command 2>&1 | Out-String -Stream | ForEach-Object { Write-Host "  $_" }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "$Green✓ $Description completed$Reset`n"
            return $true
        } else {
            Write-Host "$Red✗ $Description failed (Error code: $LASTEXITCODE)$Reset`n"
            return $false
        }
    }
    catch {
        Write-Host "$Red✗ $Description failed: $_$Reset`n"
        return $false
    }
}

# Check if Git is installed
Write-Host "$Yellow➤ Checking Git installation...$Reset"
try {
    $gitVersion = git --version 2>&1
    Write-Host "  $gitVersion"
    Write-Host "$Green✓ Git found$Reset`n"
}
catch {
    Write-Host "$Red✗ Git not found. Please install Git from https://git-scm.com/download/win$Reset"
    exit 1
}

# Navigate to project directory
$projectDir = "c:\Users\dhars\Downloads\project\ticket agent"
Write-Host "$Yellow➤ Navigating to project directory...$Reset"
Write-Host "  $projectDir"

if (Test-Path $projectDir) {
    Set-Location $projectDir
    Write-Host "$Green✓ Project directory found$Reset`n"
} else {
    Write-Host "$Red✗ Project directory not found: $projectDir$Reset"
    exit 1
}

# Check for backend folder (verification)
if (Test-Path "backend") {
    Write-Host "$Green✓ Project structure verified$Reset`n"
} else {
    Write-Host "$Red✗ Invalid project structure$Reset"
    exit 1
}

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    if (-not (Execute-Command "Initializing Git repository" "git init")) {
        exit 1
    }
}

# Create .gitignore
Write-Host "$Yellow➤ Setting up .gitignore...$Reset"
$gitignoreContent = @"
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.sqlite3
chroma_data/

# Logs
*.log
npm-debug.log

# Node
node_modules/
package-lock.json

# Temporary
.tmp/
temp/
"@

$gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8 -Force
Write-Host "$Green✓ .gitignore created$Reset`n"

# Configure git user
Write-Host "$Yellow➤ Checking Git configuration...$Reset"
$gitUserName = git config --global user.name 2>&1
$gitUserEmail = git config --global user.email 2>&1

if ([string]::IsNullOrWhiteSpace($gitUserName)) {
    Write-Host "$Yellow  Git user not configured. Setting defaults...$Reset"
    git config --global user.name "Ticket Agent Developer" 2>&1 | Out-Null
    git config --global user.email "dev@ticket-agent.local" 2>&1 | Out-Null
    Write-Host "$Green✓ Git user configured$Reset"
} else {
    Write-Host "$Green✓ Git user: $gitUserName ($gitUserEmail)$Reset"
}
Write-Host ""

# Stage all files
if (-not (Execute-Command "Staging files" "git add .")) {
    exit 1
}

# Show git status
Write-Host "$Yellow➤ Git status:$Reset"
git status 2>&1 | Out-String -Stream | ForEach-Object { Write-Host "  $_" }
Write-Host ""

# Commit files
if (-not (Execute-Command "Creating commit" "git commit -m `"$CommitMessage`"")) {
    Write-Host "$Yellow⚠ Note: Commit may have failed if files were already committed$Reset`n"
}

# Check if remote exists
$remoteExists = git remote | Select-String "origin" -Quiet

if (-not $remoteExists) {
    if (-not (Execute-Command "Adding remote repository" "git remote add origin $RepoUrl")) {
        exit 1
    }
} else {
    Write-Host "$Green✓ Remote already configured$Reset`n"
}

# Verify remote
Write-Host "$Yellow➤ Verifying remote configuration...$Reset"
git remote -v 2>&1 | Out-String -Stream | ForEach-Object { Write-Host "  $_" }
Write-Host ""

# Push to GitHub
Write-Host "$Yellow➤ Pushing to GitHub...$Reset"
Write-Host "  Repository: $RepoUrl"
Write-Host "  Branch: main"
Write-Host ""

try {
    # Try to push to main branch
    git push -u origin main 2>&1 | Out-String -Stream | ForEach-Object { 
        if ($_ -match "error|fatal|refused") {
            Write-Host "$Red  $_$Reset"
        } else {
            Write-Host "  $_"
        }
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "$Green✓ Push completed successfully$Reset`n"
    } else {
        Write-Host "$Yellow⚠ Push may have failed. Check GitHub for details.$Reset`n"
    }
}
catch {
    Write-Host "$Red✗ Push failed: $_$Reset`n"
}

# Final summary
Write-Host "$Blue╔════════════════════════════════════════════════════╗$Reset"
Write-Host "$Blue║                                                    ║$Reset"
Write-Host "$Blue║      ✅ PUSH PROCESS COMPLETED ✅                 ║$Reset"
Write-Host "$Blue║                                                    ║$Reset"
Write-Host "$Blue╚════════════════════════════════════════════════════╝$Reset`n"

Write-Host "$Green📊 Summary:$Reset"
Write-Host "  Repository: $RepoUrl"
Write-Host "  Branch: main"
Write-Host "  Project: Ticket Agent"
Write-Host ""

Write-Host "$Green🎯 Next steps:$Reset"
Write-Host "  1. Visit: https://github.com/DHARSAN777/AI-Ticket-Routing-Agent"
Write-Host "  2. Verify all files are present"
Write-Host "  3. Share the link with others"
Write-Host ""

Write-Host "$Yellow📝 To make future changes:$Reset"
Write-Host "  1. Edit files locally"
Write-Host "  2. Run: git add ."
Write-Host "  3. Run: git commit -m `"Your message`""
Write-Host "  4. Run: git push"
Write-Host ""

Write-Host "$Green✨ Thank you for using Ticket Agent! 🎫$Reset`n"

# Keep window open
Read-Host "Press Enter to exit"
