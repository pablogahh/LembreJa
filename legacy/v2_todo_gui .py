import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.LIMITE_CARACTERES = 50

        # Tema escuro
        self.tema_atual = "escuro"

        self.temas = {
            "escuro": {
                "bg": "#1e1e1e",
                "fg": "white",
                "frame": "#2d2d2d",
                "entry": "#3a3a3a",
                "button": "#4CAF50",
                "listbox": "#2b2b2b",
            },
            "claro": {
                "bg": "#f5f7fa",
                "fg": "#2c3e50",
                "frame": "#f5f7fa",
                "entry": "#ffffff",
                "button": "#2196F3",
                "listbox": "#ffffff",
                "pendentes_bg": "#FFF8E1",
                "pendentes_fg": "#F59E0B",
                "concluidas_bg": "#E8F5E9",
                "concluidas_fg": "#4CAF50",
            },
        }

        self.master.title("TAREFAS")
        self.master.geometry("900x600")
        self.master.configure(bg=self.temas[self.tema_atual]["bg"])
        self.master.minsize(800, 800)

        self.arquivo = "tarefas.json"
        self.tarefas = {"pendentes": [], "concluidas": []}

        self._build_ui()
        self.carregar_dados()
        self.aplicar_tema()

    def _build_ui(self):

        # TÍTULO
        self.lbl_titulo = tk.Label(
            self.master,
            text="📋 TAREFAS PRO",
            bg="#1e1e1e",
            fg="#FFC107",
            font=("Arial", 18, "bold"),
        )
        self.lbl_titulo.pack(pady=15)

        # BOTÃO DE TROCAR TEMA
        self.btn_tema = tk.Button(
            self.master,
            text="🌗",
            command=self.alternar_tema,
            font=("Segoe UI",),
            bg="#1e1e1e",
            fg="white",
            activebackground="#1e1e1e",
            activeforeground="white",
            bd=0,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
        )
        self.btn_tema.place(x=10, y=10)

        # ENTRY
        self.entrada = tk.Entry(
            self.master,
            width=50,
            font=("Arial", 14),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
        )

        self.contador = tk.Label(
            self.master,
            text=f"0/{self.LIMITE_CARACTERES}",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 10),
        )
        self.contador.pack()

        self.entrada.pack(pady=10)

        # ENTER adiciona tarefa
        self.entrada.bind("<Return>", self.adicionar_tarefa)

        # CONTADOR DE CARACTERES
        self.entrada.bind("<KeyRelease>", self.atualizar_contador)

        # BOTÃO ADD
        tk.Button(
            self.master,
            text="Adicionar Tarefa",
            command=self.adicionar_tarefa,
            bg="#2196F3",
            fg="white",
            width=25,
            height=1,
        ).pack(pady=5)

        # ---------------- FRAME PRINCIPAL ----------------
        self.frame_principal = tk.Frame(
            self.master,
            bg="#1e1e1e",
        )

        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        # PENDENTES
        self.left_frame = tk.Frame(self.frame_principal, bg="#1e1e1e")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=20)

        self.lbl_pendentes = tk.Label(
            self.left_frame,
            text="📌 Pendentes",
            bg="#1e1e1e",
            fg="#FFC107",
            font=("Arial", 14, "bold"),
        )
        self.lbl_pendentes.pack(pady=10)

        self.lista_pendentes = tk.Listbox(
            self.left_frame,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="#FFC107",
            selectbackground="#444",
            selectforeground="#FFC107",
            activestyle="none",
            borderwidth=0,
            height=18,
        )
        self.lista_pendentes.pack(fill="both", expand=True)
        self.lista_pendentes.bind("<Double-Button-1>", self.editar_tarefa)

        # CONCLUÍDAS
        self.right_frame = tk.Frame(self.frame_principal, bg="#1e1e1e")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20)

        self.lbl_concluidas = tk.Label(
            self.right_frame,
            text="✅ Concluídas",
            bg="#1e1e1e",
            fg="#4CAF50",
            font=("Arial", 14, "bold"),
        )
        self.lbl_concluidas.pack(pady=10)

        self.lista_concluidas = tk.Listbox(
            self.right_frame,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="#4CAF50",
            selectbackground="#444",
            selectforeground="#4CAF50",
            activestyle="none",
            borderwidth=0,
            height=18,
        )
        self.lista_concluidas.pack(fill="both", expand=True)

        # ---------------- BOTÕES ----------------
        self.button_frame = tk.Frame(self.master, bg="#1e1e1e")
        self.button_frame.pack(pady=15)

        tk.Button(
            self.button_frame,
            text="Concluir",
            command=self.concluir_tarefa,
            bg="#4CAF50",
            fg="white",
            width=15,
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            self.button_frame,
            text="Editar",
            command=self.editar_tarefa,
            bg="#FF9800",
            fg="white",
            width=15,
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            self.button_frame,
            text="Remover",
            command=self.remover_tarefa,
            bg="#f44336",
            fg="white",
            width=15,
        ).grid(row=0, column=2, padx=10)

    # ---------------- LÓGICA ----------------

    def adicionar_tarefa(self, event=None):
        texto = self.entrada.get().strip()

        if not texto:
            messagebox.showwarning("Aviso", "Digite uma tarefa!")
            return

        if len(texto) > self.LIMITE_CARACTERES:
            messagebox.showwarning(
                "Limite excedido", f"Máximo de {self.LIMITE_CARACTERES} caracteres!"
            )
            return

        self.tarefas["pendentes"].append(texto)
        self.entrada.delete(0, tk.END)

        self.atualizar_contador()
        self.salvar_dados()
        self.atualizar_interface()

    def atualizar_contador(self, event=None):
        texto = self.entrada.get()
        tamanho = len(texto)

        self.contador.config(text=f"{tamanho}/{self.LIMITE_CARACTERES}")

        if tamanho > self.LIMITE_CARACTERES:
            self.contador.config(fg="red")
        else:
            self.contador.config(fg="white")

    def concluir_tarefa(self):
        sel = self.lista_pendentes.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
            return

        i = sel[0]
        tarefa = self.tarefas["pendentes"].pop(i)
        self.tarefas["concluidas"].append(tarefa)

        self.salvar_dados()
        self.atualizar_interface()

    def remover_tarefa(self):
        sel_p = self.lista_pendentes.curselection()
        sel_c = self.lista_concluidas.curselection()

        if sel_p:
            del self.tarefas["pendentes"][sel_p[0]]
        elif sel_c:
            del self.tarefas["concluidas"][sel_c[0]]
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
            return

        self.salvar_dados()
        self.atualizar_interface()

    def editar_tarefa(self, event=None):
        sel = self.lista_pendentes.curselection()

        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma tarefa pendente!")
            return

        i = sel[0]
        atual = self.tarefas["pendentes"][i]

        novo = simpledialog.askstring(
            "Editar tarefa", "Altere a tarefa:", initialvalue=atual
        )

        if novo and novo.strip():
            self.tarefas["pendentes"][i] = novo.strip()
            self.salvar_dados()
            self.atualizar_interface()

    def alternar_tema(self):
        if self.tema_atual == "escuro":
            self.tema_atual = "claro"
        else:
            self.tema_atual = "escuro"

        self.aplicar_tema()

    def aplicar_tema(self):

        if self.tema_atual == "escuro":

            self.master.configure(bg="#1e1e1e")

            self.lbl_titulo.configure(bg="#1e1e1e", fg="white")

            self.contador.configure(bg="#1e1e1e", fg="white")

            self.frame_principal.configure(bg="#1e1e1e")
            self.left_frame.configure(bg="#1e1e1e")
            self.right_frame.configure(bg="#1e1e1e")
            self.button_frame.configure(bg="#1e1e1e")

            self.lbl_pendentes.configure(bg="#1e1e1e", fg="#FFC107")

            self.lbl_concluidas.configure(bg="#1e1e1e", fg="#4CAF50")

            self.entrada.configure(bg="#2b2b2b", fg="white", insertbackground="white")

            self.lista_pendentes.configure(
                bg="#2b2b2b", fg="#FFC107", selectbackground="#444"
            )

            self.lista_concluidas.configure(
                bg="#2b2b2b", fg="#4CAF50", selectbackground="#444"
            )

        else:

            self.master.configure(bg="#f5f7fa")

            self.lbl_titulo.configure(bg="#f5f7fa", fg="#2c3e50")

            self.contador.configure(bg="#f5f7fa", fg="#2c3e50")

            self.frame_principal.configure(bg="#f5f7fa")
            self.left_frame.configure(bg="#f5f7fa")
            self.right_frame.configure(bg="#f5f7fa")
            self.button_frame.configure(bg="#f5f7fa")

            self.lbl_pendentes.configure(bg="#f5f7fa", fg="#625F59")

            self.lbl_concluidas.configure(bg="#f5f7fa", fg="#4CAF50")

            self.entrada.configure(
                bg="#ffffff", fg="#2c3e50", insertbackground="#2c3e50"
            )

            self.lista_pendentes.configure(
                bg="#FFF8E1", fg="#000000", selectbackground="#37474F"
            )

            self.lista_concluidas.configure(
                bg="#E8F5E9", fg="#000000", selectbackground="#37474F"
            )

    # ---------------- ARQUIVO ----------------

    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, indent=4, ensure_ascii=False)

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
        else:
            self.tarefas = {"pendentes": [], "concluidas": []}

        self.atualizar_interface()

    # ---------------- UI UPDATE ----------------

    def atualizar_interface(self):
        self.lista_pendentes.delete(0, tk.END)
        self.lista_concluidas.delete(0, tk.END)

        for t in self.tarefas["pendentes"]:
            self.lista_pendentes.insert(tk.END, f"⏳ {t}")

        for t in self.tarefas["concluidas"]:
            self.lista_concluidas.insert(tk.END, f"✓ {t}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
