import os
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_pdf_to_image(output_dir):
    # Vérifier si le répertoire d'entrée existe
    if not os.path.exists(output_dir):
        raise Exception("Le répertoire d'entrée n'existe pas.")
    
    # Vérifier si le répertoire de destination existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Récupérer une liste de tous les fichiers PDF
    pdf_files = [f for f in os.listdir(output_dir) if f.endswith(".pdf") or f.endswith(".PDF") ]

    # Boucle sur tous les fichiers PDF
    for pdf_file in pdf_files:
        # Chemin d'accès complet au fichier PDF
        pdf_path = os.path.join(output_dir, pdf_file)
        
        # Ouvrir le fichier PDF
        pdf_doc = fitz.open(pdf_path)

        # Nom du fichier PDF sans extension
        pdf_filename = os.path.splitext(os.path.basename(pdf_file))[0]
        
        # Chemin d'accès au sous-dossier pour les images
        sub_dir = os.path.join(output_dir, pdf_filename)
        
        # Vérifier si le sous-dossier existe
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        # Boucle sur les pages du document PDF
        for page_number in range(pdf_doc.page_count):
            # Récupérer la page actuelle
            page = pdf_doc[page_number]
            
            # Construire le chemin d'accès complet à l'image
            output_path = os.path.join(sub_dir, f"{pdf_filename}_page_{page_number}.png")
            
            # Enregistrer la page en tant qu'image
            page.get_pixmap().save(output_path, 'PNG')

        # Fermer le document PDF
        pdf_doc.close()

def browse_folder():
    folder_path = filedialog.askdirectory()
    output_dir.set(folder_path)

def start_conversion():
    # Récupérer le chemin d'accès au répertoire
    folder_path = output_dir.get()

    try:
        convert_pdf_to_image(folder_path)
        messagebox.showinfo("Succès", "La conversion a été effectuée avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

root = tk.Tk()
root.geometry("350x150") # Définit la taille de la fenêtre à 500x500 pixels
root.title("Convertisseur PDF en Image")

output_dir = tk.StringVar()

folder_label = tk.Label(root, text="Chemin d'accès au répertoire :")
folder_entry = tk.Entry(root, width=20, textvariable=output_dir)
folder_entry.config(font=("Helvetica", 16))
browse_button = tk.Button(root, text="Parcourir", command=browse_folder)
convert_button = tk.Button(root, text="Convertir", command=start_conversion)

folder_label.pack()
folder_entry.pack()
browse_button.pack()
convert_button.pack()

root.mainloop()
