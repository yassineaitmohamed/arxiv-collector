# GitHub Publishing Guide 🚀

Step-by-step instructions to publish your arXiv Collector on GitHub.

---

## Prerequisites

Before starting, make sure you have:

1. ✅ A GitHub account (create one at https://github.com if needed)
2. ✅ Git installed on your computer
3. ✅ All project files ready in `~/Desktop/arxiv_collector/`

---

## Step 1: Prepare Your Repository on GitHub

### Create a New Repository

1. Go to https://github.com and log in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**

4. Fill in the details:
   - **Repository name**: `arxiv-collector`
   - **Description**: "A comprehensive terminal-based tool for collecting and browsing arXiv papers"
   - **Visibility**: Choose **Public** (or Private if you prefer)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these!)

5. Click **"Create repository"**

6. **Save the repository URL** shown on the next page:
   ```
   https://github.com/yourusername/arxiv-collector.git
   ```

---

## Step 2: Prepare Your Local Files

Open Terminal and navigate to your project:

```bash
# Go to your project directory
cd ~/Desktop/arxiv_collector

# Verify you're in the right place
pwd
ls -la
```

### Add the New Files

Copy the new files I created into your project:

```bash
# If you have the new README, .gitignore, LICENSE, and INSTALLATION.md
# they should be in your arxiv_collector directory

# Verify the files are there
ls -la

# You should see:
# - README.md (the new English version)
# - .gitignore
# - LICENSE
# - INSTALLATION.md
# - all your Python scripts
# - categories.txt
# - auto_update.sh
```

**Important:** Make sure you have:
- ✅ New `README.md` (English version with installation instructions)
- ✅ `.gitignore` (to exclude database and log files)
- ✅ `LICENSE` (MIT License)
- ✅ `INSTALLATION.md` (detailed setup guide)

---

## Step 3: Initialize Git Repository

```bash
# Make sure you're in the project directory
cd ~/Desktop/arxiv_collector

# Initialize git (if not already done)
git init

# Check git status
git status
# You should see all your files as "untracked"
```

---

## Step 4: Configure Git (First Time Only)

If this is your first time using Git on this computer:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use the same email as your GitHub account)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list | grep user
```

---

## Step 5: Stage and Commit Your Files

```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
# Green files = will be committed
# .db and .log files should NOT appear (excluded by .gitignore)

# Create your first commit
git commit -m "Initial commit: arXiv Collector v1.0"

# Verify the commit
git log --oneline
```

---

## Step 6: Connect to GitHub

```bash
# Add the remote repository (replace with YOUR repository URL)
git remote add origin https://github.com/yourusername/arxiv-collector.git

# Verify the remote was added
git remote -v
# Should show:
# origin  https://github.com/yourusername/arxiv-collector.git (fetch)
# origin  https://github.com/yourusername/arxiv-collector.git (push)
```

---

## Step 7: Push to GitHub

```bash
# Push your code to GitHub
git push -u origin main

# If you get an error about "master" vs "main":
git branch -M main
git push -u origin main
```

**Authentication:**

GitHub may ask for authentication. You have two options:

**Option A: Personal Access Token (Recommended)**

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "arXiv Collector"
4. Select scopes: `repo` (full control of private repositories)
5. Generate and **COPY THE TOKEN** (you won't see it again!)
6. When git asks for password, paste the token

**Option B: SSH Key**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Add it to GitHub:
# GitHub.com → Settings → SSH and GPG keys → New SSH key
# Paste the key and save

# Then use SSH URL instead:
git remote set-url origin git@github.com:yourusername/arxiv-collector.git
git push -u origin main
```

---

## Step 8: Verify on GitHub

1. Go to `https://github.com/yourusername/arxiv-collector`
2. You should see:
   - ✅ All your files listed
   - ✅ README.md displayed on the main page
   - ✅ Green "Code" button
   - ✅ Your commit message

3. Check that `.gitignore` worked:
   - ✅ NO `arxiv_collection.db` file
   - ✅ NO `update.log` file

---

## Step 9: Make Your Repository Look Professional

### Add Topics/Tags

1. On your repository page, click the gear icon ⚙️ next to "About"
2. Add topics:
   - `arxiv`
   - `python`
   - `research-tool`
   - `academic`
   - `mathematics`
   - `papers`
   - `terminal`
   - `sqlite`
