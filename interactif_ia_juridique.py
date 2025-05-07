from tkinter import ttk, messagebox
import webbrowser
import pyperclip
from ia_jurisite import IAJuridiqueWeb
import tkinter as tk

class InterfaceIAJuridique:
    def __init__(self, root):
        self.root = root
        self.root.title("🔎 Assistant Juridique - Commissaires de Justice")
        self.root.geometry("900x650")
        self.root.configure(bg="#f8f9fa")

        self.ia = IAJuridiqueWeb()
        self.resultats = []

        self.creer_menu()
        self.creer_widgets()

    def creer_menu(self):
        menu_bar = tk.Menu(self.root)
        fichier_menu = tk.Menu(menu_bar, tearoff=0)
        fichier_menu.add_command(label="Quitter", command=self.root.quit)
        menu_bar.add_cascade(label="Fichier", menu=fichier_menu)

        aide_menu = tk.Menu(menu_bar, tearoff=0)
        aide_menu.add_command(label="À propos", command=self.afficher_infos)
        menu_bar.add_cascade(label="Aide", menu=aide_menu)

        self.root.config(menu=menu_bar)

    def creer_widgets(self):
        # Titre
        tk.Label(self.root, text="Assistant Juridique pour Commissaires de Justice",
                 font=("Helvetica", 18, "bold"), bg="#f8f9fa", fg="#343a40").pack(pady=20)

        # Zone d'entrée
        cadre_recherche = tk.Frame(self.root, bg="#f8f9fa")
        cadre_recherche.pack(pady=5)

        self.entry = tk.Entry(cadre_recherche, font=("Arial", 14), width=60)
        self.entry.pack(side=tk.LEFT, padx=10)

        tk.Button(cadre_recherche, text="Rechercher", command=self.lancer_recherche,
                  font=("Arial", 12), bg="#007BFF", fg="white").pack(side=tk.LEFT)

        # Liste des résultats
        self.tree = ttk.Treeview(self.root, columns=("url"), show="headings", height=20)
        self.tree.heading("url", text="Résultats trouvés")
        self.tree.column("url", anchor="w")
        self.tree.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

        # Boutons d’action
        cadre_actions = tk.Frame(self.root, bg="#f8f9fa")
        cadre_actions.pack(pady=5)

        tk.Button(cadre_actions, text="📋 Copier l'URL", command=self.copier_url,
                  font=("Arial", 11), bg="#28a745", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(cadre_actions, text="🌐 Ouvrir dans le navigateur", command=self.ouvrir_url,
                  font=("Arial", 11), bg="#17a2b8", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(cadre_actions, text="🗑️ Effacer", command=self.effacer_resultats,
                  font=("Arial", 11), bg="#dc3545", fg="white").pack(side=tk.LEFT, padx=10)

        self.root.bind("<Return>", lambda event: self.lancer_recherche())

    def lancer_recherche(self):
        mot_cle = self.entry.get().strip()
        if not mot_cle:
            messagebox.showwarning("Champ vide", "Veuillez entrer un mot-clé.")
            return

        self.tree.delete(*self.tree.get_children())  # Efface la liste
        self.resultats = []

        try:
            liens = self.ia.recherche_google(mot_cle)
            if liens:
                for lien in liens:
                    url = lien.replace("🔍 ", "").strip()
                    self.resultats.append(url)
                    self.tree.insert("", tk.END, values=(url,))
            else:
                messagebox.showinfo("Aucun résultat", "Aucun lien pertinent trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def copier_url(self):
        selected = self.tree.focus()
        if selected:
            url = self.tree.item(selected)["values"][0]
            pyperclip.copy(url)
            messagebox.showinfo("Copié", "URL copiée dans le presse-papier.")
        else:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une URL à copier.")

    def ouvrir_url(self):
        selected = self.tree.focus()
        if selected:
            url = self.tree.item(selected)["values"][0]
            webbrowser.open(url)
        else:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une URL à ouvrir.")

    def effacer_resultats(self):
        self.entry.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.resultats = []

    def afficher_infos(self):
        messagebox.showinfo("À propos",
            "Assistant Juridique v2.0\n\nRecherche sur Legifrance, Service-Public, etc.\n"
            "Conçu pour aider les Commissaires de Justice.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceIAJuridique(root)
    root.mainloop()