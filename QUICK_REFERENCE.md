# Quick Commands Reference 🚀

All the essential commands you need to publish arXiv Collector on GitHub.

---

## 📋 Copy-Paste Commands

### 1. Navigate to Your Project

```bash
cd ~/Desktop/arxiv_collector
pwd
ls -la
```

---

### 2. Initialize Git (if needed)

```bash
git init
```

---

### 3. Configure Git (First Time Only)

```bash
# Replace with YOUR information
git config --global user.name "Yassine Ait Mohamed"
git config --global user.email "your.email@example.com"
```

---

### 4. Stage All Files

```bash
git add .
git status
```

---

### 5. First Commit

```bash
git commit -m "Initial commit: arXiv Collector v1.0 - Terminal tool for collecting and browsing arXiv papers"
```

---

### 6. Connect to GitHub

**First, create the repository on GitHub.com, then:**

```bash
# Replace 'yourusername' with YOUR GitHub username
git remote add origin https://github.com/yourusername/arxiv-collector.git

# Verify
git remote -v
```

---

### 7. Push to GitHub

```bash
# Set main as default branch
git branch -M main

# Push
git push -u origin main
```

---

## 🔄 For Future Updates

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Your update message here"

# Push to GitHub
git push
```

---

## 🆘 Common Problems & Solutions

### Problem: "Authentication failed"

**Solution:** Use a Personal Access Token

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy the token
5. When git asks for password, paste the token

---

### Problem: "fatal: not a git repository"

```bash
git init
```

---

### Problem: "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

### Problem: Accidentally committed database file

```bash
# Remove from git but keep local file
git rm --cached arxiv_collection.db
git commit -m "Remove database file"
git push

# Make sure .gitignore is correct
cat .gitignore | grep "*.db"
```

---

## 📝 One-Line Installation Command (for users)

After publishing, users can install with:

```bash
cd ~/Desktop && git clone https://github.com/yourusername/arxiv-collector.git && cd arxiv-collector && pip3 install requests && chmod +x *.py *.sh && python3 arxiv_collector.py
```

---

## 🎯 Complete Workflow (Start to Finish)

```bash
# 1. Go to project
cd ~/Desktop/arxiv_collector

# 2. Initialize
git init

# 3. Add files
git add .

# 4. First commit
git commit -m "Initial commit: arXiv Collector v1.0"

# 5. Connect to GitHub (replace URL with yours)
git remote add origin https://github.com/yourusername/arxiv-collector.git

# 6. Push
git branch -M main
git push -u origin main
```

---

## 🔗 Your Repository URLs

After creation, your repository will be at:

- **Web**: `https://github.com/yourusername/arxiv-collector`
- **Clone (HTTPS)**: `https://github.com/yourusername/arxiv-collector.git`
- **Clone (SSH)**: `git@github.com:yourusername/arxiv-collector.git`

---

## ✅ Pre-Flight Checklist

Before pushing to GitHub, verify:

- [ ] All `.py` files are present
- [ ] `README.md` is complete
- [ ] `.gitignore` exists and excludes `.db` and `.log`
- [ ] `LICENSE` file is present
- [ ] `categories.txt` is included
- [ ] `auto_update.sh` is executable (`chmod +x auto_update.sh`)
- [ ] NO database files (`.db`) are staged
- [ ] NO log files (`.log`) are staged

Check with:
```bash
git status
# Should NOT see: arxiv_collection.db, update.log
```

---

## 🎨 Optional: Add Badges to README

Add these at the top of README.md:

```markdown
# arXiv Collector 📚

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)

[rest of README...]
```

---

**Habibi, everything is ready! Just follow the commands above! 🚀**
