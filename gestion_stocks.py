import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FICHIER_PRODUITS = "produits.json"
FICHIER_VENTES = "ventes.json"


def charger_fichier(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def sauvegarder_fichier(nom_fichier, donnees):
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, indent=4, ensure_ascii=False)


produits = charger_fichier(FICHIER_PRODUITS)
ventes = charger_fichier(FICHIER_VENTES)


def sauvegarder():
    sauvegarder_fichier(FICHIER_PRODUITS, produits)
    sauvegarder_fichier(FICHIER_VENTES, ventes)


def vider_champs():
    entree_nom.delete(0, tk.END)
    entree_ref.delete(0, tk.END)
    entree_qte.delete(0, tk.END)
    entree_prix.delete(0, tk.END)
    combo_categorie.set("")


def trouver_produit(reference):
    for produit in produits:
        if produit["reference"].lower() == reference.lower():
            return produit
    return None

#add
def ajouter_produit():
   
    nom = entree_nom.get().strip()
    reference = entree_ref.get().strip()
    quantite = entree_qte.get().strip()
    prix = entree_prix.get().strip()
    categorie = combo_categorie.get().strip()

    if nom == "" or reference == "" or quantite == "" or prix == "" or categorie == "":
        messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
        return

    if trouver_produit(reference) is not None:
        messagebox.showerror("Erreur", "Cette référence existe déjà.")
        return

    try:
        quantite = int(quantite)
        prix = float(prix)

        if quantite < 0 or prix < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Quantité ou prix incorrect.")
        return

    produit = {
        "nom": nom,
        "reference": reference,
        "quantite": quantite,
        "prix": prix,
        "categorie": categorie
    }

    produits.append(produit)
    sauvegarder()
    afficher_produits()
    vider_champs()
    messagebox.showinfo("Succès", "Produit ajouté.")


def afficher_produits(liste=None):
    for ligne in tableau.get_children():
        tableau.delete(ligne)

    if liste is None:
        liste = produits

    for produit in liste:
        tableau.insert(
            "",
            tk.END,
            values=(
                produit["nom"],
                produit["reference"],
                produit["quantite"],
                f'{produit["prix"]:.2f}',
                produit["categorie"]
            )
        )


def remplir_champs(event=None):
    selection = tableau.selection()

    if not selection:
        return

    valeurs = tableau.item(selection[0], "values")

    vider_champs()
    entree_nom.insert(0, valeurs[0])
    entree_ref.insert(0, valeurs[1])
    entree_qte.insert(0, valeurs[2])
    entree_prix.insert(0, valeurs[3])
    combo_categorie.set(valeurs[4])


def modifier_produit():
    reference = entree_ref.get().strip()
    produit = trouver_produit(reference)

    if produit is None:
        messagebox.showerror("Erreur", "Produit non trouvé.")
        return

    try:
        quantite = int(entree_qte.get())
        prix = float(entree_prix.get())

        if quantite < 0 or prix < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Quantité ou prix incorrect.")
        return

    produit["nom"] = entree_nom.get().strip()
    produit["quantite"] = quantite
    produit["prix"] = prix
    produit["categorie"] = combo_categorie.get().strip()

    sauvegarder()
    afficher_produits()
    messagebox.showinfo("Succès", "Produit modifié.")


def supprimer_produit():
    reference = entree_ref.get().strip()
    produit = trouver_produit(reference)

    if produit is None:
        messagebox.showerror("Erreur", "Produit non trouvé.")
        return

    confirmation = messagebox.askyesno(
        "Confirmation",
        "Voulez-vous vraiment supprimer ce produit ?"
    )

    if confirmation:
        produits.remove(produit)
        sauvegarder()
        afficher_produits()
        vider_champs()


def rechercher():
    texte = entree_recherche.get().strip().lower()

    if texte == "":
        afficher_produits()
        return

    resultat = []

    for produit in produits:
        if texte in produit["nom"].lower() or texte in produit["reference"].lower():
            resultat.append(produit)

    afficher_produits(resultat)


def trier_par_categorie():
    liste = sorted(produits, key=lambda p: p["categorie"].lower())
    afficher_produits(liste)


def trier_par_quantite():
    liste = sorted(produits, key=lambda p: p["quantite"])
    afficher_produits(liste)


