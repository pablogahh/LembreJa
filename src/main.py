import threading
from tkinter import messagebox
import customtkinter as ctk

import components.components as comp
from components.sidebar import SidebarMenu
import database as db
import engine as eng
import formatters as fmt

# Carrega a preferência de tema antes de iniciar a janela
config = db.carregar_configuracoes()
ctk.set_appearance_mode(config.get("tema", "dark"))
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("LembreJá")
app.geometry("1200x700")
app.minsize(800, 500)

# Garante responsividade básica da janela principal
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Estado do Menu Hamburguer
menu_expandido = True

# --- MENU LATERAL (SIDEBAR) ---
sidebar = ctk.CTkFrame(app, width=250, corner_radius=0)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False) # Mantém a largura fixa sem 'encolher' pelos filhos

lbl_menu_titulo = ctk.CTkLabel(sidebar, text="Menu", font=("Segoe UI", 20, "bold"))
lbl_menu_titulo.pack(pady=(20, 15))

# --- ÁREA PRINCIPAL ---
main_area = ctk.CTkFrame(app, corner_radius=0)
main_area.pack(side="right", fill="both", expand=True)
main_area.pack_propagate(False)

# CABEÇALHO & HAMBURGUER & BOTÕES DE AÇÃO

header = ctk.CTkFrame(main_area, height=50, corner_radius=0)
header.pack(side="top", fill="x")

# Botão Hamburguer para alternar o Menu
def alternar_menu():
    global menu_expandido
    if menu_expandido:
        # Encolhe o menu
        sidebar.configure(width=65)
        lbl_menu_titulo.configure(text="")
        for nome, btn in botoes_menu.items():
            # Exibe apenas os emojis nos botões
            emoji = btn.cget("text").split(" ")[0]
            btn.configure(text=emoji, anchor="center")
        menu_expandido = False
    else:
        # Expande o menu
        sidebar.configure(width=250)
        lbl_menu_titulo.configure(text="Menu")
        mapeamento_textos = {
            "alarmes": "⏰ Alarmes",
            "calendario": "📅 Calendário",
            "categorias": "📂 Categorias",
            "estatisticas": "📊 Estatísticas",
            "configuracoes": "⚙️ Configurações"
        }
        for nome, btn in botoes_menu.items():
            btn.configure(text=mapeamento_textos[nome], anchor="w")
        menu_expandido = True

btn_hamburguer = ctk.CTkButton(
    header,
    text="☰",
    width=35,
    height=32,
    fg_color="transparent",
    hover_color=("#d0d0d0", "#3a3a3a"),
    text_color=("#1a1a1a", "#ffffff"),
    font=("Segoe UI", 18, "bold"),
    command=alternar_menu,
)
btn_hamburguer.pack(side="left", padx=(10, 5), pady=10)

lbl_logo = ctk.CTkLabel(header, text="🔔 LembreJá", font=("Segoe UI", 18, "bold"))
lbl_logo.pack(side="left", padx=10, pady=15)

def alternar_tema_rapido():
    config_atual = db.carregar_configuracoes()
    modo_atual = ctk.get_appearance_mode()

    novo_modo = "light" if modo_atual == "Dark" else "dark"
    ctk.set_appearance_mode(novo_modo)

    config_atual["tema"] = novo_modo
    db.salvar_configuracoes(config_atual)

    icone = "🌙" if novo_modo == "dark" else "☀️"
    btn_tema.configure(text=icone)

icone_inicial = "🌙" if config.get("tema", "dark") == "dark" else "☀️"

# Botão de Configurações 
btn_config = ctk.CTkButton(
    header,
    text="⚙️",
    width=40,
    height=32,
    fg_color=("#e0e0e0", "#2b2b2b"),
    hover_color=("#d0d0d0", "#3a3a3a"),
    text_color=("#1a1a1a", "#ffffff"),
    command=lambda: selecionar_aba("configuracoes"),
)
btn_config.pack(side="right", padx=15, pady=10)

# Botão de Tema 
btn_tema = ctk.CTkButton(
    header,
    text=icone_inicial,
    width=40,
    height=32,
    fg_color=("#e0e0e0", "#2b2b2b"),
    hover_color=("#d0d0d0", "#3a3a3a"),
    text_color=("#1a1a1a", "#ffffff"),
    command=alternar_tema_rapido,
)
btn_tema.pack(side="right", padx=(0, 5), pady=10)

