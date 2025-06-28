# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:08:09 2025

@author: Stéphane Pasquet
@url : mathweb.fr
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import platform

class InputPanel:
    def __init__(self, parent, project_path, main_window, params=None):
        self.frame = tk.Frame(parent, bg="#f5f5f5", padx=20, pady=20)
        self.project_path = project_path
        self.params = params or {}
        self.main_window = main_window
        self.fields = {}


        title_frame = tk.Label(self.frame, text="Paramètres du devoir", font=("Arial", 14, "bold"), bg="#f5f5f5")
        title_frame.pack(pady=(0, 20))
        
        #--- Créer un cadre 2 colonnes pour les champs texte ---
        self.field_frame = tk.Frame(self.frame)
        self.field_frame.pack(pady=10, anchor="w")

        self.add_field("Titre du devoir", "title")
        self.add_field("Nom de la classe", "class_name")
        self.add_field("Date (optionnelle)", "date")
        self.add_field("Durée du devoir (ex : 1h30)", "duration")
        
        #--- Frame consigne + préambule
        self.preamble_frame = tk.Frame(self.frame, bg="#f5f5f5")
        self.preamble_frame.pack(pady=(0, 10), anchor='w')

        #--- Consigne du devoir ---
        tk.Label(self.preamble_frame, text="Consigne du devoir :").grid(row=0, column=1, padx=(20, 0), sticky="w")
        self.consigne = tk.Text(self.preamble_frame, height=5, width=70, wrap=tk.WORD)
        self.consigne.grid(row=1, column=1, padx=(20, 0), sticky='w')
        
        #--- Préambule ---
        tk.Label(self.preamble_frame, text="Préambule LaTeX complémentaire :").grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.preamble = tk.Text(self.preamble_frame, height=5, width=70, wrap=tk.WORD)
        self.preamble.grid(row=1, column=0, padx=(0, 20), sticky='w')

        if "consigne" in self.params:
            self.consigne.insert("1.0", params["consigne"])
            
        
        if "preamble" in self.params:
            self.preamble.insert("1.0", params["preamble"])

        

        #--- colonnes pour les selectors ---
        self.selectors_frame = tk.Frame(self.frame, bg="#f5f5f5")
        self.selectors_frame.pack(pady=10, anchor="w")
        
        self.add_title_style_selector(self.selectors_frame, 0)
        self.add_question_style_selector(self.selectors_frame, 1)
        self.add_numberpage_style_selector(self.selectors_frame, 2)
        self.add_consigne_style_selector(self.selectors_frame, 3)
        self.add_cadre_style_selector(self.selectors_frame, 4)

        
        #---- Créer une question ----
        def add_new_question():
            def on_save(new_question):
                self.all_questions.append(new_question)
                self.save_questions()
                self.update_questions_listbox()
        
            self.open_question_window(on_save=on_save)
            
        
        # Mode corrigé
        self.mode_corrige_var = tk.BooleanVar()
        tk.Checkbutton(self.frame, text="Mode corrigé", variable=self.mode_corrige_var).pack(pady=(0, 10))

        
        
        # Frame contenant toute la ligne et qui s'étend horizontalement
        top_btn_frame = tk.Frame(self.frame, bg="#f5f5f5")
        top_btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Sous-frame centré pour les boutons (largeur ajustée au contenu)
        top_btn_subframe = tk.Frame(top_btn_frame, bg="#f5f5f5")
        top_btn_subframe.pack()
        
        btn_valider = tk.Button(top_btn_subframe, text="Enregistrer les paramètres", command=self.save_params, bg="blue", fg="white")
        btn_valider.pack(side=tk.LEFT, padx=5)
        
        btn_creer_question = tk.Button(top_btn_subframe, text="Créer une question", command=add_new_question, bg="green", fg="white")
        btn_creer_question.pack(side=tk.LEFT, padx=5)
        
        btn_visualiser = tk.Button(top_btn_subframe, text="Voir page 1", command=self.preview_latex, bg="red", fg="white")
        btn_visualiser.pack(side=tk.LEFT, padx=5)
        
        btn_visualiser = tk.Button(top_btn_subframe, text="Viewer externe", command=self.preview_extern, bg="purple", fg="white")
        btn_visualiser.pack(side=tk.LEFT, padx=5)
        
        # Trait horizontal
        separator = tk.Frame(self.frame, height=2, bd=1, relief=tk.SUNKEN, bg="gray")
        separator.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        # Texte explicatif sous le trait
        info_label = tk.Label(self.frame, text="Cliquez sur une question, puis...", bg="#f5f5f5", font=("Arial", 10, "italic"))
        info_label.pack(pady=(0, 5))
        
        # Deuxième ligne de boutons (déjà existant)
        mid_btn_frame = tk.Frame(self.frame, bg="#f5f5f5")
        mid_btn_frame.pack()
        
        mid_btn_subframe = tk.Frame(mid_btn_frame, bg="#f5f5f5")
        mid_btn_subframe.pack()
        
        self.modify_btn = tk.Button(mid_btn_subframe, text="Modifier", command=self.modify_question)
        self.modify_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(mid_btn_subframe, text="Supprimer", command=self.delete_question)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Liste des questions
        self.questions_listbox = tk.Listbox(self.frame, height=10)
        self.questions_listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 10))


        # Charger questions au lancement
        self.load_questions()

    #--- Ajouter un champs texte
    
    def add_field(self, label_text, key):
        row = len(self.fields) // 2
        column = (len(self.fields) % 2) * 2
    
        tk.Label(self.field_frame, text=label_text).grid(row=row, column=column, sticky="w", padx=5, pady=2)
        entry_var = tk.StringVar()
        entry = tk.Entry(self.field_frame, textvariable=entry_var, width=30)
        entry.grid(row=row, column=column + 1, padx=5, pady=2, sticky="w")
        
        # Pré-remplissage si les données existent
        if key in self.params:
            entry.insert(0, self.params[key])
    
        self.fields[key] = entry_var

    #--- Style du titre ---
    
    def add_title_style_selector(self, parent, col):
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.grid(row=0, column=col, padx=10, sticky="w")
        
        label = tk.Label(frame, text="Style de titre :", anchor="w", bg="#f5f5f5")
        label.pack(anchor="w")
        
        styles = self.get_title_styles()
        self.title_style_var = tk.StringVar(value="Classic")
        self.title_style_var.set(self.params.get("title_style", "Classic"))
        
        dropdown = tk.OptionMenu(frame, self.title_style_var, *styles)
        dropdown.config(width=20)
        dropdown.pack()

    
    def get_title_styles(self):
        styles = ["Classic"]  # Valeur par défaut
        style_dir = os.path.join(os.path.dirname(__file__), "..", "titlestyles")
        style_dir = os.path.abspath(style_dir)
    
        if os.path.isdir(style_dir):
            for fname in os.listdir(style_dir):
                if fname.endswith(".tex"):
                    styles.append(os.path.splitext(fname)[0])

        return styles
    
    def get_styles(self,name):
        if name != "consignestyles" and name != "boxstyles":
            styles = ["Classic"]
        else:
            styles = [""]  # Valeur par défaut
        style_dir = os.path.join(os.path.dirname(__file__), "..", name)
        style_dir = os.path.abspath(style_dir)
    
        if os.path.isdir(style_dir):
            for fname in os.listdir(style_dir):
                if fname.endswith(".tex"):
                    styles.append(os.path.splitext(fname)[0])

        return styles
    
        
    #--- Style de l'item des questions ---
    
    def add_question_style_selector(self, parent, col):
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.grid(row=0, column=col, padx=10, sticky="w")
        
        label = tk.Label(frame, text="Style de numérotation des questions :", anchor="w", bg="#f5f5f5")
        label.pack(anchor="w")
        
        styles = self.get_styles("questionstyles")
        self.question_style_var = tk.StringVar(value="Classic")
        self.question_style_var.set(self.params.get("question_style", "Classic"))
        
        dropdown = tk.OptionMenu(frame, self.question_style_var, *styles)
        dropdown.config(width=20)
        dropdown.pack()
    
    #--- Style du numéro de page ---
    
    def add_numberpage_style_selector(self, parent, col):
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.grid(row=0, column=col, padx=10, sticky="w")
    
        label = tk.Label(frame, text="Style de numérotation des pages :", anchor="w", bg="#f5f5f5")
        label.pack(anchor="w")
    
        styles = self.get_styles("numberpagestyles")                  
        self.numberpage_style_var = tk.StringVar(value="Classic")
        self.numberpage_style_var.set(self.params.get("numberpage_style", "Classic"))
    
        dropdown = tk.OptionMenu(frame, self.numberpage_style_var, *styles)
        dropdown.config(width=20)
        dropdown.pack()
 
    
    #--- Style de la consigne ---
    
    def add_consigne_style_selector(self, parent, col):
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.grid(row=0, column=col, padx=10, sticky="w")
    
        label = tk.Label(frame, text="Style de la consigne :", anchor="w", bg="#f5f5f5")
        label.pack(anchor="w")
    
        styles = self.get_styles("consignestyles")
        if "consigne_style" in self.params and self.params["consigne_style"]:
            self.consigne_style_var = tk.StringVar(value=self.params["consigne_style"])
        else:
            self.consigne_style_var = tk.StringVar(value="")
    
        dropdown = tk.OptionMenu(frame, self.consigne_style_var, *styles)
        dropdown.config(width=20)
        dropdown.pack()
        
    #--- Style du cadre ---
    
    def add_cadre_style_selector(self, parent, col):
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.grid(row=0, column=col, padx=10, sticky="w")
    
        label = tk.Label(frame, text="Style des cadres (pour réponses libres) :", anchor="w", bg="#f5f5f5")
        label.pack(anchor="w")
    
        styles = self.get_styles("boxstyles")
        if "cadre_style" in self.params and self.params["cadre_style"]:
            self.cadre_style_var = tk.StringVar(value=self.params["cadre_style"])
        else:
            self.cadre_style_var = tk.StringVar(value="")
    
        dropdown = tk.OptionMenu(frame, self.cadre_style_var, *styles)
        dropdown.config(width=20)
        dropdown.pack()


    def save_params(self, silent=False):
        data = self.get_params()
        file_path = os.path.join(self.project_path, "params.json")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if not silent:
                messagebox.showinfo("Succès", f"Paramètres enregistrés dans {file_path}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer les paramètres :\n{e}")
            
    def get_params(self):
        data = {}
        for key, entry in self.fields.items():
            data[key] = entry.get()
        data["title_style"] = self.title_style_var.get()
        data["question_style"] = self.question_style_var.get()
        data["numberpage_style"] = self.numberpage_style_var.get()
        data["preamble"] = self.preamble.get("1.0", tk.END).strip()
        data["consigne"] = self.consigne.get("1.0", tk.END).strip()
        data["consigne_style"] = self.consigne_style_var.get()
        data["cadre_style"] = self.cadre_style_var.get()
   
        return data


    
    #--- Méthode pour la demande d'une question ---

    def open_question_window(self, prefill=None, on_save=None):
        window = tk.Toplevel(self.frame)
        window.title("Nouvelle question")
        window.geometry("500x600")
        window.grab_set()
    
        # === Variables ===
        question_type_var = tk.StringVar(value="QCM")
        nb_prop_var = tk.StringVar()
        hauteur_var = tk.StringVar()
        lignes_var = tk.BooleanVar()
        colonnes_var = tk.StringVar(value="1")
        bonne_reponse_var = tk.StringVar()
        propositions = []
    
        # === Widgets ===
    
        tk.Label(window, text="Type de question :").pack()
        type_menu = tk.OptionMenu(window, question_type_var, "QCM", "Réponse libre")
        type_menu.pack(pady=(0, 10))
        
        tk.Label(window, text="Libellé de la question :").pack(pady=(10, 2))
        
        # Champ Text multilignes
        libelle_entry = tk.Text(window, height=10, width=60, wrap=tk.WORD, bd=2, relief=tk.SOLID)#tk.Text(window, height=5, width=60, wrap=tk.WORD)
        libelle_entry.pack(pady=(0, 10))
    
        # Frame dynamique
        dynamic_frame = tk.Frame(window)
        dynamic_frame.pack(fill=tk.BOTH, expand=True)
    
        def update_form(*args):
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
    
            if question_type_var.get() == "QCM":
                tk.Label(dynamic_frame, text="Nombre de colonnes :").pack()
                colonnes_entry = tk.Entry(dynamic_frame, textvariable=colonnes_var)
                colonnes_entry.pack(pady=(0, 5))

                tk.Label(dynamic_frame, text="Nombre de propositions :").pack()
                nb_entry = tk.Entry(dynamic_frame, textvariable=nb_prop_var)
                nb_entry.pack(pady=(0, 5))
    
                def generate_propositions():
                    for widget in prop_frame.winfo_children():
                        widget.destroy()
                    propositions.clear()
    
                    try:
                        n = int(nb_prop_var.get())
                        if n <= 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif.")
                        return
    
                    for i in range(n):
                        tk.Label(prop_frame, text=f"Proposition {i+1} :").pack(anchor="w")
                        texte_var = tk.StringVar()
                        correct_var = tk.BooleanVar()
                        tk.Entry(prop_frame, textvariable=texte_var, width=50).pack()
                        tk.Checkbutton(prop_frame, text="Bonne réponse", variable=correct_var).pack(anchor="w")
                        propositions.append((texte_var, correct_var))
    
                    if prefill and "propositions" in prefill:
                        for i, (texte_var, correct_var) in enumerate(propositions):
                            if i < len(prefill["propositions"]):
                                texte_var.set(prefill["propositions"][i]["texte"])
                                correct_var.set(prefill["propositions"][i]["correct"])
    
                tk.Button(dynamic_frame, text="Générer les propositions", command=generate_propositions).pack(pady=5)
                prop_frame = tk.Frame(dynamic_frame)
                prop_frame.pack()
    
                if prefill and prefill.get("type") == "QCM":
                    nb_prop_var.set(str(len(prefill.get("propositions", []))))
                    colonnes_var.set(str(prefill.get("colonnes", "1")))
                    generate_propositions()
    
            elif question_type_var.get() == "Réponse libre":
                tk.Label(dynamic_frame, text="Bonne réponse attendue :").pack(anchor="w", pady=(10, 0))
                bonne_reponse_entry = tk.Entry(dynamic_frame, textvariable=bonne_reponse_var, width=60)
                bonne_reponse_entry.pack(pady=(0, 10))
                
                tk.Label(dynamic_frame, text="Hauteur du cadre (en cm) :").pack(anchor="w")
                hauteur_entry = tk.Entry(dynamic_frame, textvariable=hauteur_var, width=10)
                hauteur_entry.pack(pady=(0, 10))
                
                ligne_check = tk.Checkbutton(dynamic_frame, text="Ajouter des lignes pointillées", variable=lignes_var)
                ligne_check.pack(anchor="w")


                # Préremplissage des champs spécifiques
                if prefill and prefill.get("type") == "Réponse libre":
                    hauteur_var.set(str(prefill.get("hauteur", "5")))
                    bonne_reponse_var.set(prefill.get("bonne_reponse", ""))
                    hauteur_var.set(str(prefill.get("hauteur", "5")))
                    lignes_var.set(prefill.get("lignes", False))

    
    
        question_type_var.trace_add("write", update_form)
    
        # Pré-remplissage
        if prefill:
            libelle_entry.insert("1.0", prefill.get("libelle", ""))
            question_type_var.set(prefill.get("type", "QCM"))


    
        update_form()
    
        def valider():
            libelle = libelle_entry.get("1.0", tk.END).strip()
            if not libelle:
                messagebox.showerror("Erreur", "Le libellé de la question ne peut pas être vide.")
                return
    
            data = {
                "type": question_type_var.get(),
                "libelle": libelle,
            }
    
            if data["type"] == "QCM":
                props = []
                for texte_var, correct_var in propositions:
                    texte = texte_var.get().strip()
                    if not texte:
                        messagebox.showerror("Erreur", "Toutes les propositions doivent être remplies.")
                        return
                    props.append({"texte": texte, "correct": correct_var.get()})
    
                if not any(p["correct"] for p in props):
                    messagebox.showerror("Erreur", "Au moins une proposition doit être correcte.")
                    return
                
                try:
                    colonnes = int(colonnes_var.get())
                    if colonnes <= 0:
                        raise ValueError
                    data["colonnes"] = colonnes
                except ValueError:
                    messagebox.showerror("Erreur", "Le nombre de colonnes doit être un entier positif.")
                    return

                data["propositions"] = props
    
            elif data["type"] == "Réponse libre":
                try:
                    hauteur = float(hauteur_var.get())
                    if hauteur <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Erreur", "La hauteur du cadre doit être un nombre positif.")
                    return
                
                data["hauteur"] = hauteur
                data["lignes"] = lignes_var.get()
                data["bonne_reponse"] = bonne_reponse_var.get().strip()


    
            if on_save:
                on_save(data)
    
            window.destroy()
    
        tk.Button(window, text="Valider", command=valider, bg="blue", fg="white").pack(pady=10)


    #=== Fin de l'ajout d'une question
    
    #--- Liste des questions
    
    def load_questions(self):
        """Charge la liste des questions depuis questions.json"""
        self.questions_file = os.path.join(self.project_path, "questions.json")
        if os.path.exists(self.questions_file):
            with open(self.questions_file, "r", encoding="utf-8") as f:
                try:
                    self.all_questions = json.load(f)
                except json.JSONDecodeError:
                    self.all_questions = []
        else:
            self.all_questions = []
    
        self.update_questions_listbox()
    
    def update_questions_listbox(self):
        """Met à jour l'affichage de la liste des questions"""
        self.questions_listbox.delete(0, tk.END)
        for i, q in enumerate(self.all_questions):
            # Affiche type + début du libellé (limité à 50 caractères)
            label = f"{i+1}. [{q['type']}] {q['libelle'][:50]}"
            self.questions_listbox.insert(tk.END, label)
    
    def modify_question(self):
        """Ouvre la fenêtre question avec les données sélectionnées"""
        selected = self.questions_listbox.curselection()
        if not selected:
            messagebox.showwarning("Sélectionner une question", "Veuillez sélectionner une question à modifier.")
            return
        index = selected[0]
        question = self.all_questions[index]
    
        def save_modifications(updated_data):
            self.all_questions[index] = updated_data
            self.save_questions()
            self.update_questions_listbox()
    
        self.open_question_window(prefill=question, on_save=save_modifications)
    
    def delete_question(self):
        """Supprime la question sélectionnée"""
        selected = self.questions_listbox.curselection()
        if not selected:
            messagebox.showwarning("Sélectionner une question", "Veuillez sélectionner une question à supprimer.")
            return
        index = selected[0]
        if messagebox.askyesno("Confirmer suppression", "Voulez-vous vraiment supprimer cette question ?"):
            del self.all_questions[index]
            self.save_questions()
            self.update_questions_listbox()
    
    def save_questions(self):
        """Sauvegarde la liste des questions dans le fichier JSON"""
        with open(self.questions_file, "w", encoding="utf-8") as f:
            json.dump(self.all_questions, f, indent=2, ensure_ascii=False)
    
        
    # --- LaTeX ---
        
    def preview_latex(self):
        project_path = self.project_path
        if self.mode_corrige_var.get():
            tex_file = os.path.join(project_path, "preview_correction.tex")
            pdf_file = os.path.join(project_path, "preview_correction.pdf")
   
        else:
            tex_file = os.path.join(project_path, "preview.tex")
            pdf_file = os.path.join(project_path, "preview.pdf")
        
        latex_code = self.build_latex_from_params(self.get_params())
        
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_code)
        
        try:
            subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", tex_file],
                    cwd=project_path,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur LaTeX", f"Erreur lors de la compilation :\n{e}")
            return
        
        # Mise à jour de l'aperçu PDF dans le panneau PreviewPanel
        self.main_window.preview_panel.update_preview(pdf_file)

    
    def build_latex_from_params(self, params):
        lines = [
            r"\documentclass{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage[french]{babel}",
            r"\usepackage[bmargin=1.5cm, tmargin=1cm,hmargin=10mm]{geometry}",
            r"\usepackage{multicol}",
            r"\usepackage{amssymb}",
            r"\usepackage{tikz}",
            ""
        ]
        
        # Inclure un style personnalisé des cadres si sélectionné
        if params.get("cadre_style") and params["cadre_style"] != "":
            style_file_path = os.path.join("boxstyles", params["cadre_style"] + ".tex")
            try:
                with open(style_file_path, "r", encoding="utf-8") as f:
                    style_content = f.read()
                lines.append(f"% --- Début du style des cadres {params['cadre_style']} ---")
                lines.append(style_content)
                lines.append(f"% --- Fin du style des cadres {params['cadre_style']} ---\n")
            except FileNotFoundError:
                lines.append(f"% Style {params['cadre_style']} introuvable, on continue sans style.\n")
        
        if self.mode_corrige_var.get():
            lines.append(r"\newsavebox{\tmpcasebox}")
            lines.append(r"\sbox{\tmpcasebox}{$\square$}")
            lines.append(r"\newlength\tmpwidth")
            lines.append(r"\newcommand{\checkedbox}{\settowidth{\tmpwidth}{\usebox{\tmpcasebox}}$\square$\kern-\tmpwidth\scalebox{1.2}{\color{red}$\checkmark$\kern-4pt}}")
        
        
    
        # Inclure un style personnalisé du titre si sélectionné
        if params.get("title_style") and params["title_style"] != "Classic":
            style_file_path = os.path.join("titlestyles", params["title_style"] + ".tex")
            try:
                with open(style_file_path, "r", encoding="utf-8") as f:
                    style_content = f.read()
                lines.append(f"% --- Début du style {params['title_style']} ---")
                lines.append(style_content)
                lines.append(f"% --- Fin du style {params['title_style']} ---\n")
            except FileNotFoundError:
                lines.append(f"% Style {params['title_style']} introuvable, on continue sans style.\n")
                
        # Inclure un style personnalisé des questions
        if params.get("question_style") and params["question_style"] != "Classic":
            style_file_path = os.path.join("questionstyles", params["question_style"] + ".tex")
            try:
                with open(style_file_path, "r", encoding="utf-8") as f:
                    style_content = f.read()
                lines.append(f"% --- Début du style des questions {params['question_style']} ---")
                lines.append(style_content)
                lines.append(f"% --- Fin du style des questions {params['question_style']} ---\n")
            except FileNotFoundError:
                lines.append(f"% Style {params['question_style']} introuvable, on continue sans style.\n")
                
        # Inclure un style personnalisé du numéro des pages
        if params.get("numberpage_style") and params["numberpage_style"] != "Classic":
            style_file_path = os.path.join("numberpagestyles", params["numberpage_style"] + ".tex")
            try:
                with open(style_file_path, "r", encoding="utf-8") as f:
                    style_content = f.read()
                lines.append(f"% --- Début du style des numéros de page {params['numberpage_style']} ---")
                lines.append(style_content)
                lines.append(f"% --- Fin du style des numéros de page {params['numberpage_style']} ---\n")
            except FileNotFoundError:
                lines.append(f"% Style {params['numberpage_style']} introuvable, on continue sans style.\n")
                
        # Inclure un style personnalisé dela consigne
        if params.get("consigne_style") and params["consigne_style"] != "":
            style_file_path = os.path.join("consignestyles", params["consigne_style"] + ".tex")
            try:
                with open(style_file_path, "r", encoding="utf-8") as f:
                    style_content = f.read()
                lines.append(f"% --- Début du style de la consigne {params['consigne_style']} ---")
                lines.append(style_content)
                lines.append(f"% --- Fin du style de la consigne {params['consigne_style']} ---\n")
            except FileNotFoundError:
                lines.append(f"% Style {params['consigne_style']} introuvable, on continue sans style.\n")
                
        if params["date"] != "":
            date = " - " + params["date"]
        else:
            date = ""
            
        if params.get("preamble") and params["preamble"] != "":
            lines.append(params["preamble"])
    
        lines += [
            "",
            r"\title{" + params.get("title", "Titre du devoir") + "}",
            r"\author{" + params.get("class_name", "") + "}",
            r"\date{" + params.get("duration", "") + date +  "}",
            "",
            r"\begin{document}",
            r"\maketitle",
            ""
        ]
        
        if params.get("numberpage_style") and params["numberpage_style"] != "Classic" and params["numberpage_style"] != "Nopageno":
            lines.append(r"\thispagestyle{fancy}")
    
        # Métadonnées supplémentaires    
        lines.append("")
        if params.get("consigne_style") and params["consigne_style"] != "":
            lines.append(r"\begin{consigne}{Consigne}") # Ici, le titre du cadre "Consigne"
            lines.append(params["consigne"])
            lines.append(r"\end{consigne}")
            lines.append("")
        
        # Charger les questions depuis questions.json
        questions_path = os.path.join(self.project_path, "questions.json")
        try:
            with open(questions_path, "r", encoding="utf-8") as f:
                questions = json.load(f)
        except FileNotFoundError:
            questions = []
        
        lines.append(r"\begin{enumerate}")

        for q in questions:
            lines.append(r"\begin{minipage}{\linewidth}")
            lines.append(r"\item " + q["libelle"])
        
            if q["type"] == "QCM":
                colonnes = q.get("colonnes", 1)
                if colonnes > 1:
                    lines.append(rf"\begin{{multicols}}{{{colonnes}}}")
        
                lines.append(r"\begin{itemize}")
                for prop in q.get("propositions", []):
                    if self.mode_corrige_var.get() and prop["correct"]:
                        lines.append(r"\item[\checkedbox] " + prop["texte"])
                    else:
                        lines.append(r"\item " + prop["texte"])
                       
                lines.append(r"\end{itemize}")
        
                if colonnes > 1:
                    lines.append(r"\end{multicols}")
        
            elif q["type"] == "Réponse libre":
                hauteur = q.get("hauteur", 5)
                lignes = q.get("lignes", False)
                
                if self.mode_corrige_var.get():
                    lines.append(rf"\newline\bgroup\itshape {q['bonne_reponse']}\egroup")
                else:
                    # Environnement TikZ personnalisé
                    lines += [
                        r"\begin{center}",
                        r"\begin{tikzpicture}",
                        rf"\draw[answerbox] (0,0) rectangle (\linewidth,{hauteur});"
                    ]
                    if lignes:
                        # lignes horizontales tous les 0.8cm
                        spacing = 0.8
                        count = int(hauteur // spacing)
                        for i in range(1, count+1):
                            y = i * spacing
                            lines.append(rf"\draw[lines] (0,{y}) -- (\linewidth,{y});")
                    lines += [
                        r"\end{tikzpicture}",
                        r"\end{center}"
                    ]
                    
            lines.append(r"\end{minipage}")
            lines.append("")
            lines.append(r"\bigskip")
            lines.append("")

        
        lines.append(r"\end{enumerate}")
        lines.append("")
        lines.append(r"\end{document}")
    
        return "\n".join(lines)
    
    def preview_extern(self):
        if self.mode_corrige_var.get():
            pdf_path = os.path.join(self.project_path, "preview_correction.pdf")
        else:
            pdf_path = os.path.join(self.project_path, "preview.pdf")
        
        self.preview_latex()
    
        try:
            if platform.system() == "Windows":
                os.startfile(pdf_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d’ouvrir le PDF : {e}")

