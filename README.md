# Générateur de Devoirs – Stéphane Pasquet

**Un outil Python avec interface graphique (Tkinter) pour générer automatiquement des sujets de devoirs LaTeX à destination des enseignants.**

## ✨ Fonctionnalités

- Interface intuitive pour :
  - Renseigner les informations générales du devoir (titre, classe, date, durée…)
  - Ajouter des questions de type QCM ou Réponse libre
  - Visualiser le devoir ou la correction
- Génération de code LaTeX avec :
  - Mise en page personnalisée
  - Cadres de réponses adaptés
  - Affichage des bonnes réponses en mode "corrigé"
- Visualisation directe du PDF généré via le visualiseur système

## 🛠️ Technologies utilisées

- Python 3.x
- Tkinter pour l'interface graphique
- LaTeX pour la mise en forme
- `os`, `subprocess`, `json` pour le traitement en arrière-plan

## 🚀 Lancer l'application

```bash
python main.py
```

> Assurez-vous que `pdflatex` (distribué par [TeX Live](https://www.tug.org/texlive/) ou [MiKTeX](https://miktex.org/)) est installé et accessible via la ligne de commande.

## 📁 Organisation du projet

```
test-constructor/
├── boxstyles/
├────── Style01.tex
├────── Style02.tex
├────── Style03.tex
├────── Style04.tex
├────── Style05.tex
├────── Style06.tex
├── consignestyles/
├────── Modern.tex
├────── Simple.tex
├── gui/
├────── input_panel.py
├────── main_window.py
├────── preview_panel.py
├── numberpagestyles/
├────── Frameboxed.tex
├────── Nopageno.tex
├────── Shadow.tex
├────── Sobre.tex
├── questionstyles/
├────── Boxed.tex
├────── Frameboxed.tex
├────── Labeled.tex
├────── Simple.tex
├── titlestyles/
├────── Minimalist.tex
├────── Shadow.tex
├────── WithNameMinimalist.tex
├────── WithNameShadow.tex
├── main.py
├── test_constructor.ico
```
## 📄 Ajout de templates

Vous pouvez ajouter les styles que vous voulez (il suffit d'utiliser la même syntaxe LaTeX que les autres fichiers). Et je serai ravi de les ajouter au projet!

## 📦 Installation des dépendances

Ce projet n’utilise que la bibliothèque standard de Python.  
Aucune installation de package externe n’est requise.


## 📝 Licence

MIT License – libre d'utilisation et de modification.

## 👨‍🏫 Auteur

**Stéphane Pasquet**  
[mathweb.fr](https://www.mathweb.fr)
