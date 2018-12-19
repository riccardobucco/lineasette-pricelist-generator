from tkinter import messagebox, Tk
from tkinter.filedialog import askopenfilename

import tkinter as tk

# Select a layout for the price list using a GUI
def select_layout(callback):
    def _print_filename():
        filename = askopenfilename(filetypes=[("Excel files", "*.xls")])
        label_filename.config(text=filename)
    def _close_window():
        if label_filename["text"] == "":
            messagebox.showerror("Errore", "Devi selezionare un listino in formato Excel!")
        else:
            root.quit()
            callback(layout.get(), label_filename["text"])
    root = Tk()
    root.geometry("1000x400")
    layout = tk.IntVar()
    label_select_layout = tk.Label(root, text="Seleziona il layout desiderato:")
    r1 = tk.Radiobutton(root, text="Orizzontale", variable=layout, value=0)
    r2 = tk.Radiobutton(root, text="Verticale", variable=layout, value=1)
    label_select_pricelist = tk.Label(root, text="Seleziona il listino in formato Excel:")
    button_choose_file = tk.Button(root, text="Scegli file...", command=_print_filename)
    label_filename = tk.Label(root, text="")
    button_ok = tk.Button(root, text="OK", command=_close_window)
    label_select_layout.pack()
    r1.pack()
    r2.pack()
    label_select_pricelist.pack()
    button_choose_file.pack()
    label_filename.pack()
    button_ok.pack()
    root.mainloop()