# Container Principal Scrollável (Responsivo)
content = ctk.CTkScrollableFrame(main_area, fg_color="transparent")
content.pack(padx=20, pady=20, fill="both", expand=True)

botoes_menu = {}
btn_novo_alarme = None


def recarregar_interface_cards():
    global btn_novo_alarme
    for widget in content.winfo_children():
        if widget != btn_novo_alarme:
            widget.destroy()

    alarmes_ativos = db.carregar_alarmes()
    for alarme in alarmes_ativos:
        comp.criar_card_alarme(app, content, alarme, recarregar_interface_cards)


def carregar_tela_alarmes():
    global btn_novo_alarme
    btn_novo_alarme = ctk.CTkButton(
        content,
        text="➕ Novo Alarme",
        height=45,
        font=("Segoe UI", 14, "bold"),
        command=lambda: comp.abrir_janela_alarme(
            app, content, recarregar_interface_cards
        ),
    )
    btn_novo_alarme.pack(anchor="nw", pady=(0, 10))
    recarregar_interface_cards()


def carregar_tela_estatisticas():
    for widget in content.winfo_children():
        widget.destroy()

    lbl_titulo = ctk.CTkLabel(
        content, text="📊 Estatísticas & Produtividade", font=("Segoe UI", 24, "bold")
    )
    lbl_titulo.pack(anchor="nw", pady=(10, 20))

    dados = db.obter_estatisticas()

    frame_kpis = ctk.CTkFrame(content, fg_color="transparent")
    frame_kpis.pack(fill="x", pady=(0, 20))

    for i in range(4):
        frame_kpis.grid_columnconfigure(i, weight=1)

    def criar_kpi_card(parent, coluna, titulo, valor, icone, cor_destaque):
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=("#ffffff", "#2b2b2b"),
            border_width=1,
            border_color=("#e0e0e0", "#3a3a3a"),
        )
        card.grid(row=0, column=coluna, padx=5, pady=5, sticky="nsew")

        barra = ctk.CTkFrame(card, height=4, fg_color=cor_destaque, corner_radius=2)
        barra.pack(fill="x", side="top")

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(padx=12, pady=12, fill="both")

        ctk.CTkLabel(
            info_frame,
            text=f"{icone} {titulo}",
            font=("Segoe UI", 11),
            text_color=("#666666", "#a0a0a0"),
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=str(valor),
            font=("Segoe UI", 20, "bold"),
            text_color=("#1a1a1a", "#ffffff"),
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))

    criar_kpi_card(frame_kpis, 0, "Total Alarmes", dados["total_alarmes"], "⏰", "#1f538d")
    criar_kpi_card(frame_kpis, 1, "Ativos", dados["ativos"], "🟢", "#2e7d32")
    criar_kpi_card(frame_kpis, 2, "Histórico", dados["historico"], "📜", "#8e24aa")
    criar_kpi_card(frame_kpis, 3, "Popular", dados["cat_mais_popular"], "⭐", "#f57c00")

    lbl_sub = ctk.CTkLabel(
        content, text="📂 Distribuição por Categoria", font=("Segoe UI", 18, "bold")
    )
    lbl_sub.pack(anchor="nw", pady=(10, 10))

    frame_categorias = ctk.CTkFrame(
        content,
        fg_color=("#ffffff", "#2b2b2b"),
        corner_radius=12,
        border_width=1,
        border_color=("#e0e0e0", "#3a3a3a"),
    )
    frame_categorias.pack(fill="x", pady=5, padx=5)

    if not dados["detalhes_categorias"]:
        ctk.CTkLabel(
            frame_categorias, text="Nenhuma categoria cadastrada.", text_color="#888888"
        ).pack(pady=20)
    else:
        for nome_cat, info in dados["detalhes_categorias"].items():
            linha = ctk.CTkFrame(frame_categorias, fg_color="transparent")
            linha.pack(fill="x", padx=20, pady=10)

            info_linha = ctk.CTkFrame(linha, fg_color="transparent")
            info_linha.pack(fill="x")

            ctk.CTkLabel(
                info_linha,
                text=nome_cat,
                font=("Segoe UI", 14, "bold"),
                text_color=("#1a1a1a", "#ffffff"),
            ).pack(side="left")

            ctk.CTkLabel(
                info_linha,
                text=f"{info['qtd']} alarmes ({info['porcentagem']:.1f}%)",
                font=("Segoe UI", 12),
                text_color=("#666666", "#a0a0a0"),
            ).pack(side="right")

            progress = ctk.CTkProgressBar(linha, height=10, corner_radius=5)
            progress.pack(fill="x", pady=(5, 0))
            progress.set(info["porcentagem"] / 100)
            progress.configure(
                progress_color=info["cor"], fg_color=("#e0e0e0", "#1e1e1e")
            )


