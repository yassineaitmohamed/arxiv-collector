# arXiv Collector 📚

A comprehensive terminal-based tool for collecting, storing, and browsing arXiv papers with support for automated updates and multiple viewing interfaces.

**Author:** Yassine Ait Mohamed  

---

## 🎯 Features

- ✅ **Automated Collection**: Collect papers from arXiv since any year (e.g., 2000)
- ✅ **Smart Updates**: Automatic updates every 2 days via cron job
- ✅ **Local Storage**: SQLite database for offline access
- ✅ **Multiple Interfaces**: 
  - Terminal browser with navigation
  - Table view for quick scanning
  - GUI application (dark/light themes)
- ✅ **Search & Filter**: By keyword, category, year, or author
- ✅ **Customizable Categories**: Easy configuration via `categories.txt`
- ✅ **Export**: Generate markdown reports of your collection

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
# Navigate to your Desktop (or preferred location)
cd ~/Desktop

# Clone the repository
git clone https://github.com/yourusername/arxiv-collector.git

# Enter the project directory
cd arxiv-collector
```

### Step 2: Install Dependencies

```bash
# Install required Python packages
pip3 install requests

# Or if you prefer using pip
pip install requests

# For GUI interface (optional)
# tkinter is usually pre-installed with Python
# If not available on Linux:
sudo apt-get install python3-tk
```

### Step 3: Set Up Automatic Updates (Optional)

```bash
# Make the update script executable
chmod +x auto_update.sh

# Test the update script
./auto_update.sh
```

---

## 🚀 Quick Start

### First Time: Initial Collection

Collecting papers for the first time creates your local database. The duration depends on how far back you go:

```bash
# Collect all papers since 2020 (recommended - faster)
python3 arxiv_collector.py init 2020

# Or collect since 2000 (may take several hours!)
python3 arxiv_collector.py init 2000

# For testing, try just 2024
python3 arxiv_collector.py init 2024
```

**Note**: The initial collection respects arXiv's API rate limits (3-second delays between requests).

### Regular Updates

After the initial collection, keep your database current:

```bash
# Update with papers from last 2 days (default)
python3 arxiv_collector.py update

# Update with papers from last 7 days
python3 arxiv_collector.py update 7

# Update with papers from last 30 days
python3 arxiv_collector.py update 30
```

---

## 📖 Usage

### Browse Your Collection

Navigate through your collected papers interactively:

```bash
# Browse the 100 most recent papers
python3 arxiv_collector.py browse

# Browse only the 50 most recent papers
python3 arxiv_collector.py browse 50
```

**Navigation Commands:**
- `Enter` or `n`: Next article
- `p`: Previous article
- `q`: Quit browser
- `<number>`: Jump to article number

### Search Papers

```bash
# Search for "Poisson"
python3 arxiv_collector.py search Poisson

# Search for "symplectic"
python3 arxiv_collector.py search symplectic

# Search with multiple words (use quotes)
python3 arxiv_collector.py search "Lie algebroid"

# Search in titles only
python3 arxiv_collector.py search "shifted symplectic"
```

### Table View Interface

Quick overview in a compact table format:

```bash
# Interactive menu
python3 arxiv_table.py

# Or use direct commands:
python3 arxiv_table.py all 100        # Show 100 recent papers
python3 arxiv_table.py search Poisson  # Search for keyword
python3 arxiv_table.py cat math.SG     # Filter by category
python3 arxiv_table.py year 2024       # Filter by year
python3 arxiv_table.py details 2411.12345v1  # Show paper details
```

### GUI Application

Launch the graphical interface with dark/light theme support:

```bash
python3 arxiv_gui.py
```

**GUI Features:**
- 🌙 Dark/Light theme toggle
- 🔍 Real-time search filtering
- 📊 Category and year filters
- 🖱️ Click to open papers in browser
- 📝 View detailed abstracts
- 📈 Collection statistics

### View Statistics

```bash
python3 arxiv_collector.py stats
```

Shows:
- Total papers collected
- Papers per category
- Date range of collection
- Recent collection activity

---

## ⚙️ Automated Updates

### Option 1: Cron Job (macOS/Linux)

Set up automatic updates every 2 days:

```bash
# Open your crontab
crontab -e

