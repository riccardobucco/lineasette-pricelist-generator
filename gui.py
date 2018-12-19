import tkinter as tk

# Select a layout for the price list using a GUI
def select_layout(callback):
    def _close_window():
        root.quit()
        callback(layout.get())
    root = tk.Tk()
    root.geometry("400x400")
    layout = tk.IntVar()
    label = tk.Label(root, text="Seleziona il layout desiderato:")
    r1 = tk.Radiobutton(root, text="Orizzontale", variable=layout, value=0)
    r2 = tk.Radiobutton(root, text="Verticale", variable=layout, value=1)
    button = tk.Button(root, text="OK", command=_close_window)
    label.pack()
    r1.pack()
    r2.pack()
    button.pack()
    root.mainloop()