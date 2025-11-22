#!/usr/bin/env python3
"""
arXiv Collector - Interface Tableau Terminal
Affichage des articles dans un tableau terminal
Par Yassine Ait
"""

import sqlite3
from datetime import datetime
import sys

class ArxivTableViewer:
    def __init__(self, db_path="arxiv_collection.db"):
        self.db_path = db_path
    
    def get_articles(self, search_query=None, category=None, year=None, limit=100):
        """Récupère les articles avec filtres"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT arxiv_id, title, authors, category, published, link FROM articles WHERE 1=1"
        params = []
        
        if search_query:
            query += " AND (title LIKE ? OR abstract LIKE ? OR authors LIKE ?)"
            search_term = f"%{search_query}%"
            params.extend([search_term, search_term, search_term])
        
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
    
    def truncate_text(self, text, max_length):
        """Tronque le texte à une longueur maximale"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def get_first_author(self, authors_str):
        """Récupère le premier auteur"""
        if not authors_str:
            return "Unknown"
        authors = authors_str.split(";")
        first = authors[0].strip()
        if len(authors) > 1:
            return first + " et al."
        return first
    
    def display_table(self, articles):
        """Affiche les articles dans un tableau"""
        if not articles:
            print("\n❌ Aucun article trouvé.\n")
            return
        
        # Largeurs des colonnes
        col_num = 5
        col_titre = 50
        col_auteur = 25
        col_annee = 6
        col_cat = 10
        col_link = 30
        
        # Ligne de séparation
        separator = "+" + "-" * col_num + "+" + "-" * col_titre + "+" + "-" * col_auteur + "+" + "-" * col_annee + "+" + "-" * col_cat + "+" + "-" * col_link + "+"
        
        # En-tête
        print("\n" + separator)
        print(f"| {'#':<{col_num-2}} | {'TITRE':<{col_titre-2}} | {'AUTEUR':<{col_auteur-2}} | {'ANNÉE':<{col_annee-2}} | {'CAT':<{col_cat-2}} | {'LIEN':<{col_link-2}} |")
        print(separator)
        
        # Articles
        for idx, article in enumerate(articles, 1):
            arxiv_id = article[0]
            titre = self.truncate_text(article[1], col_titre - 2)
            auteurs = self.truncate_text(self.get_first_author(article[2]), col_auteur - 2)
            annee = article[4][:4] if article[4] else "????"
            categorie = article[3][:col_cat-2] if article[3] else "???"
            link = self.truncate_text(article[5], col_link - 2)
            
            print(f"| {idx:<{col_num-2}} | {titre:<{col_titre-2}} | {auteurs:<{col_auteur-2}} | {annee:<{col_annee-2}} | {categorie:<{col_cat-2}} | {link:<{col_link-2}} |")
        
        print(separator)
        print(f"\n📊 Total: {len(articles)} articles\n")
    
    def interactive_menu(self):
        """Menu interactif"""
        while True:
            print("\n" + "="*80)
            print("📚 arXiv COLLECTOR - Vue Tableau")
            print("="*80)
            print("\nOptions:")
            print("  1. Afficher tous les articles récents")
            print("  2. Rechercher par mot-clé")
            print("  3. Filtrer par catégorie")
            print("  4. Filtrer par année")
            print("  5. Voir les détails d'un article")
            print("  6. Quitter")
            
            choice = input("\nChoix: ").strip()
            
            if choice == '1':
                limit = input("Nombre d'articles à afficher (défaut: 50): ").strip()
                limit = int(limit) if limit.isdigit() else 50
                articles = self.get_articles(limit=limit)
                self.display_table(articles)
                
            elif choice == '2':
                keyword = input("Mot-clé: ").strip()
                if keyword:
                    articles = self.get_articles(search_query=keyword)
                    self.display_table(articles)
                    
            elif choice == '3':
                print("\nCatégories disponibles: math.DG, math.SG, math-ph, math.AG, math.QA, math.RT")
                cat = input("Catégorie: ").strip()
                if cat:
                    articles = self.get_articles(category=cat)
                    self.display_table(articles)
                    
            elif choice == '4':
                year = input("Année (ex: 2024): ").strip()
                if year.isdigit():
                    articles = self.get_articles(year=int(year))
                    self.display_table(articles)
                    
            elif choice == '5':
                arxiv_id = input("arXiv ID (ex: 2511.16644v1): ").strip()
                if arxiv_id:
                    self.show_article_details(arxiv_id)
                    
            elif choice == '6':
                print("\n👋 Au revoir habibi!\n")
                break
            
            else:
                print("❌ Choix invalide")
    
    def show_article_details(self, arxiv_id):
        """Affiche les détails d'un article"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM articles WHERE arxiv_id = ?", (arxiv_id,))
        article = cursor.fetchone()
        conn.close()
        
        if not article:
            print(f"\n❌ Article {arxiv_id} non trouvé.\n")
            return
        
        print("\n" + "="*80)
        print("📄 DÉTAILS DE L'ARTICLE")
        print("="*80)
        print(f"\n📌 arXiv ID: {article[0]}")
        print(f"\n📄 Titre:\n   {article[1]}")
        print(f"\n✍️  Auteurs:\n   {article[2]}")
        print(f"\n🏷️  Catégorie: {article[4]}")
        print(f"\n📅 Publié: {article[5][:10]}")
        print(f"\n🔗 Lien: {article[7]}")
        print(f"\n📥 PDF: {article[8]}")
        print(f"\n📝 Abstract:\n{article[3]}")
        print("\n" + "="*80 + "\n")


def main():
    """Fonction principale"""
    viewer = ArxivTableViewer()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'all':
            # Afficher tous les articles
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            articles = viewer.get_articles(limit=limit)
            viewer.display_table(articles)
        
        elif cmd == 'search':
            # Rechercher
            if len(sys.argv) < 3:
                print("Usage: python3 arxiv_table.py search <mot-clé>")
                return
            keyword = sys.argv[2]
            articles = viewer.get_articles(search_query=keyword)
            viewer.display_table(articles)
        
        elif cmd == 'cat':
            # Par catégorie
            if len(sys.argv) < 3:
                print("Usage: python3 arxiv_table.py cat <catégorie>")
                return
            category = sys.argv[2]
            articles = viewer.get_articles(category=category)
            viewer.display_table(articles)
        
        elif cmd == 'year':
            # Par année
            if len(sys.argv) < 3:
                print("Usage: python3 arxiv_table.py year <année>")
                return
            year = int(sys.argv[2])
            articles = viewer.get_articles(year=year)
            viewer.display_table(articles)
        
        elif cmd == 'details':
            # Détails d'un article
            if len(sys.argv) < 3:
                print("Usage: python3 arxiv_table.py details <arxiv_id>")
                return
            arxiv_id = sys.argv[2]
            viewer.show_article_details(arxiv_id)
        
        elif cmd == 'menu':
            # Menu interactif
            viewer.interactive_menu()
        
        else:
            print_usage()
    
    else:
        # Par défaut, afficher le menu
        viewer.interactive_menu()


def print_usage():
    """Affiche l'aide"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                      arXiv COLLECTOR - Vue Tableau                         ║
╚════════════════════════════════════════════════════════════════════════════╝

UTILISATION:

    python3 arxiv_table.py [commande] [options]

COMMANDES:

    menu                    Menu interactif (défaut)
    all [limite]            Afficher tous les articles (défaut: 50)
    search <mot-clé>        Rechercher par mot-clé
    cat <catégorie>         Filtrer par catégorie
    year <année>            Filtrer par année
    details <arxiv_id>      Afficher les détails d'un article

EXEMPLES:

    # Menu interactif
    python3 arxiv_table.py
    python3 arxiv_table.py menu
    
    # Afficher les 100 derniers articles
    python3 arxiv_table.py all 100
    
    # Rechercher "Poisson"
    python3 arxiv_table.py search Poisson
    
    # Articles de math.SG
    python3 arxiv_table.py cat math.SG
    
    # Articles de 2024
    python3 arxiv_table.py year 2024
    
    # Détails d'un article
    python3 arxiv_table.py details 2511.16644v1

📝 Note: La base de données doit être créée avec arxiv_collector.py
    """)


if __name__ == "__main__":
    main()
