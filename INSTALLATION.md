# Installation Guide 🚀

Complete step-by-step installation instructions for arXiv Collector.

---

## Prerequisites

- **Python 3.6+** (check with `python3 --version`)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Terminal/Command Line** access

---

## Installation Steps

### Step 1: Create Project Directory

Open your terminal and navigate to your Desktop (or preferred location):

```bash
# Navigate to Desktop
cd ~/Desktop

# Verify you're in the right place
pwd
# Should show: /Users/yourusername/Desktop (macOS)
#          or: /home/yourusername/Desktop (Linux)
```

### Step 2: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/arxiv-collector.git

# You should see output like:
# Cloning into 'arxiv-collector'...
# remote: Enumerating objects: ...
# Receiving objects: 100% ...
```

### Step 3: Enter the Project Directory

```bash
# Move into the project folder
cd arxiv-collector

# List files to verify
ls -la

# You should see:
# arxiv_collector.py
# arxiv_table.py
# arxiv_gui.py
# auto_update.sh
# categories.txt
# README.md
# LICENSE
# .gitignore
```

### Step 4: Install Python Dependencies

```bash
# Install the requests library
pip3 install requests

# If you get a permission error, try:
pip3 install --user requests

# Or using pip (without the 3):
pip install requests
```

**Verify installation:**
```bash
python3 -c "import requests; print('requests installed successfully!')"
```

### Step 5: Make Scripts Executable (macOS/Linux)

```bash
# Make all Python scripts executable
chmod +x arxiv_collector.py
chmod +x arxiv_table.py
chmod +x arxiv_gui.py
chmod +x auto_update.sh

# Verify permissions
ls -l *.py *.sh
# You should see -rwxr-xr-x for executable files
```

### Step 6: Test the Installation

```bash
# Test the main script
python3 arxiv_collector.py

# You should see usage information
# If you see an error, check Python and dependencies
```

---

## First Time Setup

### Initialize Your Database

Choose one of these options based on how much data you want:

**Option A: Quick Test (2024 only - fastest)**
```bash
python3 arxiv_collector.py init 2024
# Takes ~10-30 minutes
```

**Option B: Recent Papers (2020-present - recommended)**
```bash
python3 arxiv_collector.py init 2020
# Takes ~1-3 hours
```

**Option C: Full Archive (2000-present - comprehensive)**
```bash
python3 arxiv_collector.py init 2000
# Takes 4-8 hours
# Recommended: Run overnight or in background
```

**Run in Background (macOS/Linux):**
```bash
# Start the collection and detach from terminal
nohup python3 arxiv_collector.py init 2020 > init.log 2>&1 &

# Check progress
tail -f init.log

# Check if still running
ps aux | grep arxiv_collector
```

### Verify the Collection

```bash
# Check database was created
ls -lh arxiv_collection.db

# View statistics
python3 arxiv_collector.py stats

# Browse some papers
python3 arxiv_collector.py browse 10
```

---

## Setup Automatic Updates

### macOS/Linux: Using Cron

**Step 1: Test the update script**
```bash
./auto_update.sh
```

**Step 2: Open crontab**
```bash
crontab -e
```

**Step 3: Add cron job**

Press `i` to enter insert mode (if using vim), then add:

```bash
# Update every 2 days at 8:00 AM
0 8 */2 * * /Users/yourusername/Desktop/arxiv-collector/auto_update.sh
```

**Important:** Replace `/Users/yourusername/Desktop/arxiv-collector/` with your actual path:
```bash
# Find your full path
pwd
# Copy the output and use it in crontab
```

**Step 4: Save and exit**
- Press `ESC`
- Type `:wq` and press `Enter`

**Step 5: Verify cron job**
```bash
# List your cron jobs
crontab -l

# You should see your new entry
```

**Cron Time Examples:**
```bash
# Every day at 8 PM
0 20 * * * /path/to/auto_update.sh

# Every Monday at 6 AM
0 6 * * 1 /path/to/auto_update.sh

# Every weekday at noon
0 12 * * 1-5 /path/to/auto_update.sh

