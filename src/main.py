import threading
from tkinter import messagebox
import customtkinter as ctk

import components.components as comp
from components.sidebar import SidebarMenu
import database as db
import engine as eng
import formatters as fmt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("LembreJá")
app.geometry("1200x700")

# Menu Lateral
sidebar = ctk.CTkFrame(app, width=250, corner_radius=0)
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="Menu", font=("Segoe UI", 22, "bold")).pack(pady=(30, 20))

# Área Principal
main_area = ctk.CTkFrame(app, corner_radius=0)
main_area.pack(side="right", fill="both", expand=True)
main_area.pack_propagate(False)

# Cabeçalho
header = ctk.CTkFrame(main_area, height=50, corner_radius=0)
header.pack(side="top", fill="x")
ctk.CTkLabel(header, text="🔔 LembreJá", font=("Segoe UI", 20, "bold")).pack(
    side="left", padx=20, pady=15
)
ctk.CTkButton(header, text="⚙️", width=40).pack(side="right", padx=20, pady=15)
ctk.CTkButton(header, text="🌙", width=40).pack(side="right")

# Container Principal de Conteúdo
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
    else:
        ctk.CTkLabel(
            content,
            text=f"📂 Aba '{nome_aba.upper()}' (Estrutura modular pronta)",
            font=("Segoe UI", 18),
        ).pack(pady=50)


def carregar_tela_categorias():
    """Busca as categorias no banco e renderiza a interface visual com botões de ação."""
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

        # Barra lateral colorida
        barra_cor = ctk.CTkFrame(card, width=12, fg_color=cat["cor"], corner_radius=0)
        barra_cor.pack(side="left", fill="y")

        lbl_nome = ctk.CTkLabel(
            card, text=cat["nome"], font=("Segoe UI", 16, "bold")
        )
        lbl_nome.pack(side="left", padx=20, pady=15)

        # Frame de ações à direita (Contador + Botões)
        frame_direita = ctk.CTkFrame(card, fg_color="transparent")
        frame_direita.pack(side="right", padx=15)

        lbl_contador = ctk.CTkLabel(
            frame_direita,
            text=f"⏰ {total_alarmes} vinculados",
            font=("Segoe UI", 13),
            text_color="#888888",
        )
        lbl_contador.pack(side="left", padx=(0, 15))

        # Botão de Editar
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

        # Botão de Excluir
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
    """Abre o modal unificado para criar ou editar categorias."""
    janela_pop = ctk.CTkToplevel(app)
    
    # Define o título dinamicamente com base na ação
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

    # Campo Nome
    ctk.CTkLabel(
        janela_pop, text="Nome da Categoria:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(20, 5))

    txt_nome = ctk.CTkEntry(
        janela_pop, width=360, placeholder_text="Ex: Finanças, Saúde, Academia..."
    )
    txt_nome.pack(padx=20, pady=5)

    # Seleção de Cor
    ctk.CTkLabel(
        janela_pop, text="Selecione uma Cor:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(15, 5))

    combo_cores = ctk.CTkComboBox(
        janela_pop, width=360, values=list(opcoes_cores.keys()), state="readonly"
    )
    combo_cores.set("🔴 Vermelho")
    combo_cores.pack(padx=20, pady=5)

    # Preenchimento automático caso esteja em MODO EDIÇÃO
    if categoria_para_editar:
        txt_nome.insert(0, categoria_para_editar["nome"])
        # Mapeia o valor Hexadecimal de volta para o texto amigável do combobox
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
            # Chama atualização no banco
            db.atualizar_categoria(categoria_para_editar["id"], nome, cor)
        else:
            # Cria uma nova
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
    """Exibe uma mensagem detalhada antes de apagar a categoria."""
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


def criar_botao_menu(texto, comando_aba):
    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        height=45,
        anchor="w",
        fg_color="transparent",
        text_color="#a0a0a0",
        hover_color="#2b2b2b",
        font=("Segoe UI", 13, "bold"),
        command=lambda: selecionar_aba(comando_aba),
    )
    botao.pack(fill="x", padx=15, pady=5)
    return botao


botoes_menu["alarmes"] = criar_botao_menu("⏰ Alarmes", "alarmes")
botoes_menu["calendario"] = criar_botao_menu("📅 Calendário", "calendario")
botoes_menu["categorias"] = criar_botao_menu("📂 Categorias", "categorias")
botoes_menu["estatisticas"] = criar_botao_menu("📊 Estatísticas", "estatisticas")
botoes_menu["configuracoes"] = criar_botao_menu("⚙️ Configurações", "configuracoes")

selecionar_aba("alarmes")

threading.Thread(
    target=eng.verificar_alarmes_loop,
    args=(app, recarregar_interface_cards),
    daemon=True,
).start()

app.mainloop()