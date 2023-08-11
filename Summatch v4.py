import tkinter as tk
import customtkinter as Ctk
from tkinter import ttk, filedialog
import itertools

Ctk.set_appearance_mode("dark")
Ctk.set_default_color_theme("dark-blue")

def formatar_entry_soma():
    entrada_soma = entry_soma.get().replace("R$", "").replace(".", "").replace(",", ".")
    entry_soma.delete(0, tk.END)
    entry_soma.insert(tk.END, entrada_soma)

def encontrar_combinacao(event=None):
    formatar_entry_soma()
    soma_desejada = float(entry_soma.get().strip()) if entry_soma.get().strip() else None
    valores = [float(val.strip()) for val in entry_valores.get().split(";")]

    if soma_desejada is None:
        result_text = ""
    else:
        best_combination = None
        min_difference = float('inf')

        for r in range(1, len(valores) + 1):
            for combination in itertools.combinations(valores, r):
                current_sum = sum(combination)
                difference = abs(soma_desejada - current_sum)
                if difference < min_difference:
                    best_combination = combination
                    min_difference = difference

        if best_combination:
            result_text = "Valor encontrado:\n"
            for value in best_combination:
                result_text += " - {:.2f}\n".format(value)
            result_text += "\n(Diferença: {:.2f})".format(min_difference)
        else:
            result_text = "Valor mais próximo:\n{}\n(Diferença: {:.2f})".format(best_combination, min_difference)

    result_label.configure(state="normal")
    result_label.delete("1.0", tk.END)
    result_label.insert(tk.END, result_text)
    result_label.tag_add("1.0", tk.END)
    result_label.configure(state="disabled")

def importar_valores():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
            valores = ";".join([line.replace("R$", "").replace(".", "").replace(",", ".").strip() for line in lines])
        entry_valores.delete(0, tk.END)
        entry_valores.insert(tk.END, valores)

def resetar_valores():
    entry_soma.delete(0, tk.END)
    entry_valores.delete(0, tk.END)
    result_label.configure(state="normal")
    result_label.delete("1.0", tk.END)
    result_label.configure(state="disabled")

def mostrar_sobre():
    sobre_window = Ctk.Toplevel(root)
    sobre_window.title("Sobre")
    sobre_window.geometry("300x200")
    
    text_sobre = Ctk.Text(sobre_window, height=10, width=100)
    text_sobre.pack()
    text_sobre.insert(Ctk.END, "Versão: 1.0\n")
    text_sobre.insert(Ctk.END, "Autor: Derik Rodrigues\n")
    text_sobre.insert(Ctk.END, "Descrição: O SumMatch irá buscar e exibir a combinação correta dos valores, fornecendo uma solução rápida e conveniente para resolver quebra-cabeças de soma.")
    text_sobre.configure(state="normal")

root = Ctk.CTk() 
root.geometry("400x400")  # Aumenta a altura da janela para acomodar o resultado expandido
root.title("Sum Match v4")

frame = Ctk.CTkFrame(master=root)
frame.pack(pady=10, padx=20, fill="both",)

menu = Ctk.CTkButton(master=root, text="Importar valores",font=("Roboto", 16), border_width=2, command=importar_valores, height=35)
menu.pack()

label = Ctk.CTkLabel(master=frame, text="Encontrar combinação de valores", font=("Roboto", 23))
label.pack(pady=5, padx=5, fill="both")

entry_soma = Ctk.CTkEntry(master=frame, border_width=2, placeholder_text="Valor procurado")
entry_soma.pack(pady=5, padx=10, fill="both")

entry_valores = Ctk.CTkEntry(master=frame, border_width=2, placeholder_text="Valores a somar")
entry_valores.pack(pady=5, padx=10, fill="both")

button_encontrar = Ctk.CTkButton(master=frame, border_width=2, text="Encontrar Combinação", command=encontrar_combinacao, font=("Roboto", 13))
button_encontrar.pack(pady=5, padx=40)

button_reset = Ctk.CTkButton(master=frame, border_width=2, text="Reset", command=resetar_valores, font=("Roboto", 13))
button_reset.pack(pady=5, padx=40)

entry_soma.bind("<Return>", encontrar_combinacao)

result_frame = Ctk.CTkFrame(master=frame, border_width=3)
result_frame.pack(pady=10, padx=40, fill="both", expand=True)

result_label = Ctk.CTkTextbox(master=result_frame, border_width=4, wrap="word", state="disabled", height=120)
result_label.pack(pady=1, padx=1, fill="both", expand=True)

root.mainloop()