def fenetre_vente():
    fenetre = tk.Toplevel(root)
    fenetre.title("Enregistrer une vente")
    fenetre.geometry("360x260")
    fenetre.resizable(False, False)

    tk.Label(fenetre, text="Référence du produit").pack(pady=(20, 5))
    ref_vente = tk.Entry(fenetre, width=30)
    ref_vente.pack()

    tk.Label(fenetre, text="Quantité vendue").pack(pady=(12, 5))
    qte_vente = tk.Entry(fenetre, width=30)
    qte_vente.pack()

    tk.Label(fenetre, text="Date (JJ/MM/AAAA)").pack(pady=(12, 5))
    date_vente = tk.Entry(fenetre, width=30)
    date_vente.insert(0, datetime.now().strftime("%d/%m/%Y"))
    date_vente.pack()

    def valider_vente():
        reference = ref_vente.get().strip()
        produit = trouver_produit(reference)

        if produit is None:
            messagebox.showerror("Erreur", "Produit non trouvé.", parent=fenetre)
            return

        try:
            quantite = int(qte_vente.get())

            if quantite <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Quantité incorrecte.", parent=fenetre)
            return

        if quantite > produit["quantite"]:
            messagebox.showerror(
                "Erreur",
                "Stock insuffisant pour cette vente.",
                parent=fenetre
            )
            return

        date = date_vente.get().strip()

        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Date incorrecte. Exemple : 15/05/2025",
                parent=fenetre
            )
            return

        total = quantite * produit["prix"]

        vente = {
            "reference": produit["reference"],
            "nom": produit["nom"],
            "categorie": produit["categorie"],
            "quantite": quantite,
            "prix_unitaire": produit["prix"],
            "total": total,
            "date": date
        }

        ventes.append(vente)
        produit["quantite"] -= quantite
        sauvegarder()
        afficher_produits()

        messagebox.showinfo(
            "Vente enregistrée",
            f"Vente enregistrée.\nTotal : {total:.2f} €",
            parent=fenetre
        )
        fenetre.destroy()

    tk.Button(
        fenetre,
        text="Valider la vente",
        command=valider_vente,
        width=20
    ).pack(pady=20)


def fenetre_rapports():
    fenetre = tk.Toplevel(root)
    fenetre.title("Rapports et statistiques")
    fenetre.geometry("600x430")

    zone = tk.Text(fenetre, wrap=tk.WORD, font=("Arial", 11))
    zone.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    if len(produits) == 0:
        zone.insert(tk.END, "Aucun produit enregistré.\n")
    else:
        plus_stock = max(produits, key=lambda p: p["quantite"])
        moins_stock = min(produits, key=lambda p: p["quantite"])

        zone.insert(tk.END, "RAPPORT DU STOCK\n")
        zone.insert(tk.END, "-" * 45 + "\n")
        zone.insert(
            tk.END,
            f'Produit avec le plus de stock : {plus_stock["nom"]} '
            f'({plus_stock["quantite"]})\n'
        )
        zone.insert(
            tk.END,
            f'Produit avec le moins de stock : {moins_stock["nom"]} '
            f'({moins_stock["quantite"]})\n\n'
        )

    if len(ventes) == 0:
        zone.insert(tk.END, "Aucune vente enregistrée.\n")
    else:
        total_ca = 0
        quantites_vendues = {}
        ca_categories = {}

        for vente in ventes:
            total_ca += vente["total"]

            nom = vente["nom"]
            quantites_vendues[nom] = quantites_vendues.get(nom, 0) + vente["quantite"]

            categorie = vente["categorie"]
            ca_categories[categorie] = ca_categories.get(categorie, 0) + vente["total"]

        produit_plus_vendu = max(quantites_vendues, key=quantites_vendues.get)

        zone.insert(tk.END, "\nRAPPORT DES VENTES\n")
        zone.insert(tk.END, "-" * 45 + "\n")
        zone.insert(
            tk.END,
            f"Produit le plus vendu : {produit_plus_vendu} "
            f"({quantites_vendues[produit_plus_vendu]} unités)\n"
        )
        zone.insert(tk.END, f"Chiffre d'affaires total : {total_ca:.2f} €\n\n")

        zone.insert(tk.END, "Chiffre d'affaires par catégorie :\n")

        for categorie, montant in ca_categories.items():
            zone.insert(tk.END, f"- {categorie} : {montant:.2f} €\n")

    zone.config(state=tk.DISABLED)


def stock_faible():
    faibles = [p for p in produits if p["quantite"] <= 5]

    if not faibles:
        messagebox.showinfo("Stock faible", "Aucun produit avec un stock faible.")
        return

    texte = "Produits avec 5 unités ou moins :\n\n"

    for produit in faibles:
        texte += f'- {produit["nom"]} : {produit["quantite"]} unité(s)\n'

    messagebox.showwarning("Alerte stock faible", texte)


root = tk.Tk()
root.title("Gestion des stocks")
root.geometry("900x610")
root.resizable(False, False)

