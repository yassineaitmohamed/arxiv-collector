#!/usr/bin/env python3
"""
arXiv Collector - Collecte et affiche les articles arXiv
Par Yassine Ait
"""

import sqlite3
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import os
import sys

class ArxivCollector:
    def __init__(self, db_path="arxiv_collection.db"):
        self.db_path = db_path
        self.base_url = "http://export.arxiv.org/api/query"
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                arxiv_id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                abstract TEXT,
                category TEXT,
                published DATE,
                updated DATE,
                link TEXT,
                pdf_link TEXT,
                last_fetched TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fetch_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                fetch_date TIMESTAMP,
                articles_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def fetch_arxiv_articles(self, categories, start_date, end_date, max_results=1000):
        """Récupère les articles depuis arXiv API"""
        all_articles = []
        
        for category in categories:
            print(f"📥 Fetching {category}...", end=" ", flush=True)
            
            # Construction de la requête
            search_query = f"cat:{category}"
            params = {
                'search_query': search_query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                if response.status_code == 200:
                    articles = self.parse_arxiv_response(response.text, category, start_date, end_date)
                    all_articles.extend(articles)
                    print(f"✓ {len(articles)} articles")
                else:
                    print(f"✗ Error {response.status_code}")
                
                # Respecter les limites de l'API arXiv (3 secondes entre requêtes)
                time.sleep(3)
            
            except Exception as e:
                print(f"✗ Error: {e}")
        
        return all_articles
    
    def parse_arxiv_response(self, xml_content, category, start_date, end_date):
        """Parse la réponse XML de l'API arXiv"""
        articles = []
        root = ET.fromstring(xml_content)
        
        # Namespace pour arXiv
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        for entry in root.findall('atom:entry', ns):
            # ID arXiv
            id_elem = entry.find('atom:id', ns)
            arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else None
            
            # Date de publication
            published_elem = entry.find('atom:published', ns)
            if published_elem is not None:
                published_date = datetime.fromisoformat(published_elem.text.replace('Z', '+00:00'))
                
                # Convertir start_date et end_date en timezone-aware si nécessaire
                if start_date.tzinfo is None:
                    from datetime import timezone
                    start_date = start_date.replace(tzinfo=timezone.utc)
                if end_date.tzinfo is None:
                    from datetime import timezone
                    end_date = end_date.replace(tzinfo=timezone.utc)
                
                # Filtrer par date
                if published_date < start_date or published_date > end_date:
                    continue
            else:
                continue
            
            # Titre
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "No title"
            
            # Auteurs
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None:
                    authors.append(name_elem.text)
            authors_str = "; ".join(authors)
            
            # Abstract
            summary_elem = entry.find('atom:summary', ns)
            abstract = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else ""
            
            # Date de mise à jour
            updated_elem = entry.find('atom:updated', ns)
            updated_date = datetime.fromisoformat(updated_elem.text.replace('Z', '+00:00')) if updated_elem is not None else published_date
            
            # Liens
            link = f"https://arxiv.org/abs/{arxiv_id}"
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            articles.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors_str,
                'abstract': abstract,
                'category': category,
                'published': published_date,
                'updated': updated_date,
                'link': link,
                'pdf_link': pdf_link
            })
        
        return articles
    
    def save_articles(self, articles):
        """Sauvegarde les articles dans la base de données"""
        if not articles:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        count = 0
        for article in articles:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO articles 
                    (arxiv_id, title, authors, abstract, category, published, updated, link, pdf_link, last_fetched)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article['arxiv_id'],
                    article['title'],
                    article['authors'],
                    article['abstract'],
                    article['category'],
                    article['published'],
                    article['updated'],
                    article['link'],
                    article['pdf_link'],
                    datetime.now()
                ))
                count += 1
            except sqlite3.IntegrityError:
                pass  # Article déjà existant
        
        conn.commit()
        conn.close()
        return count
    
    def update_collection(self, categories, days_back=2):
        """Met à jour la collection avec les nouveaux articles"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"\n🔄 Mise à jour de la collection")
        print(f"📅 Période: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")
        print(f"📚 Catégories: {', '.join(categories)}\n")
        
        articles = self.fetch_arxiv_articles(categories, start_date, end_date)
        saved = self.save_articles(articles)
        
        # Log de la mise à jour
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for category in categories:
            cursor.execute('''
                INSERT INTO fetch_log (category, fetch_date, articles_count)
                VALUES (?, ?, ?)
            ''', (category, datetime.now(), saved))
        conn.commit()
        conn.close()
        
        print(f"\n✅ {saved} articles ajoutés/mis à jour\n")
    
    def initial_collection(self, categories, start_year=2000):
        """Collection initiale depuis une année donnée"""
        end_date = datetime.now()
        start_date = datetime(start_year, 1, 1)
        
        print(f"\n🚀 Collection initiale")
        print(f"📅 Période: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")
        print(f"📚 Catégories: {', '.join(categories)}")
        print(f"⚠️  Cela peut prendre du temps...\n")
        
        # Collecter par année pour éviter de surcharger l'API
        current_year = start_year
        total_saved = 0
        
        while current_year <= end_date.year:
            year_start = datetime(current_year, 1, 1)
            year_end = datetime(current_year, 12, 31, 23, 59, 59)
            
            if year_end > end_date:
                year_end = end_date
            
            print(f"📆 Année {current_year}...")
            articles = self.fetch_arxiv_articles(categories, year_start, year_end, max_results=2000)
            saved = self.save_articles(articles)
            total_saved += saved
            print(f"   💾 {saved} articles sauvegardés\n")
            
            current_year += 1
            time.sleep(5)  # Pause entre années
        
        print(f"\n✅ Collection initiale terminée: {total_saved} articles au total\n")
    
    def search_articles(self, keyword=None, category=None, year=None, limit=100):
        """Recherche d'articles dans la collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM articles WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (title LIKE ? OR abstract LIKE ? OR authors LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if year:
            query += " AND strftime('%Y', published) = ?"
            params.append(str(year))
        
        query += " ORDER BY published DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def display_article(self, article, index=None):
        """Affiche un article de manière formatée"""
        if index is not None:
            print(f"\n{'='*80}")
            print(f"Article {index}")
            print(f"{'='*80}")
        else:
            print(f"\n{'='*80}")
        
        print(f"\n📄 Titre: {article[1]}")
        print(f"\n✍️  Auteurs: {article[2]}")
        print(f"\n📅 Date: {article[5][:10]}")
        print(f"\n🏷️  Catégorie: {article[4]}")
        print(f"\n📌 Citation arXiv: {article[0]}")
        print(f"\n🔗 Lien: {article[7]}")
        print(f"\n📥 PDF: {article[8]}")
        print(f"\n📝 Abstract:\n{article[3][:500]}{'...' if len(article[3]) > 500 else ''}")
        print(f"\n{'='*80}\n")
    
    def interactive_browser(self, articles):
        """Navigateur interactif pour parcourir les articles"""
        if not articles:
            print("❌ Aucun article trouvé.")
            return
        
        index = 0
        total = len(articles)
        
        print(f"\n📚 {total} articles trouvés")
        print("\nCommandes: [Enter]=suivant | [p]=précédent | [q]=quitter | [s]=recherche | [numero]=aller à\n")
        
        while True:
            self.display_article(articles[index], index + 1)
            print(f"[{index + 1}/{total}] ", end="")
            
            try:
                cmd = input("Commande: ").strip().lower()
                
                if cmd == '' or cmd == 'n':
                    index = (index + 1) % total
                elif cmd == 'p':
                    index = (index - 1) % total
                elif cmd == 'q':
                    break
                elif cmd.isdigit():
                    new_index = int(cmd) - 1
                    if 0 <= new_index < total:
                        index = new_index
                    else:
                        print(f"❌ Numéro invalide (1-{total})")
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir habibi!")
                break
    
    def stats(self):
        """Affiche les statistiques de la collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total d'articles
        cursor.execute("SELECT COUNT(*) FROM articles")
        total = cursor.fetchone()[0]
        
        # Par catégorie
        cursor.execute("SELECT category, COUNT(*) FROM articles GROUP BY category ORDER BY COUNT(*) DESC")
        by_category = cursor.fetchall()
        
        # Par année
        cursor.execute("SELECT strftime('%Y', published) as year, COUNT(*) FROM articles GROUP BY year ORDER BY year DESC LIMIT 10")
        by_year = cursor.fetchall()
        
        # Article le plus récent
        cursor.execute("SELECT title, published FROM articles ORDER BY published DESC LIMIT 1")
        latest = cursor.fetchone()
        
        conn.close()
        
        print(f"\n{'='*80}")
        print(f"📊 STATISTIQUES DE LA COLLECTION")
        print(f"{'='*80}\n")
        print(f"📚 Total d'articles: {total}\n")
        
        print(f"📂 Par catégorie:")
        for cat, count in by_category:
            print(f"   {cat}: {count}")
        
        print(f"\n📅 Par année (10 dernières):")
        for year, count in by_year:
            print(f"   {year}: {count}")
        
        if latest:
            print(f"\n🆕 Article le plus récent:")
            print(f"   {latest[0][:80]}...")
            print(f"   {latest[1][:10]}")
        
        print(f"\n{'='*80}\n")


def main():
    """Fonction principale"""
    collector = ArxivCollector()
    
    # Catégories par défaut
    categories = ['math.DG', 'math.SG', 'math-ph', 'math.AG', 'math.QA', 'math.RT']
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'init':
            # Collection initiale
            year = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
            collector.initial_collection(categories, start_year=year)
        
        elif cmd == 'update':
            # Mise à jour
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 2
            collector.update_collection(categories, days_back=days)
        
        elif cmd == 'stats':
            # Statistiques
            collector.stats()
        
        elif cmd == 'search':
            # Recherche
            keyword = sys.argv[2] if len(sys.argv) > 2 else None
            articles = collector.search_articles(keyword=keyword)
            collector.interactive_browser(articles)
        
        elif cmd == 'browse':
            # Navigation libre
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            articles = collector.search_articles(limit=limit)
            collector.interactive_browser(articles)
        
        else:
            print("❌ Commande inconnue")
            print_usage()
    
    else:
        print_usage()


def print_usage():
    """Affiche l'aide"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                           arXiv COLLECTOR                                  ║