def carregar_tela_configuracoes():
    for widget in content.winfo_children():
        widget.destroy()

    lbl_titulo = ctk.CTkLabel(
        content, text="⚙️ Configurações", font=("Segoe UI", 24, "bold")
    )
    lbl_titulo.pack(anchor="nw", pady=(10, 20))

    config_atual = db.carregar_configuracoes()

    estilo_card = {
        "fg_color": ("#ffffff", "#2b2b2b"),
        "corner_radius": 12,
        "border_width": 1,
        "border_color": ("#e0e0e0", "#3a3a3a"),
    }

    # APARÊNCIA
    frame_aparencia = ctk.CTkFrame(content, **estilo_card)
    frame_aparencia.pack(fill="x", pady=10, padx=5)

    lbl_aparencia = ctk.CTkLabel(
        frame_aparencia,
        text="🎨 Aparência",
        font=("Segoe UI", 16, "bold"),
        text_color=("#1a1a1a", "#ffffff"),
    )
    lbl_aparencia.pack(anchor="w", padx=20, pady=(15, 10))

    row_tema = ctk.CTkFrame(frame_aparencia, fg_color="transparent")
    row_tema.pack(fill="x", padx=20, pady=(0, 15))

    ctk.CTkLabel(
        row_tema,
        text="Tema do Aplicativo:",
        font=("Segoe UI", 13),
        text_color=("#333333", "#dce1e6"),
    ).pack(side="left")

    def mudar_tema(novo_tema):
        modo = "dark" if novo_tema == "Escuro" else "light"
        ctk.set_appearance_mode(modo)
        config_atual["tema"] = modo
        db.salvar_configuracoes(config_atual)

    opt_tema = ctk.CTkOptionMenu(
        row_tema, values=["Escuro", "Claro"], command=mudar_tema, width=120
    )
    opt_tema.set("Escuro" if config_atual.get("tema") == "dark" else "Claro")
    opt_tema.pack(side="right")

    # PREFERÊNCIAS DE ALARME
    frame_alarmes = ctk.CTkFrame(content, **estilo_card)
    frame_alarmes.pack(fill="x", pady=10, padx=5)

    lbl_alarmes_tit = ctk.CTkLabel(
        frame_alarmes,
        text="🔔 Notificações & Som",
        font=("Segoe UI", 16, "bold"),
        text_color=("#1a1a1a", "#ffffff"),
    )
    lbl_alarmes_tit.pack(anchor="w", padx=20, pady=(15, 10))

    row_som = ctk.CTkFrame(frame_alarmes, fg_color="transparent")
    row_som.pack(fill="x", padx=20, pady=(0, 15))

    def toggle_som():
        config_atual["som_alarme"] = switch_som.get() == 1
        db.salvar_configuracoes(config_atual)

    switch_som = ctk.CTkSwitch(
        row_som,
        text="Emitir sinal sonoro nos alarmes",
        font=("Segoe UI", 13),
        command=toggle_som,
        text_color=("#333333", "#dce1e6"),
    )
    if config_atual.get("som_alarme", True):
        switch_som.select()
    else:
        switch_som.deselect()
    switch_som.pack(anchor="w")

    # GERENCIAMENTO DE DADOS
    frame_dados = ctk.CTkFrame(content, **estilo_card)
    frame_dados.pack(fill="x", pady=10, padx=5)

    lbl_dados_tit = ctk.CTkLabel(
        frame_dados,
        text="🛠️ Gerenciamento de Dados",
        font=("Segoe UI", 16, "bold"),
        text_color=("#1a1a1a", "#ffffff"),
    )
    lbl_dados_tit.pack(anchor="w", padx=20, pady=(15, 10))

    row_botoes = ctk.CTkFrame(frame_dados, fg_color="transparent")
    row_botoes.pack(fill="x", padx=20, pady=(0, 15))

    def acao_limpar_historico():
        if messagebox.askyesno(
            "⚠️ Limpar Histórico",
            "Tem certeza que deseja apagar todo o histórico de alarmes já disparados?",
        ):
            db.limpar_historico()
            messagebox.showinfo("Sucesso", "Histórico apagado com sucesso!")

    btn_limpar_hist = ctk.CTkButton(
        row_botoes,
        text="🗑️ Limpar Histórico",
        fg_color=("#fde8e8", "#3a1a1a"),
        hover_color=("#f8b4b4", "#c84343"),
        text_color=("#9b1c1c", "#ff9999"),
        font=("Segoe UI", 12, "bold"),
        command=acao_limpar_historico,
    )
    btn_limpar_hist.pack(side="left", padx=(0, 10))