# Every 3 days at 9 AM
0 9 */3 * * /path/to/auto_update.sh
```

### Windows: Using Task Scheduler

**Step 1: Create a batch file**

Create `auto_update.bat`:
```batch
@echo off
cd C:\Users\yourusername\Desktop\arxiv-collector
python arxiv_collector.py update 2 >> update.log 2>&1
```

**Step 2: Open Task Scheduler**
- Press `Win + R`
- Type `taskschd.msc` and press Enter

**Step 3: Create Basic Task**
- Click "Create Basic Task"
- Name: "arXiv Collector Update"
- Trigger: Daily
- Repeat: Every 2 days
- Action: Start a program
- Program: `C:\Users\yourusername\Desktop\arxiv-collector\auto_update.bat`

---

## Optional: GUI Setup

### Install tkinter (if needed)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
# tkinter is usually pre-installed
# If not, reinstall Python from python.org
```

**Test tkinter:**
```bash
python3 -c "import tkinter; print('tkinter is ready!')"
```

### Launch GUI

```bash
python3 arxiv_gui.py
```

---

## Customization

### Configure Categories

Edit the `categories.txt` file to customize which arXiv categories you want to track:

```bash
# Open in your text editor
nano categories.txt

# Or
vim categories.txt

# Or on macOS
open -e categories.txt
```

**Available categories:**
- `math.DG` - Differential Geometry
- `math.SG` - Symplectic Geometry
- `math.AG` - Algebraic Geometry
- `math.QA` - Quantum Algebra
- `math.RT` - Representation Theory
- `math.CT` - Category Theory
- `math-ph` - Mathematical Physics
- `hep-th` - High Energy Physics - Theory
- `gr-qc` - General Relativity
- `quant-ph` - Quantum Physics

Find all categories at: https://arxiv.org/category_taxonomy

---

## Verification Checklist

✅ Python 3.6+ installed  
✅ `requests` library installed  
✅ Repository cloned to Desktop  
✅ Scripts made executable  
✅ Database initialized with papers  
✅ Can browse papers successfully  
✅ Update script works  
✅ (Optional) Cron job configured  
✅ (Optional) GUI launches  

---

## Troubleshooting

### "command not found: python3"

Try `python` instead:
```bash
python --version
python arxiv_collector.py
```

Or install Python 3:
```bash
# macOS
brew install python3

# Linux (Ubuntu/Debian)
sudo apt-get install python3

# Linux (Fedora)
sudo dnf install python3
```

### "No module named 'requests'"

```bash
pip3 install requests
# If that fails:
python3 -m pip install requests
# Or:
pip install --user requests
```

### "Permission denied"

```bash
# Make scripts executable
chmod +x *.py *.sh

# Or run with python3 explicitly
python3 arxiv_collector.py
```

### Database is empty after init

```bash
# Check if init completed
tail -n 20 nohup.out  # If you used nohup

# Try again with verbose output
python3 arxiv_collector.py init 2024
```

### Cron job not working

```bash
# Check cron is running
ps aux | grep cron

# Check crontab
crontab -l

# Use full paths in crontab
# ❌ BAD: 0 8 */2 * * ./auto_update.sh
# ✅ GOOD: 0 8 */2 * * /Users/you/Desktop/arxiv-collector/auto_update.sh

# Check update log
cat update.log
```

---

## Next Steps

Once installed:

1. **Daily Update Routine**: `python3 arxiv_collector.py update && python3 arxiv_collector.py browse 20`
2. **Quick Search**: `python3 arxiv_collector.py search "your research topic"`
3. **Table View**: `python3 arxiv_table.py` for quick scanning
4. **GUI Browsing**: `python3 arxiv_gui.py` for comfortable reading

---

## Getting Help

If you encounter issues:

1. Check this installation guide thoroughly
2. Check the main [README.md](README.md)
3. Look at [Troubleshooting section](#troubleshooting)
4. Open an issue on GitHub with:
   - Your OS and Python version
   - Complete error message
   - Steps you've tried

---

**Habibi, you're all set! Start collecting papers! 📚**
