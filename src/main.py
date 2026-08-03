import customtkinter as ctk
import database as db
import engine as eng
import formatters as fmt

import components.components as comp
from components.sidebar import SidebarMenu

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("LembreJá")
app.geometry("1200x700")

# Menu Lateral (Fixo e limpo dos erros de 'self')
sidebar = ctk.CTkFrame(app, width=250, corner_radius=0)
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="Menu", font=("Segoe UI", 22, "bold")).pack(pady=(30, 20))

# Área Principal (Onde fica o cabeçalho e os cartões)
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

# Container Principal de Conteúdo (Scrollable)
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
    """Busca as categorias no banco e renderiza a interface visual para o usuário."""
    # 1. Limpeza de segurança (Garante que a tela comece totalmente em branco)
    for widget in content.winfo_children():
        widget.destroy()

    # 2. Cabeçalho interno da aba
    lbl_titulo = ctk.CTkLabel(
        content, 
        text="📁 Minhas Categorias", 
        font=("Segoe UI", 24, "bold")
    )
    lbl_titulo.pack(anchor="nw", pady=(10, 20))

    # 3. Botão para criar nova categoria futuramente
    btn_nova_cat = ctk.CTkButton(
        content,
        text="➕ Nova Categoria",
        height=40,
        font=("Segoe UI", 13, "bold"),
        command=abrir_janela_nova_categoria
    )
    btn_nova_cat.pack(anchor="nw", pady=(0, 20))

    # 4. Painel de Exibição das Categorias (Lista)
    frame_lista = ctk.CTkFrame(content, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)

    # 5. O Elo com o Database: Buscamos os dados salvos no HD
    lista_categorias = db.carregar_categorias()
    lista_alarmes = db.carregar_alarmes()

    # 6. Laço de repetição (Loop) para desenhar cada categoria na tela
    for cat in lista_categorias:
        # Lógica de negócio: Conta quantos alarmes usam o ID desta categoria
        total_alarmes = sum(1 for alarme in lista_alarmes if alarme.get("categoria_id") == cat["id"])

        # Criamos o container/card visual para a categoria
        card = ctk.CTkFrame(frame_lista, height=60, corner_radius=8)
        card.pack(fill="x", pady=6)
        card.pack_propagate(False) # Proteção de tamanho fixa

        # Detalhe visual: Uma barrinha colorida na esquerda com a cor da categoria
        barra_cor = ctk.CTkFrame(card, width=12, fg_color=cat["cor"], corner_radius=0)
        barra_cor.pack(side="left", fill="y")

        # Texto com o nome da categoria
        lbl_nome = ctk.CTkLabel(
            card, 
            text=cat["nome"], 
            font=("Segoe UI", 16, "bold")
        )
        lbl_nome.pack(side="left", padx=20, pady=15)

        # Contador de alarmes vinculados no canto direito
        lbl_contador = ctk.CTkLabel(
            card, 
            text=f"⏰ {total_alarmes} vinculados", 
            font=("Segoe UI", 13),
            text_color="#888888"
        )
        lbl_contador.pack(side="right", padx=20, pady=15)

def abrir_janela_nova_categoria():
    """Abre uma janela pop-up para o usuário cadastrar uma nova categoria."""
    # Cria uma janela flutuante (Toplevel)
    janela_pop = ctk.CTkToplevel(app)
    janela_pop.title("📁 Nova Categoria")
    janela_pop.geometry("400x250")
    janela_pop.resizable(False, False)
    
    # Garante que o usuário foque apenas nessa janela enquanto ela estiver aberta
    janela_pop.grab_set()
    janela_pop.attributes("-topmost", True)

    # Label de instrução
    ctk.CTkLabel(
        janela_pop, text="Nome da Categoria:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(20, 5))

    # Campo de texto (Entry) para o nome
    txt_nome = ctk.CTkEntry(
        janela_pop, width=360, placeholder_text="Ex: Finanças, Saúde, Academia..."
    )
    txt_nome.pack(padx=20, pady=5)

    # Label para a seleção de cor
    ctk.CTkLabel(
        janela_pop, text="Selecione uma Cor:", font=("Segoe UI", 14, "bold")
    ).pack(anchor="nw", padx=20, pady=(15, 5))

    # Caixa de seleção (ComboBox) com opções de cores em formato amigável
    opcoes_cores = {
        "🔴 Vermelho": "#FF5555",
        "🟢 Verde": "#50FA7B",
        "🔵 Azul": "#8BE9FD",
        "🟡 Amarelo": "#F1FA8C",
        "🟣 Roxo": "#BD93F9",
        "🟠 Laranja": "#FFB86C",
        "⚪ Cinza": "#6272A4"
    }
    
    combo_cores = ctk.CTkComboBox(
        janela_pop, width=360, values=list(opcoes_cores.keys()), state="readonly"
    )
    combo_cores.set("🔴 Vermelho")  # Valor padrão inicial
    combo_cores.pack(padx=20, pady=5)

    # Função interna disparada ao clicar no botão "Salvar"
    def salvar_clique():
        nome = txt_nome.get().strip()
        cor_selecionada_texto = combo_cores.get()
        cor = opcoes_cores[cor_selecionada_texto] # Traduz o nome para o código Hexadecimal (#FF5555...)

        # Validação simples de dados
        if not nome:
            from tkinter import messagebox
            messagebox.showwarning("⚠️ Ops!", "Por favor, digite o nome da categoria.", parent=janela_pop)
            return

        # Chamando a função do database.py para gravar no arquivo JSON
        db.criar_categorias(nome, cor)

        # Fecha a janela pop-up
        janela_pop.destroy()

        # Recarrega a tela de categorias para o novo card aparecer instantaneamente!
        carregar_tela_categorias()

    # Botão de Ação para Salvar
    btn_salvar = ctk.CTkButton(
        janela_pop,
        text="💾 Salvar Categoria",
        height=35,
        font=("Segoe UI", 13, "bold"),
        command=salvar_clique
    )
    btn_salvar.pack(pady=25)

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


# Inicialização dos botões do Menu Lateral
botoes_menu["alarmes"] = criar_botao_menu("⏰ Alarmes", "alarmes")
botoes_menu["calendario"] = criar_botao_menu("📅 Calendário", "calendario")
botoes_menu["categorias"] = criar_botao_menu("📂 Categorias", "categorias")
botoes_menu["estatisticas"] = criar_botao_menu("📊 Estatísticas", "estatisticas")
botoes_menu["configuracoes"] = criar_botao_menu("⚙️ Configurações", "configuracoes")

# Força inicialização na aba padrão
selecionar_aba("alarmes")

# Dispara o motor em uma Thread isolada para não congelar o mouse
import threading

threading.Thread(
    target=eng.verificar_alarmes_loop,
    args=(app, recarregar_interface_cards),
    daemon=True,
).start()

app.mainloop()