║                      Collection d'articles arXiv                           ║
╚════════════════════════════════════════════════════════════════════════════╝

UTILISATION:

    python3 arxiv_collector.py <commande> [options]

COMMANDES:

    init [année]        Collection initiale depuis année (défaut: 2000)
                        Ex: python3 arxiv_collector.py init 2020
    
    update [jours]      Mise à jour avec articles des X derniers jours (défaut: 2)
                        Ex: python3 arxiv_collector.py update 7
    
    browse [limite]     Parcourir les articles (défaut: 100 derniers)
                        Ex: python3 arxiv_collector.py browse 50
    
    search <mot-clé>    Rechercher par mot-clé
                        Ex: python3 arxiv_collector.py search "Poisson"
    
    stats               Afficher les statistiques de la collection

CATÉGORIES:
    math.DG, math.SG, math-ph, math.AG, math.QA, math.RT

EXEMPLES:

    # Première utilisation - collection depuis 2020
    python3 arxiv_collector.py init 2020
    
    # Mise à jour tous les 2 jours
    python3 arxiv_collector.py update
    
    # Parcourir les 50 derniers articles
    python3 arxiv_collector.py browse 50
    
    # Rechercher "symplectic"
    python3 arxiv_collector.py search symplectic
    
    # Voir les stats
    python3 arxiv_collector.py stats

📝 Note: Utilisez un cron job pour automatiser la mise à jour tous les 2 jours
    """)


if __name__ == "__main__":
    main()