# Add this line (runs at 8:00 AM every 2 days)
0 8 */2 * * /Users/yourusername/Desktop/arxiv-collector/auto_update.sh

# Save and exit (in vim: press ESC, then type :wq)
```

**Cron Time Examples:**
```bash
0 8 */2 * *   # Every 2 days at 8:00 AM
0 20 * * *    # Every day at 8:00 PM
0 6 * * 1     # Every Monday at 6:00 AM
0 12 * * 1-5  # Every weekday at noon
```

### Option 2: Manual Execution

```bash
# Run the update script manually
./auto_update.sh

# Check the log file
cat update.log

# Or tail the log to see latest entries
tail -n 50 update.log
```

---

## 📂 Project Structure

```
arxiv-collector/
├── arxiv_collector.py      # Main collection script
├── arxiv_table.py          # Table view interface
├── arxiv_gui.py            # GUI application
├── auto_update.sh          # Automated update script
├── categories.txt          # Categories configuration
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
│
├── arxiv_collection.db     # SQLite database (created on first run)
└── update.log              # Update logs (created by auto_update.sh)
```

**Note**: The database file (`arxiv_collection.db`) is not tracked in Git.

---

## 🏷️ Default Categories

The default categories are configured in `categories.txt`:

- `math.DG` - Differential Geometry
- `math.SG` - Symplectic Geometry  
- `math-ph` - Mathematical Physics
- `math.AG` - Algebraic Geometry
- `math.QA` - Quantum Algebra
- `math.RT` - Representation Theory

### Customize Categories

Edit `categories.txt` to add or remove categories:

```bash
# Open in your text editor
nano categories.txt

# Or
vim categories.txt

# Add one category per line
# Example additions:
# math.CT - Category Theory
# hep-th - High Energy Physics - Theory
# quant-ph - Quantum Physics
```

Find all available arXiv categories at: https://arxiv.org/category_taxonomy

---

## 📊 Sample Output

### Browse Mode:
```
================================================================================
Article 1/50
================================================================================

📄 Title: Poisson Structures on 1-Shifted Coisotropic Structures

✍️  Authors: John Doe; Jane Smith; Alice Johnson

📅 Published: 2024-11-20

🏷️  Category: math.SG

📌 arXiv ID: 2411.12345v1

🔗 Link: https://arxiv.org/abs/2411.12345
📥 PDF: https://arxiv.org/pdf/2411.12345.pdf

📝 Abstract:
We study Poisson structures arising from 1-shifted coisotropic structures
in derived symplectic geometry. Our main result establishes a natural
correspondence between...

================================================================================
[1/50] Command: 
```

### Table Mode:
```
+-----+----------------------------------------------------+-------------------------+--------+------------+--------------------------------+
| #   | TITLE                                              | AUTHOR                  | YEAR   | CATEGORY   | LINK                           |
+-----+----------------------------------------------------+-------------------------+--------+------------+--------------------------------+
| 1   | Poisson Structures on 1-Shifted Coisotropic...     | John Doe et al.         | 2024   | math.SG    | https://arxiv.org/abs/2411...  |
| 2   | Derived Symplectic Geometry and TQFT               | Jane Smith et al.       | 2024   | math.DG    | https://arxiv.org/abs/2411...  |
+-----+----------------------------------------------------+-------------------------+--------+------------+--------------------------------+