titre = tk.Label(
    root,
    text="Gestion des stocks",
    font=("Arial", 18, "bold")
)
titre.pack(pady=12)
 #joker was here

cadre_formulaire = tk.LabelFrame(root, text="Produit", padx=12, pady=10)
cadre_formulaire.pack(fill=tk.X, padx=20)

tk.Label(cadre_formulaire, text="Nom").grid(row=0, column=0, sticky="w", pady=4)
entree_nom = tk.Entry(cadre_formulaire, width=25)
entree_nom.grid(row=0, column=1, padx=8)

tk.Label(cadre_formulaire, text="Référence").grid(row=0, column=2, sticky="w", pady=4)
entree_ref = tk.Entry(cadre_formulaire, width=20)
entree_ref.grid(row=0, column=3, padx=8)

tk.Label(cadre_formulaire, text="Quantité").grid(row=1, column=0, sticky="w", pady=4)
entree_qte = tk.Entry(cadre_formulaire, width=25)
entree_qte.grid(row=1, column=1, padx=8)

tk.Label(cadre_formulaire, text="Prix unitaire").grid(row=1, column=2, sticky="w", pady=4)
entree_prix = tk.Entry(cadre_formulaire, width=20)
entree_prix.grid(row=1, column=3, padx=8)

tk.Label(cadre_formulaire, text="Catégorie").grid(row=2, column=0, sticky="w", pady=4)

combo_categorie = ttk.Combobox(
    cadre_formulaire,
    values=[
        "Alimentaire",
        "Électronique",
        "Informatique",
        "Vêtements",
        "Maison",
        "Autre"
    ],
    width=22,
    state="readonly"
)
combo_categorie.grid(row=2, column=1, padx=8)

cadre_boutons = tk.Frame(root)
cadre_boutons.pack(pady=10)

tk.Button(cadre_boutons, text="Ajouter", width=12, command=ajouter_produit).grid(row=0, column=0, padx=4)
tk.Button(cadre_boutons, text="Modifier", width=12, command=modifier_produit).grid(row=0, column=1, padx=4)
tk.Button(cadre_boutons, text="Supprimer", width=12, command=supprimer_produit).grid(row=0, column=2, padx=4)
tk.Button(cadre_boutons, text="Vider", width=12, command=vider_champs).grid(row=0, column=3, padx=4)
tk.Button(cadre_boutons, text="Vente", width=12, command=fenetre_vente).grid(row=0, column=4, padx=4)

cadre_recherche = tk.Frame(root)
cadre_recherche.pack(fill=tk.X, padx=20, pady=5)

tk.Label(cadre_recherche, text="Recherche :").pack(side=tk.LEFT)

entree_recherche = tk.Entry(cadre_recherche, width=30)
entree_recherche.pack(side=tk.LEFT, padx=5)

tk.Button(cadre_recherche, text="Rechercher", command=rechercher).pack(side=tk.LEFT, padx=3)
tk.Button(cadre_recherche, text="Tout afficher", command=afficher_produits).pack(side=tk.LEFT, padx=3)
tk.Button(cadre_recherche, text="Trier catégorie", command=trier_par_categorie).pack(side=tk.LEFT, padx=3)
tk.Button(cadre_recherche, text="Trier quantité", command=trier_par_quantite).pack(side=tk.LEFT, padx=3)

colonnes = ("nom", "reference", "quantite", "prix", "categorie")

tableau = ttk.Treeview(root, columns=colonnes, show="headings", height=13)

tableau.heading("nom", text="Nom")
tableau.heading("reference", text="Référence")
tableau.heading("quantite", text="Quantité")
tableau.heading("prix", text="Prix (€)")
tableau.heading("categorie", text="Catégorie")

tableau.column("nom", width=180)
tableau.column("reference", width=130)
tableau.column("quantite", width=90, anchor="center")
tableau.column("prix", width=100, anchor="center")
tableau.column("categorie", width=150)

tableau.pack(fill=tk.X, padx=20, pady=10)
tableau.bind("<<TreeviewSelect>>", remplir_champs)

cadre_bas = tk.Frame(root)
cadre_bas.pack(pady=5)

tk.Button(
    cadre_bas,
    text="Rapports / statistiques",
    width=22,
    command=fenetre_rapports
).grid(row=0, column=0, padx=8)

tk.Button(
    cadre_bas,
    text="Stock faible",
    width=18,
    command=stock_faible
).grid(row=0, column=1, padx=8)

tk.Button(
    cadre_bas,
    text="Quitter",
    width=12,
    command=root.destroy
).grid(row=0, column=2, padx=8)

afficher_produits()

root.mainloop()
