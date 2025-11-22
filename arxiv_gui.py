#!/usr/bin/env python3
"""
arXiv Collector - Interface Graphique Professionnelle
Interface style LMA pour la collection d'articles arXiv
Par Yassine Ait Mohamed - Université de Sherbrooke
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import webbrowser
import subprocess
import os

class ArxivGUI:
    def __init__(self):
        self.db_path = "arxiv_collection.db"
        self.root = tk.Tk()
        self.root.title("📚 AVCP")
        self.root.geometry("1400x900")
        
        # ===== THÈME SOMBRE (Oxford/UdeS) =====
        self.bg_dark = "#1a1d1a"
        self.bg_darker = "#141614"
        self.bg_lighter = "#252a25"
        self.fg_light = "#e8ede8"
        self.fg_bright = "#ffffff"
        self.accent_blue = "#002147"      # Bleu Oxford foncé
        self.accent_green = "#00a650"     # Vert UdeS
        self.accent_orange = "#d4a017"    # Or
        self.accent_yellow = "#ffd700"    # Jaune doré
        self.accent_red = "#8B0000"       # Rouge Oxford
        self.accent_cyan = "#4a9b8e"      # Cyan verdâtre
        
        # ===== THÈME CLAIR (Clean & Professional) =====
        self.bg_light = "#f5f5dc"           # Beige clair
        self.bg_light_darker = "#ebe8d8"    # Beige plus foncé
        self.bg_light_lighter = "#faf8f0"   # Beige très clair
        self.fg_dark = "#2c3e50"
        self.text_light = "#2c3e50"
        self.accent_blue_light = "#3498db"
        self.accent_green_light = "#27ae60"
        self.accent_orange_light = "#e67e22"
        self.accent_yellow_light = "#f39c12"
        self.accent_red_light = "#dc3545"
        self.accent_cyan_light = "#16a085"
        
        self.mode_theme = "dark"
        self.root.configure(bg=self.bg_dark)
        
        # Filtres
        self.current_filter = "all"
        self.search_term = ""
        
        self.create_widgets()
        self.refresh_articles()
    
    def get_colors(self):
        """Retourner les couleurs selon le thème actuel"""
        if self.mode_theme == "dark":
            return {
                'bg': self.bg_dark,
                'bg_darker': self.bg_darker,
                'bg_lighter': self.bg_lighter,
                'fg': self.fg_light,
                'fg_bright': self.fg_bright,
                'blue': self.accent_blue,
                'green': self.accent_green,
                'orange': self.accent_orange,
                'yellow': self.accent_yellow,
                'red': self.accent_red,
                'cyan': self.accent_cyan,
                'search_bg': "#1a1a1a",
                'search_fg': "#ff4444",
                'button_bg': "#000000",
                'highlight_all': "#1a4d7a",
                'highlight_cat': "#1a3a52",
                'text': "#ffffff"
            }
        else:
            return {
                'bg': self.bg_light,
                'bg_darker': self.bg_light_darker,
                'bg_lighter': self.bg_light_lighter,
                'fg': self.fg_dark,
                'fg_bright': self.fg_dark,
                'blue': self.accent_blue_light,
                'green': self.accent_green_light,
                'orange': self.accent_orange_light,
                'yellow': self.accent_yellow_light,
                'red': self.accent_red_light,
                'cyan': self.accent_cyan_light,
                'search_bg': "#ffffff",
                'search_fg': "#d32f2f",
                'button_bg': "#ecf0f1",
                'highlight_all': "#d6eaf8",
                'highlight_cat': "#fef5e7",
                'text': "#002147"
            }
    
    def create_widgets(self):
        """Créer tous les widgets de l'interface"""
        c = self.get_colors()
        
        # ===== HEADER =====
        self.header_frame = tk.Frame(self.root, bg=c['bg_darker'], height=80)
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        self.header_label = tk.Label(
            self.header_frame,
            text="📚 ACP",
            font=("SF Pro Display", 24, "bold"),
            bg=c['bg_darker'],
            fg=c['fg_bright']
        )
        self.header_label.pack(pady=20)
        
        # ===== SEARCH BAR =====
        self.search_container = tk.Frame(self.root, bg=c['bg'], height=80)
        self.search_container.pack(fill=tk.X, padx=20, pady=(15, 10))
        self.search_container.pack_propagate(False)
        
        self.search_frame = tk.Frame(self.search_container, bg=c['bg'])
        self.search_frame.place(relx=0.5, rely=0.5, anchor="center", width=800)
        
        self.search_icon = tk.Label(
            self.search_frame,
            text="🔍",
            font=("SF Pro Display", 18),
            bg=c['bg'],
            fg=c['fg']
        )
        self.search_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = tk.Entry(
            self.search_frame,
            font=("SF Pro Display", 16),
            bg=c['search_bg'],
            fg=c['search_fg'],
            insertbackground=c['search_fg'],
            relief=tk.FLAT,
            bd=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        self.search_entry.bind('<Return>', lambda e: self.search_articles())
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search_change())
        
        # ===== FILTRES =====
        self.filter_frame = tk.Frame(self.root, bg=c['bg'], height=60)
        self.filter_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.filter_frame.pack_propagate(False)
        
        # Frame centré pour les boutons
        self.filter_buttons_frame = tk.Frame(self.filter_frame, bg=c['bg'])
        self.filter_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Boutons de filtre
        self.create_filter_button("Tous", "all", c)
        self.create_filter_button("math.DG", "math.DG", c)
        self.create_filter_button("math.SG", "math.SG", c)
        self.create_filter_button("math-ph", "math-ph", c)
        self.create_filter_button("math.AG", "math.AG", c)
        self.create_filter_button("math.QA", "math.QA", c)
        self.create_filter_button("math.RT", "math.RT", c)
        
        # ===== BOUTONS D'ACTION =====
        self.button_frame = tk.Frame(self.root, bg=c['bg'], height=50)
        self.button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.button_frame.pack_propagate(False)
        
        button_container = tk.Frame(self.button_frame, bg=c['bg'])
        button_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Refresh
        self.refresh_frame = self.create_action_button(
            button_container, "🔄 Refresh", c['button_bg'], c['red'],
            self.refresh_articles
        )
        
        # Update
        self.update_frame = self.create_action_button(
            button_container, "⬇️ Update", c['button_bg'], c['orange'],
            self.update_collection
        )
        
        # Stats
        self.stats_frame = self.create_action_button(
            button_container, "📊 Stats", c['button_bg'], c['blue'],
            self.show_stats
        )
        
        # Theme
        self.theme_frame = self.create_action_button(
            button_container, "🌓 Theme", c['button_bg'], c['cyan'],
            self.toggle_theme
        )
        
        # Export
        self.export_frame = self.create_action_button(
            button_container, "💾 Export", c['button_bg'], c['green'],
            self.export_list
        )
        
        # ===== TREEVIEW =====
        self.tree_container = tk.Frame(self.root, bg=c['bg'])
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Style pour le TreeView
        style = ttk.Style()
        style.configure("Treeview",
                       background=c['bg_lighter'],
                       foreground=c['text'],
                       fieldbackground=c['bg_lighter'],
                       borderwidth=0,
                       font=("SF Pro Display", 12),
                       rowheight=40)
        
        style.configure("Treeview.Heading",
                       background=c['bg_darker'],
                       foreground=c['blue'],
                       borderwidth=0,
                       font=("SF Pro Display", 13, "bold"))
        
        style.map('Treeview',
                 background=[('selected', c['blue'])])
        
        # Colonnes
        columns = ("Title", "Author", "year", "Category", "arXiv ID")
        self.tree = ttk.Treeview(
            self.tree_container,
            columns=columns,
            show="tree headings",
            selectmode="browse"
        )
        
        # Configuration des colonnes
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Title", width=500, anchor=tk.W)
        self.tree.column("Author", width=250, anchor=tk.W)
        self.tree.column("year", width=80, anchor=tk.CENTER)
        self.tree.column("Category", width=100, anchor=tk.CENTER)
        self.tree.column("arXiv ID", width=150, anchor=tk.CENTER)
        
        # En-têtes
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W if col in ["Titre", "Auteur"] else tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-clic pour ouvrir
        self.tree.bind('<Double-Button-1>', self.on_double_click)
        
        # Menu contextuel
        self.context_menu = tk.Menu(self.root, tearoff=0, 
                                    bg=c['bg_lighter'], fg=c['fg_bright'],
                                    activebackground=c['blue'],
                                    activeforeground=c['fg_bright'])
        self.context_menu.add_command(label="🔗 Ouvrir sur arXiv", command=self.open_arxiv)
        self.context_menu.add_command(label="📥 Télécharger PDF", command=self.download_pdf)
        self.context_menu.add_command(label="📋 Copier citation", command=self.copy_citation)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="ℹ️ Détails complets", command=self.show_details)
        
        self.tree.bind('<Button-2>', self.show_context_menu)  # Clic droit Mac
        self.tree.bind('<Button-3>', self.show_context_menu)  # Clic droit PC
        
        # ===== BARRE D'ACTION INFÉRIEURE =====
        self.action_frame = tk.Frame(self.root, bg=c['bg'], height=60)
        self.action_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.action_frame.pack_propagate(False)
        
        action_container = tk.Frame(self.action_frame, bg=c['bg'])
        action_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Boutons d'action
        self.open_arxiv_frame = self.create_large_button(
            action_container, "🔗 Open arXiv", c['button_bg'], c['orange'],
            self.open_arxiv
        )
        
        self.download_frame = self.create_large_button(
            action_container, "📥 Download PDF", c['button_bg'], c['green'],
            self.download_pdf
        )
        
        self.details_frame = self.create_large_button(
            action_container, "ℹ️ Details", c['button_bg'], c['cyan'],
            self.show_details
        )
    
    def create_filter_button(self, text, filter_value, c):
        """Créer un bouton de filtre"""
        is_active = self.current_filter == filter_value
        
        frame = tk.Frame(self.filter_buttons_frame, 
                        bg=c['highlight_all'] if is_active else c['button_bg'],
                        padx=15, pady=8)
        frame.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(
            frame,
            text=text,
            font=("SF Pro Display", 12, "bold" if is_active else "normal"),
            bg=c['highlight_all'] if is_active else c['button_bg'],
            fg=c['blue'] if is_active else "#aaaaaa",
            cursor="hand2"
        )
        label.pack()
        
        # Store reference
        setattr(self, f"filter_{filter_value}_frame", frame)
        setattr(self, f"filter_{filter_value}_label", label)
        
        label.bind('<Button-1>', lambda e: self.set_filter(filter_value))
    
    def create_action_button(self, parent, text, bg, fg, command):
        """Créer un bouton d'action"""
        frame = tk.Frame(parent, bg=bg, padx=12, pady=6)
        frame.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(
            frame,
            text=text,
            font=("SF Pro Display", 11),
            bg=bg,
            fg=fg,
            cursor="hand2"
        )
        label.pack()
        label.bind('<Button-1>', lambda e: command())
        
        return frame
    
    def create_large_button(self, parent, text, bg, fg, command):
        """Créer un grand bouton d'action"""
        frame = tk.Frame(parent, bg=bg, padx=20, pady=10)
        frame.pack(side=tk.LEFT, padx=10)
        
        label = tk.Label(
            frame,
            text=text,
            font=("SF Pro Display", 13, "bold"),
            bg=bg,
            fg=fg,
            cursor="hand2"
        )
        label.pack()
        label.bind('<Button-1>', lambda e: command())
        
        return frame
    
    def set_filter(self, filter_value):
        """Changer le filtre actif"""
        self.current_filter = filter_value
        self.update_filter_buttons()
        self.refresh_articles()
    
    def update_filter_buttons(self):
        """Mettre à jour l'apparence des boutons de filtre"""
        c = self.get_colors()
        filters = ["all", "math.DG", "math.SG", "math-ph", "math.AG", "math.QA", "math.RT"]
        
        for f in filters:
            frame = getattr(self, f"filter_{f}_frame")
            label = getattr(self, f"filter_{f}_label")
            
            is_active = self.current_filter == f
            frame.configure(bg=c['highlight_all'] if is_active else c['button_bg'])
            label.configure(
                bg=c['highlight_all'] if is_active else c['button_bg'],
                fg=c['blue'] if is_active else "#aaaaaa",
                font=("SF Pro Display", 12, "bold" if is_active else "normal")
            )
    
    def get_articles(self):
        """Récupérer les articles de la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT arxiv_id, title, authors, category, published, link, pdf_link FROM articles WHERE 1=1"
        params = []
        
        if self.search_term:
            query += " AND (title LIKE ? OR authors LIKE ? OR abstract LIKE ?)"
            search = f"%{self.search_term}%"
            params.extend([search, search, search])
        
        if self.current_filter != "all":
            query += " AND category = ?"
            params.append(self.current_filter)
        
        query += " ORDER BY published DESC LIMIT 200"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def refresh_articles(self):
        """Rafraîchir la liste des articles"""
        # Vider le TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Charger les articles
        articles = self.get_articles()
        
        for article in articles:
            arxiv_id, titre, auteurs, categorie, published, link, pdf_link = article
            
            # Premier auteur
            first_author = auteurs.split(";")[0].strip() if auteurs else "Unknown"
            if ";" in auteurs:
                first_author += " et al."
            
            # Année
            annee = published[:4] if published else "????"
            
            # Tronquer le titre
            titre_court = titre[:80] + "..." if len(titre) > 80 else titre
            
            self.tree.insert("", tk.END, values=(titre_court, first_author, annee, categorie, arxiv_id),
                           tags=(arxiv_id, link, pdf_link))
    
    def on_search_change(self):
        """Recherche en temps réel"""
        self.search_term = self.search_entry.get()
        if len(self.search_term) >= 3 or self.search_term == "":
            self.refresh_articles()
    
    def search_articles(self):
        """Rechercher des articles"""
        self.search_term = self.search_entry.get()
        self.refresh_articles()
    
    def toggle_theme(self):
        """Basculer entre mode sombre et clair"""
        self.mode_theme = "light" if self.mode_theme == "dark" else "dark"
        self.update_theme()
    
    def update_theme(self):
        """Mettre à jour le thème de l'interface"""
        c = self.get_colors()
        
        # Root
        self.root.configure(bg=c['bg'])
        
        # Header
        self.header_frame.configure(bg=c['bg_darker'])
        self.header_label.configure(bg=c['bg_darker'], fg=c['fg_bright'])
        
        # Recherche
        self.search_container.configure(bg=c['bg'])
        self.search_frame.configure(bg=c['bg'])
        self.search_icon.configure(bg=c['bg'], fg=c['fg'])
        self.search_entry.configure(bg=c['search_bg'], fg=c['search_fg'],
                                   insertbackground=c['search_fg'])
        
        # Filtres
        self.filter_frame.configure(bg=c['bg'])
        self.filter_buttons_frame.configure(bg=c['bg'])
        self.update_filter_buttons()
        
        # Boutons d'action
        self.button_frame.configure(bg=c['bg'])
        
        # TreeView
        self.tree_container.configure(bg=c['bg'])
        style = ttk.Style()
        style.configure("Treeview",
                       background=c['bg_lighter'],
                       foreground=c['text'],
                       fieldbackground=c['bg_lighter'])
        
        style.configure("Treeview.Heading",
                       background=c['bg_darker'],
                       foreground=c['blue'])
        
        style.map('Treeview',
                 background=[('selected', c['blue'])])
        
        # Menu contextuel
        self.context_menu.configure(bg=c['bg_lighter'], fg=c['fg_bright'],
                                   activebackground=c['blue'])
        
        # Action frame
        self.action_frame.configure(bg=c['bg'])
    
    def on_double_click(self, event):
        """Ouvrir l'article au double-clic"""
        self.open_arxiv()
    
    def show_context_menu(self, event):
        """Afficher le menu contextuel"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def open_arxiv(self):
        """Ouvrir l'article sur arXiv"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un article")
            return
        
        item = self.tree.item(selection[0])
        link = item["tags"][1]
        webbrowser.open(link)
    
    def download_pdf(self):
        """Télécharger le PDF"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un article")
            return
        
        item = self.tree.item(selection[0])
        pdf_link = item["tags"][2]
        webbrowser.open(pdf_link)
    
    def copy_citation(self):
        """Copier la citation arXiv"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un article")
            return
        
        item = self.tree.item(selection[0])
        arxiv_id = item["tags"][0]
        
        # Copier dans le presse-papier
        self.root.clipboard_clear()
        self.root.clipboard_append(arxiv_id)
        messagebox.showinfo("Succès", f"Citation copiée: {arxiv_id}")
    
    def show_details(self):
        """Afficher les détails complets de l'article"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un article")
            return
        
        item = self.tree.item(selection[0])
        arxiv_id = item["tags"][0]
        
        # Récupérer les détails complets
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE arxiv_id = ?", (arxiv_id,))
        article = cursor.fetchone()
        conn.close()
        
        if article:
            details = f"""📄 DÉTAILS DE L'ARTICLE

