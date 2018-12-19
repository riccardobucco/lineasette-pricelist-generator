from tkinter import Button, Label, messagebox, Radiobutton, Spinbox, Tk
from tkinter.filedialog import askdirectory, askopenfilename

import tkinter as tk

# Select a layout for the price list using a GUI
def get_user_input(callback):
    def _choose_pricelist():
        filename = askopenfilename(filetypes=[("File Excel", "*.xls")])
        label_filename.config(text=filename)
    def _choose_images_location():
        folder = askdirectory()
        label_images_location.config(text=folder)
    def _choose_save_location():
        folder = askdirectory()
        label_save_location.config(text=folder)
    def _close_window():
        if label_filename["text"] == "":
            messagebox.showerror("Errore", "Devi selezionare un listino in formato Excel!")
        elif label_save_location["text"] == "":
            messagebox.showerror("Errore", "Devi specificare dove vuoi salvare il listino in formato html!")
        else:
            root.quit()
            callback(int(layout.get()), int(spinbox_multiple.get()), label_filename["text"], label_images_location["text"], label_save_location["text"])
    root = Tk()
    layout = tk.IntVar()
    root.geometry("1000x400")
    label_select_layout = Label(root, text="Seleziona il layout desiderato:")
    r1 = Radiobutton(root, text="Orizzontale (max 4 colonne per facciata)", variable=layout, value=0)
    r2 = Radiobutton(root, text="Verticale (max 3 colonne per facciata)", variable=layout, value=1)
    label_select_multiple = Label(root, text="Il listino avrà numero di colonne multiplo di:")
    spinbox_multiple = Spinbox(root, from_=1, to=16, width=3)
    label_select_pricelist = Label(root, text="Seleziona il listino in formato Excel:")
    button_choose_file = Button(root, text="Scegli file...", command=_choose_pricelist)
    label_filename = Label(root, text="")
    label_ask_images_location = Label(root, text="Seleziona la cartella contenente le immagini:")
    button_choose_images_location = Button(root, text="Scegli cartella...", command=_choose_images_location)
    label_images_location = Label(root, text="")
    label_ask_save_location = Label(root, text="Specifica dove vuoi salvare il listino in formato html:")
    button_choose_save_location = Button(root, text="Scegli cartella...", command=_choose_save_location)
    label_save_location = Label(root, text="")
    button_ok = Button(root, text="OK", command=_close_window)
    label_select_layout.pack()
    r1.pack()
    r2.pack()
    label_select_multiple.pack()
    spinbox_multiple.pack()
    label_select_pricelist.pack()
    button_choose_file.pack()
    label_filename.pack()
    label_ask_images_location.pack()
    button_choose_images_location.pack()
    label_images_location.pack()
    label_ask_save_location.pack()
    button_choose_save_location.pack()
    label_save_location.pack()
    button_ok.pack()
    root.mainloop()