def carregar_tela_categorias():
    for widget in content.winfo_children():
        widget.destroy()

    lbl_titulo = ctk.CTkLabel(
        content, text="📁 Minhas Categorias", font=("Segoe UI", 24, "bold")
    )
    lbl_titulo.pack(anchor="nw", pady=(10, 20))

    btn_nova_cat = ctk.CTkButton(
        content,
        text="➕ Nova Categoria",
        height=40,
        font=("Segoe UI", 13, "bold"),
        command=lambda: abrir_janela_categoria(),
    )
    btn_nova_cat.pack(anchor="nw", pady=(0, 20))

    frame_lista = ctk.CTkFrame(content, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)

    lista_categorias = db.carregar_categorias()
    lista_alarmes = db.carregar_alarmes()

    for cat in lista_categorias:
        total_alarmes = sum(
            1 for alarme in lista_alarmes if str(alarme.get("categoria_id")) == str(cat["id"])
        )

        card = ctk.CTkFrame(frame_lista, height=60, corner_radius=8)
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)

        barra_cor = ctk.CTkFrame(card, width=12, fg_color=cat["cor"], corner_radius=0)
        barra_cor.pack(side="left", fill="y")

        lbl_nome = ctk.CTkLabel(card, text=cat["nome"], font=("Segoe UI", 15, "bold"), anchor="w")
        lbl_nome.pack(side="left", padx=15, pady=15, fill="x", expand=True)

        frame_direita = ctk.CTkFrame(card, fg_color="transparent")
        frame_direita.pack(side="right", padx=15)

        lbl_contador = ctk.CTkLabel(
            frame_direita,
            text=f"⏰ {total_alarmes} vinculados",
            font=("Segoe UI", 13),
            text_color="#888888",
        )
        lbl_contador.pack(side="left", padx=(0, 15))

        btn_editar = ctk.CTkButton(
            frame_direita,
            text="✏️",
            width=35,
            height=32,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            command=lambda c=cat: abrir_janela_categoria(categoria_para_editar=c),
        )
        btn_editar.pack(side="left", padx=3)

        btn_excluir = ctk.CTkButton(
            frame_direita,
            text="🗑️ Excluir",
            width=85,
            height=34,
            corner_radius=8,
            fg_color="#3a1a1a",       
            hover_color="#c84343",     
            text_color="#ff9999",      
            font=("Segoe UI", 12, "bold"),
            command=lambda c_id=cat["id"], c_nome=cat["nome"], qtd=total_alarmes: confirmar_exclusao_categoria(c_id, c_nome, qtd),
        )
        btn_excluir.pack(side="left", padx=4)