📌 arXiv ID: {article[0]}

📄 Titre:
{article[1]}

✍️ Auteurs:
{article[2]}

🏷️ Catégorie: {article[4]}

📅 Publié: {article[5][:10]}
📅 Mis à jour: {article[6][:10]}

🔗 Lien: {article[7]}
📥 PDF: {article[8]}

📝 Abstract:
{article[3]}
"""
            
            # Créer une fenêtre de détails
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Détails - {arxiv_id}")
            details_window.geometry("800x600")
            c = self.get_colors()
            details_window.configure(bg=c['bg'])
            
            text_widget = tk.Text(details_window, wrap=tk.WORD,
                                 bg=c['bg_lighter'], fg=c['text'],
                                 font=("SF Pro Display", 12),
                                 padx=20, pady=20)
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert("1.0", details)
            text_widget.configure(state="disabled")
    
    def update_collection(self):
        """Lancer la mise à jour de la collection"""
        response = messagebox.askyesno(
            "Mise à jour",
            "Lancer la mise à jour de la collection?\n\n"
            "Cela va collecter les articles des 2 derniers jours."
        )
        
        if response:
            # Lancer arxiv_collector.py en arrière-plan
            try:
                subprocess.Popen(["python3", "arxiv_collector.py", "update", "2"])
                messagebox.showinfo("Info", "Mise à jour lancée en arrière-plan!\n\nActualisez dans quelques minutes.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer la mise à jour:\n{e}")
    
    def show_stats(self):
        """Afficher les statistiques"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total
        cursor.execute("SELECT COUNT(*) FROM articles")
        total = cursor.fetchone()[0]
        
        # Par catégorie
        cursor.execute("SELECT category, COUNT(*) FROM articles GROUP BY category ORDER BY COUNT(*) DESC")
        by_cat = cursor.fetchall()
        
        # Par année
        cursor.execute("SELECT strftime('%Y', published) as year, COUNT(*) FROM articles GROUP BY year ORDER BY year DESC LIMIT 5")
        by_year = cursor.fetchall()
        
        conn.close()
        
        stats_text = f"""📊 STATISTIQUES DE LA COLLECTION

📚 Total: {total} articles

📂 Par catégorie:
"""
        for cat, count in by_cat:
            stats_text += f"   {cat}: {count}\n"
        
        stats_text += "\n📅 Par année (5 dernières):\n"
        for year, count in by_year:
            stats_text += f"   {year}: {count}\n"
        
        messagebox.showinfo("Statistiques", stats_text)
    
    def export_list(self):
        """Exporter la liste actuelle"""
        articles = self.get_articles()
        
        if not articles:
            messagebox.showwarning("Attention", "Aucun article à exporter")
            return
        
        # Export en format texte simple
        export_text = "# arXiv Collection Export\n\n"
        
        for article in articles:
            arxiv_id, titre, auteurs, categorie, published, link, pdf_link = article
            export_text += f"## {titre}\n"
            export_text += f"- **Auteurs**: {auteurs}\n"
            export_text += f"- **Catégorie**: {categorie}\n"
            export_text += f"- **Date**: {published[:10]}\n"
            export_text += f"- **arXiv**: {arxiv_id}\n"
            export_text += f"- **Lien**: {link}\n"
            export_text += f"- **PDF**: {pdf_link}\n\n"
        
        # Sauvegarder
        filename = f"arxiv_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(export_text)
        
        messagebox.showinfo("Succès", f"Exporté dans:\n{filename}")
    
    def run(self):
        """Lancer l'interface"""
        self.root.mainloop()


def main():
    """Fonction principale"""
    app = ArxivGUI()
    app.run()


if __name__ == "__main__":
    main()