📊 Total: 2 articles
```

---

## 🔧 Technical Details

### Database Schema

**articles table:**
- `arxiv_id` (TEXT, PRIMARY KEY): Unique arXiv identifier
- `title` (TEXT): Paper title
- `authors` (TEXT): Semicolon-separated author list
- `abstract` (TEXT): Full abstract
- `category` (TEXT): Primary arXiv category
- `published` (DATE): Publication date
- `updated` (DATE): Last update date
- `link` (TEXT): arXiv abstract URL
- `pdf_link` (TEXT): Direct PDF URL
- `last_fetched` (TIMESTAMP): When the record was added

**fetch_log table:**
- `id` (INTEGER, PRIMARY KEY)
- `category` (TEXT): Category fetched
- `fetch_date` (TIMESTAMP): When the fetch occurred
- `articles_count` (INTEGER): Number of articles fetched

### arXiv API Limits

The script respects arXiv's API guidelines:
- 3-second delay between requests
- Maximum 1,000 results per query
- Automatic retry on connection errors

---

## 💡 Tips & Best Practices

### Performance

1. **Start Recent**: For your first collection, use `init 2020` or `init 2022` instead of `init 2000`
2. **Regular Updates**: Run `update` every 2-3 days to stay current without long wait times
3. **Targeted Search**: Use specific keywords for better search results
4. **Category Filter**: Use `arxiv_table.py cat math.SG` to quickly filter papers

### Workflow Suggestions

1. **Morning Routine**: Check new papers with `python3 arxiv_collector.py update && python3 arxiv_collector.py browse 20`
2. **Weekly Review**: Use table view to quickly scan the week's papers
3. **Research Session**: Use GUI for comfortable browsing with theme switching
4. **Export Lists**: Generate markdown reports for paper reviews or reading lists

### Database Maintenance

```bash
# Check database size
ls -lh arxiv_collection.db

# SQLite database can handle thousands of papers efficiently
# Typical size: ~1 MB per 100 papers with full abstracts

# Backup your database
cp arxiv_collection.db arxiv_collection_backup_$(date +%Y%m%d).db

# Reset database (WARNING: deletes all data!)
rm arxiv_collection.db
python3 arxiv_collector.py init 2024
```

---

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'requests'"**
```bash
pip3 install requests
# Or
python3 -m pip install requests
```

**"Permission denied" when running scripts**
```bash
chmod +x arxiv_collector.py
chmod +x arxiv_table.py
chmod +x arxiv_gui.py
chmod +x auto_update.sh
```

**Initial collection is very slow**
```bash
# This is normal! arXiv API requires 3-second delays
# Start with a recent year:
python3 arxiv_collector.py init 2022

# Let it run in the background:
nohup python3 arxiv_collector.py init 2020 &
```

**Too many results in browse mode**
```bash
# Limit to fewer papers
python3 arxiv_collector.py browse 20
```

**Cron job not running**
```bash
# Check if cron is running
ps aux | grep cron

# Check cron logs (macOS)
log show --predicate 'process == "cron"' --last 1d

# Check cron logs (Linux)
grep CRON /var/log/syslog
```

**GUI doesn't open**
```bash
# Check if tkinter is installed
python3 -c "import tkinter"

# On Linux, install tkinter:
sudo apt-get install python3-tk

# On macOS, tkinter should be pre-installed with Python
```

---

## 📚 Use Cases

This tool is designed for researchers who want to:

- **Stay Current**: Automatically track new publications in your field
- **Build Library**: Create a personal searchable archive of relevant papers
- **Discover Papers**: Browse by category to find papers you might have missed
- **Prepare Reviews**: Export and organize papers for literature reviews
- **Track Trends**: Monitor publication activity in specific areas
- **Offline Access**: Browse paper metadata without internet connection

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional export formats (BibTeX, CSV)
- Integration with reference managers (Zotero, Mendeley)
- Advanced search (boolean operators, regex)
- Paper recommendations based on reading history
- Web interface version
- Mobile-responsive design

Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 📧 Contact

**Yassine Ait Mohamed**  
PhD Student in Mathematics  
Université de Sherbrooke

For questions, suggestions, or collaboration:
- GitHub Issues: [Report a bug or request a feature]
- Email: [y.aitmohamed@yahoo.com]

---



---


*Built with ❤️ for the mathematical research community*