def abrir_janela_categoria(categoria_para_editar=None):
    janela_pop = ctk.CTkToplevel(app)
    titulo_modal = "✏️ Editar Categoria" if categoria_para_editar else "📁 Nova Categoria"
    janela_pop.title(titulo_modal)
    janela_pop.geometry("400x270")
    janela_pop.resizable(False, False)

    janela_pop.grab_set()
    janela_pop.attributes("-topmost", True)

    opcoes_cores = {
        "🔴 Vermelho": "#FF5555",
        "🟢 Verde": "#50FA7B",
        "🔵 Azul": "#8BE9FD",
        "🟡 Amarelo": "#F1FA8C",
        "🟣 Roxo": "#BD93F9",
        "🟠 Laranja": "#FFB86C",
        "⚪ Cinza": "#6272A4",
    }

    ctk.CTkLabel(
        janela_pop, text="Nome da Categoria:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(20, 5))

    txt_nome = ctk.CTkEntry(
        janela_pop, width=360, placeholder_text="Ex: Finanças, Saúde, Academia..."
    )
    txt_nome.pack(padx=20, pady=5)

    ctk.CTkLabel(
        janela_pop, text="Selecione uma Cor:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(15, 5))

    combo_cores = ctk.CTkComboBox(
        janela_pop, width=360, values=list(opcoes_cores.keys()), state="readonly"
    )
    combo_cores.set("🔴 Vermelho")
    combo_cores.pack(padx=20, pady=5)

    if categoria_para_editar:
        txt_nome.insert(0, categoria_para_editar["nome"])
        for nome_cor, hex_code in opcoes_cores.items():
            if hex_code.lower() == categoria_para_editar["cor"].lower():
                combo_cores.set(nome_cor)
                break

    def salvar_clique():
        nome = txt_nome.get().strip()
        cor_selecionada_texto = combo_cores.get()
        cor = opcoes_cores[cor_selecionada_texto]

        if not nome:
            messagebox.showwarning(
                "⚠️ Ops!", "Por favor, digite o nome da categoria.", parent=janela_pop
            )
            return

        if categoria_para_editar:
            db.atualizar_categoria(categoria_para_editar["id"], nome, cor)
        else:
            db.criar_categorias(nome, cor)

        janela_pop.destroy()
        carregar_tela_categorias()

    texto_botao = "💾 Salvar Alterações" if categoria_para_editar else "💾 Salvar Categoria"
    
    btn_salvar = ctk.CTkButton(
        janela_pop,
        text=texto_botao,
        height=35,
        font=("Segoe UI", 13, "bold"),
        command=salvar_clique,
    )
    btn_salvar.pack(pady=25)


def confirmar_exclusao_categoria(cat_id, cat_nome, qtd_alarmes=0):
    if qtd_alarmes > 0:
        mensagem = (
            f"A categoria '{cat_nome}' possui {qtd_alarmes} alarme(s) vinculado(s)!\n\n"
            f"Se continuar, a categoria será apagada e os alarmes ficarão sem categoria.\n\n"
            f"Deseja realmente excluir?"
        )
    else:
        mensagem = f"Deseja realmente excluir a categoria '{cat_nome}'?"

    if messagebox.askyesno("⚠️ Confirmar Exclusão", mensagem):
        db.deletar_categoria(cat_id)
        carregar_tela_categorias()


def selecionar_aba(nome_aba):
    for nome, botao in botoes_menu.items():
        if nome == nome_aba:
            botao.configure(fg_color="#1f538d", text_color="#ffffff")
        else:
            botao.configure(fg_color="transparent", text_color="#a0a0a0")

    for widget in content.winfo_children():
        widget.destroy()

    if nome_aba == "alarmes":
        carregar_tela_alarmes()
    elif nome_aba == "calendario":
        comp.carregar_tela_calendario(app, content)
    elif nome_aba == "categorias":
        carregar_tela_categorias()
    elif nome_aba == "estatisticas":
        carregar_tela_estatisticas()
    elif nome_aba == "configuracoes":
        carregar_tela_configuracoes()


def criar_botao_menu(texto, comando_aba):
    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        height=45,
        anchor="w",
        fg_color="transparent",
        text_color="#a0a0a0",
        hover_color=("#e0e0e0", "#2b2b2b"),
        font=("Segoe UI", 13, "bold"),
        command=lambda: selecionar_aba(comando_aba),
    )
    botao.pack(fill="x", padx=10, pady=5)
    return botao


botoes_menu["alarmes"] = criar_botao_menu("⏰ Alarmes", "alarmes")
botoes_menu["calendario"] = criar_botao_menu("📅 Calendário", "calendario")
botoes_menu["categorias"] = criar_botao_menu("📂 Categorias", "categorias")
botoes_menu["estatisticas"] = criar_botao_menu("📊 Estatísticas", "estatisticas")
botoes_menu["configuracoes"] = criar_botao_menu("⚙️ Configurações", "configuracoes")

# Inicialização
selecionar_aba("alarmes")

threading.Thread(
    target=eng.verificar_alarmes_loop,
    args=(app, recarregar_interface_cards),
    daemon=True,
).start()

app.mainloop()