3. Save changes

### Add Repository Description

In the same "About" section:
- Description: "📚 Terminal-based tool for collecting, searching, and browsing arXiv papers with automated updates"
- Website: (your website if you have one)

### Create Releases (Optional)

1. Click "Releases" → "Create a new release"
2. Tag version: `v1.0.0`
3. Release title: `arXiv Collector v1.0.0 - Initial Release`
4. Description:
   ```markdown
   ## 🎉 First Release
   
   Complete tool for managing arXiv papers from your terminal.
   
   ### Features
   - Collection from any year
   - Automatic updates
   - Search and browse
   - Multiple interfaces (terminal, table, GUI)
   
   ### Installation
   See [INSTALLATION.md](INSTALLATION.md) for details.
   ```
5. Publish release

---

## Step 10: Future Updates

When you make changes to your code:

```bash
# 1. Check what changed
git status

# 2. Stage changes
git add .
# Or stage specific files:
git add arxiv_collector.py

# 3. Commit with a meaningful message
git commit -m "Add feature: export to BibTeX"

# 4. Push to GitHub
git push

# That's it! Your changes are now on GitHub
```

---

## Common Git Commands Reference

```bash
# Check status of your files
git status

# See your commit history
git log --oneline

# See what changed in files
git diff

# Undo changes to a file (before staging)
git checkout -- filename.py

# Unstage a file (after git add)
git reset HEAD filename.py

# Create a new branch
git checkout -b feature-name

# Switch between branches
git checkout main
git checkout feature-name

# Merge a branch
git checkout main
git merge feature-name

# Pull latest changes from GitHub
git pull

# See remotes
git remote -v
```

---

## Best Practices

### Commit Messages

Good commit messages:
- ✅ `Add feature: export papers to BibTeX format`
- ✅ `Fix bug: handle missing author names`
- ✅ `Update README: add Windows installation steps`
- ✅ `Improve performance: optimize database queries`

Bad commit messages:
- ❌ `update`
- ❌ `fix`
- ❌ `changes`
- ❌ `asdf`

### What to Commit

DO commit:
- ✅ Source code (`.py` files)
- ✅ Configuration files (`.txt`, `.sh`)
- ✅ Documentation (`.md` files)
- ✅ License and README

DO NOT commit:
- ❌ Database files (`.db`)
- ❌ Log files (`.log`)
- ❌ Personal data
- ❌ API keys or passwords
- ❌ Large binary files

### Branching Strategy

For features or experiments:
```bash
# Create a feature branch
git checkout -b feature/bibtex-export

# Work on your feature
# ... make changes ...

# Commit your work
git add .
git commit -m "Add BibTeX export functionality"

# Push the branch
git push -u origin feature/bibtex-export

# On GitHub, create a Pull Request
# After review, merge to main
```

---

## Troubleshooting

### "fatal: not a git repository"

```bash
# Initialize git
git init
```

### "error: failed to push"

```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### "Authentication failed"

```bash
# Use personal access token as password
# Or set up SSH key (see Step 7)
```

### "refusing to merge unrelated histories"

```bash
# If you initialized README on GitHub:
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Accidentally committed database file

```bash
# Remove from git but keep local file
git rm --cached arxiv_collection.db
git commit -m "Remove database file from git"
git push

# Make sure .gitignore includes *.db
echo "*.db" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore to exclude database files"
git push
```

---

## Adding Collaborators

If you want others to contribute:

1. Go to your repository on GitHub
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Enter their GitHub username
5. They'll receive an invitation

---

## Making Your Repository Popular

### Add Badges to README

At the top of your README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub stars](https://img.shields.io/github/stars/yourusername/arxiv-collector)
```

### Share It

- Tweet about it with #arXiv #Python #AcademicTools
- Post on Reddit (r/Python, r/academia, r/mathematics)
- Share in math/physics Discord servers
- Add to lists like "awesome-python" or "awesome-research-tools"

---

## Next Steps

After publishing:

1. ✅ Share the repository link with colleagues
2. ✅ Add it to your CV/website
3. ✅ Monitor for issues or pull requests
4. ✅ Keep updating with new features
5. ✅ Respond to user feedback

---

**Congratulations habibi! Your code is now on GitHub! 🎉**

Your repository: `https://github.com/yourusername/arxiv-collector`

Share it with the world! 🌍
