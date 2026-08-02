import customtkinter as ctk


class SidebarMenu(ctk.CTkFrame):
    def __init__(self, parent, selecionar_aba_callback, toggle_callback=None):
        super().__init__(parent, width=60, corner_radius=0)

        self.parent = parent
        self.selecionar_aba_callback = selecionar_aba_callback  # Conecta com o main.py
        self.toggle_callback = toggle_callback
        self.is_expanded = False

        self.width_collapsed = 60
        self.width_expanded = 200

        self.pack_propagate(False)
        self.setup_widgets()

    def setup_widgets(self):
        # 1. Botão Hambúrguer
        self.hamburger_btn = ctk.CTkButton(
            self,
            text="☰",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=("black", "white"),
            font=("Arial", 24, "bold"),
            hover_color=("gray80", "gray20"),
            command=self.toggle_menu,
        )
        self.hamburger_btn.pack(pady=15, anchor="center")

        # 2. Botão Lembretes/Alarmes
        self.btn_lembretes = ctk.CTkButton(
            self,
            text="",
            width=40,
            height=45,
            fg_color="transparent",
            text_color="#a0a0a0",
            hover_color="#2b2b2b",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
            command=lambda: self.mudar_aba("alarmes", self.btn_lembretes),
        )
        self.btn_lembretes.pack(fill="x", padx=10, pady=5)

        # Define o ícone inicial quando recolhido
        self.btn_lembretes.configure(
            text="⏰" if not self.is_expanded else "⏰ Alarmes"
        )

        # 3. Botão Histórico / Calendário
        self.btn_historico = ctk.CTkButton(
            self,
            text="",
            width=40,
            height=45,
            fg_color="transparent",
            text_color="#a0a0a0",
            hover_color="#2b2b2b",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
            command=lambda: self.mudar_aba("calendario", self.btn_historico),
        )
        self.btn_historico.pack(fill="x", padx=10, pady=5)
        self.btn_historico.configure(
            text="📅" if not self.is_expanded else "📅 Calendário"
        )

    def toggle_menu(self):
        if self.is_expanded:
            self.configure(width=self.width_collapsed)
            self.btn_lembretes.configure(text="⏰", anchor="center")
            self.btn_historico.configure(text="📅", anchor="center")
            self.is_expanded = False
        else:
            self.configure(width=self.width_expanded)
            self.btn_lembretes.configure(text=" ⏰ Alarmes", anchor="w")
            self.btn_historico.configure(text=" 📅 Calendário", anchor="w")
            self.is_expanded = True

        if self.toggle_callback:
            self.toggle_callback(self.is_expanded)

    def mudar_aba(self, nome_aba, botao_clicado):
        # Reseta o estilo de todos os botões da barra lateral
        self.btn_lembretes.configure(fg_color="transparent", text_color="#a0a0a0")
        self.btn_historico.configure(fg_color="transparent", text_color="#a0a0a0")

        # Destaca o botão ativo
        botao_clicado.configure(fg_color="#1f538d", text_color="#ffffff")

        # Executa a troca de tela lá no main.py
        if self.selecionar_aba_callback:
            self.selecionar_aba_callback(nome_aba)
