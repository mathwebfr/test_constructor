# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:07:30 2025

@author: Stéphane Pasquet
@url : mathweb.fr
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from gui.input_panel import InputPanel
from gui.preview_panel import PreviewPanel
import json
import os

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Générateur de Devoirs - Stéphane Pasquet - mathweb.fr")
        #self.root.geometry("1000x600")
        self.root.iconbitmap("test_constructor.ico")
        self.root.state('zoomed')

        self.start_menu_frame = tk.Frame(self.root)
        self.start_menu_frame.pack(expand=True)

        label = tk.Label(self.start_menu_frame, text="Que souhaitez-vous faire ?", font=("Arial", 16))
        label.pack(pady=20)

        options = ["Choisir ici...","Créer un nouveau devoir", "Ouvrir un devoir existant"]
        self.choice_var = tk.StringVar(value=options[0])
        dropdown = tk.OptionMenu(self.start_menu_frame, self.choice_var, *options, command=self.menu_choice_selected)
        dropdown.config(width=30, font=("Arial", 12))
        dropdown.pack(pady=10)

    def menu_choice_selected(self, choice):
        if choice == "Créer un nouveau devoir":
            self.show_new_project_form()
        elif choice == "Ouvrir un devoir existant":
            # À implémenter plus tard
            self.open_existing_project()
        else:
            # autre item ?
            pass
        
    def open_existing_project(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionnez le fichier params.json",
            filetypes=[("Fichier JSON", "params.json")]
        )
        if not file_path:
            return  # L'utilisateur a annulé
    
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                params = json.load(f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")
            return
    
        # Enregistre le chemin du projet
        self.project_path = os.path.dirname(file_path)
    
        # Affiche les panneaux avec les valeurs préchargées
        self.show_main_panels(params)
        
    def show_main_panels(self, params):
        # Détruire le menu de démarrage
        self.start_menu_frame.pack_forget()
    
        # Créer les deux panneaux principaux
        self.input_panel = InputPanel(self.root, self.project_path, self, params)

        self.preview_panel = PreviewPanel(self.root)
    
        # Stocker une référence pour accès depuis InputPanel
        self.input_panel.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.preview_panel.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)




    def show_new_project_form(self):
        self.start_menu_frame.pack_forget()
    
        self.project_path = ""  # Emplacement de base
        self.project_name_var = tk.StringVar()
        self.project_location_var = tk.StringVar()
    
        self.new_project_frame = tk.Frame(self.root)
        self.new_project_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
        title_label = tk.Label(self.new_project_frame, text="Paramètres du nouveau devoir", font=("Arial", 14))
        title_label.pack(pady=(0, 20))
    
        # ---- Choix du dossier de base ----
        folder_frame = tk.Frame(self.new_project_frame)
        folder_frame.pack(fill=tk.X, pady=10)
    
        folder_label = tk.Label(folder_frame, text="Emplacement de base :", width=20, anchor="w")
        folder_label.pack(side=tk.LEFT)
    
        choose_button = tk.Button(folder_frame, text="Choisir un dossier", command=self.choose_directory)
        choose_button.pack(side=tk.LEFT)
    
        self.path_display = tk.Label(folder_frame, text="", fg="gray", anchor="w")
        self.path_display.pack(side=tk.LEFT, padx=10)
    
        # ---- Nom du devoir ----
        name_frame = tk.Frame(self.new_project_frame)
        name_frame.pack(fill=tk.X, pady=10)
    
        name_label = tk.Label(name_frame, text="Nom du devoir :", width=20, anchor="w")
        name_label.pack(side=tk.LEFT)
    
        name_entry = tk.Entry(name_frame, textvariable=self.project_name_var)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
        self.project_name_var.trace_add("write", self.update_final_path)
    
        # ---- Emplacement final affiché ----
        self.final_path_label = tk.Label(self.new_project_frame, text="", fg="blue", font=("Arial", 10, "italic"))
        self.final_path_label.pack(pady=20)
        
        # ---- Bouton de validation ----
        validate_btn = tk.Button(self.new_project_frame, text="Valider", command=self.validate_project, bg="green", fg="white", font=("Arial", 12))
        validate_btn.pack(pady=10)

        
    def choose_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path = path
            self.path_display.config(text=path)
            self.update_final_path()

    def update_final_path(self, *args):
        if self.project_path and self.project_name_var.get():
            final_path = f"{self.project_path}/{self.project_name_var.get()}"
            self.final_path_label.config(text=f"Le projet sera placé dans le dossier : {final_path}")
        else:
            self.final_path_label.config(text="")
            
    
    def validate_project(self):
        name = self.project_name_var.get()
        base_path = self.project_path
    
        if not name or not base_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner un emplacement et entrer un nom pour le devoir.")
            return
    
        self.project_full_path = os.path.join(base_path, name)
    
        try:
            os.makedirs(self.project_full_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier du devoir :\n{e}")
            return
    
        self.new_project_frame.pack_forget()
        self.show_main_editor()
        
    def show_main_editor(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
        # Panneau gauche
        self.input_panel = InputPanel(self.main_frame, self.project_full_path, self)
        self.input_panel.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # Panneau droit
        self.preview_panel = PreviewPanel(self.main_frame)
        self.preview_panel.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)






    def run(self):
        self.root.mainloop()

