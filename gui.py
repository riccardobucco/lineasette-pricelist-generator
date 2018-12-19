from tkinter import Button, Label, messagebox, Radiobutton, Spinbox, Tk
from tkinter.filedialog import askopenfilename

import tkinter as tk

# Select a layout for the price list using a GUI
def get_user_input(callback):
    def _print_filename():
        filename = askopenfilename(filetypes=[("File Excel", "*.xls")])
        label_filename.config(text=filename)
    def _close_window():
        if label_filename["text"] == "":
            messagebox.showerror("Errore", "Devi selezionare un listino in formato Excel!")
        else:
            root.quit()
            callback(int(layout.get()), int(spinbox_multiple.get()), label_filename["text"])
    root = Tk()
    layout = tk.IntVar()
    root.geometry("1000x400")
    label_select_layout = Label(root, text="Seleziona il layout desiderato:")
    r1 = Radiobutton(root, text="Orizzontale (max 4 colonne per facciata)", variable=layout, value=0)
    r2 = Radiobutton(root, text="Verticale (max 3 colonne per facciata)", variable=layout, value=1)
    label_select_multiple = Label(root, text="Il listino avrà numero di colonne multiplo di:")
    spinbox_multiple = Spinbox(root, from_=1, to=16, width=3)
    label_select_pricelist = Label(root, text="Seleziona il listino in formato Excel:")
    button_choose_file = Button(root, text="Scegli file...", command=_print_filename)
    label_filename = Label(root, text="")
    button_ok = Button(root, text="OK", command=_close_window)
    label_select_layout.pack()
    r1.pack()
    r2.pack()
    label_select_multiple.pack()
    spinbox_multiple.pack()
    label_select_pricelist.pack()
    button_choose_file.pack()
    label_filename.pack()
    button_ok.pack()
    root.mainloop()