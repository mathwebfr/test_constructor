# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:08:32 2025

@author: Stéphane Pasquet
@url : mathweb.fr
"""

import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io
import tkinter as tk

class PreviewPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(self.frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.image_label.image = None

    def update_preview(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)  # Première page (index 0)
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # garder la référence
        except Exception as e:
            print(f"Erreur lors de l'affichage PDF : {e}")
