import tkinter as tk
from queue import Queue

def init_popup(queue: Queue):
    janela = tk.Tk()
    # janela.title('Popup de Texto')
    janela.geometry("500x300")

    caixa_de_texto = tk.Text(janela, wrap=tk.WORD, height=10, width=50)
    caixa_de_texto.pack(expand=1, fill=tk.BOTH)

    def update_text():
        if not queue.empty():
            texto = queue.get()
            if not isinstance(texto, str):
                texto = "Comando incorreto..."
            caixa_de_texto.config(state=tk.NORMAL)
            caixa_de_texto.delete(1.0, tk.END)
            caixa_de_texto.insert(tk.END, texto + "\n")
            caixa_de_texto.config(state=tk.DISABLED)
            janela.deiconify()
            janela.focus_force()

        janela.after(100, update_text)

    janela.iconify()
    update_text()
    janela.mainloop()
