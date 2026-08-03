import tkinter as tk
from tkinter import messagebox

# Lista de tarefas

tarefas = []

# Função adicionar tarefa

def adicionar_tarefa():

    tarefa = entrada.get().strip()
    if tarefa != "":

        lista_tarefas.insert(tk.END, tarefa)
        tarefas.append(tarefa)
        entrada.delete(0, tk.END)
        salvar_tarefas()

    else:
        messagebox.showwarning(
            "Aviso",
            "Digite uma tarefa!"
        )



def adicionar_tarefa_enter(event):
    adicionar_tarefa()

# Função remover tarefa

def remover_tarefa():
    try:
        indice = lista_tarefas.curselection()[0]
        lista_tarefas.delete(indice)
        tarefas.pop(indice)
        salvar_tarefas()

    except:
        messagebox.showwarning(
            "Aviso",
            "Selecione uma tarefa!"
        )

# Função concluir tarefa

def concluir_tarefa():
    try:
        indice = lista_tarefas.curselection()[0]
        tarefa = lista_tarefas.get(indice)
        if tarefa.startswith("✓ "):
            messagebox.showinfo(
                "Aviso",
                "Tarefa já concluída!"
          )

        else:
            lista_tarefas.delete(indice)
            lista_tarefas.insert(indice, "✓ " + tarefa)
            salvar_tarefas()

    except:
        messagebox.showwarning(
            "Aviso",
            "Selecione uma tarefa!"
        )

def salvar_tarefas():

    with open("tarefas.txt", "w", encoding="utf-8") as arquivo:
        itens = lista_tarefas.get(0, tk.END)
        for tarefa in itens:
            arquivo.write(tarefa + "\n")

def carregar_tarefas():
    try:
        with open("tarefas.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:

                tarefa = linha.strip()
                lista_tarefas.insert(tk.END, tarefa)
                tarefas.append(tarefa)

    except FileNotFoundError:

        pass

janela = tk.Tk()

janela.configure(bg="#1e1e1e")
janela.title("TAREFAS")
janela.geometry("400x600")


# Campo de texto

entrada = tk.Entry(
    janela,
    width=35,
    font=("Arial", 14),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"

)

entrada.pack(pady=15)

entrada.bind("<Return>", adicionar_tarefa_enter)


# Botão adicionar

botao_add = tk.Button(
    janela,
    text="Adicionar Tarefa",
    command=adicionar_tarefa,
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    width=20
)

botao_add.pack(pady=5)


# Lista de tarefas

lista_tarefas = tk.Listbox(
    janela,
    width=45,
    height=18,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    selectbackground="#444",
    selectforeground="white",
    highlightthickness=0,
    bd=0
)

lista_tarefas.pack(pady=15)

# Função para carregar tarefas ao iniciar o programa



carregar_tarefas()


# Botão remover

botao_remover = tk.Button(

    janela,
    text="Remover Tarefa",
    command=remover_tarefa,
    bg="#f44336",
    fg="white",
    activebackground="#d32f2f",
    width=20
)



botao_remover.pack(pady=5)

botao_concluir = tk.Button(

    janela,
    text="Concluir Tarefa",
    command=concluir_tarefa,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    width=20
)



botao_concluir.pack(pady=5)

# Rodar sistema

janela.mainloop()