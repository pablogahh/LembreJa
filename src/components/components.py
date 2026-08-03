import uuid
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar

import database as db
import formatters as fmt


def abrir_calendario(entry_target):
    janela_cal = ctk.CTkToplevel()
    janela_cal.title("Selecionar Data")
    janela_cal.geometry("300x260")
    janela_cal.grab_set()
    janela_cal.lift()

    cal = Calendar(
        janela_cal, selectmode="day", locale="pt_BR", date_pattern="dd/mm/yyyy"
    )
    cal.pack(pady=10, fill="both", expand=True)

    def confirmar_data():
        entry_target.delete(0, "end")
        entry_target.insert(0, cal.get_date())
        entry_target.configure(border_color="#2fa572")
        janela_cal.destroy()

    ctk.CTkButton(janela_cal, text="Confirmar Data", command=confirmar_data).pack(
        pady=5
    )


def abrir_janela_alarme(
    app, content_panel, recarregar_callback, alarme_para_editar=None, card_visual=None
):
    janela = ctk.CTkToplevel(app)
    janela.title("Novo Alarme" if not alarme_para_editar else "Editar Alarme")
    janela.geometry("400x580")
    janela.lift()
    janela.focus_force()
    janela.transient(app)
    janela.grab_set()

    ctk.CTkLabel(
        janela,
        text="Criar Novo Alarme" if not alarme_para_editar else "Editar Alarme",
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=20)

    entry_titulo = ctk.CTkEntry(janela, placeholder_text="Título do Alarme", width=350)
    entry_titulo.pack(pady=10)

    try:
        dados_categorias = db.carregar_categorias()
    except Exception:
        dados_categorias = ["Estudos", "Trabalho", "Pessoal", "Geral"]

    if not dados_categorias:
        dados_categorias = ["Estudos", "Trabalho", "Pessoal", "Geral"]

    nomes_categorias = []
    mapa_categorias = {}     
    mapa_ids_para_nomes = {} 

    for idx, cat in enumerate(dados_categorias):
        if isinstance(cat, dict):
            c_id = str(cat.get("id", idx))
            c_nome = f"{cat.get('icone', '')} {cat.get('nome', '')}".strip()
        else:
            c_id = str(cat)
            c_nome = str(cat)

        nomes_categorias.append(c_nome)
        mapa_categorias[c_nome] = c_id
        mapa_ids_para_nomes[c_id] = c_nome

    combo_categoria = ctk.CTkComboBox(
        janela,
        values=nomes_categorias,
        width=350,
    )
    combo_categoria.pack(pady=10)

    if nomes_categorias and not alarme_para_editar:
        combo_categoria.set(nomes_categorias[0])

    combo_prioridade = ctk.CTkComboBox(
        janela, values=["🟢 Baixa", "🟡 Média", "🔴 Alta"], width=350
    )
    combo_prioridade.pack(pady=10)

    frame_data = ctk.CTkFrame(janela, fg_color="transparent")
    frame_data.pack(pady=10)

    entry_data = ctk.CTkEntry(frame_data, placeholder_text="Data (DDMMYYYY)", width=295)
    entry_data.pack(side="left", padx=(0, 5))
    entry_data.bind(
        "<KeyRelease>", lambda event: fmt.aplicar_mascara_e_validar(entry_data, "data")
    )

    ctk.CTkButton(
        frame_data, text="📅", width=50, command=lambda: abrir_calendario(entry_data)
    ).pack(side="right")

    entry_horario = ctk.CTkEntry(janela, placeholder_text="Horário (HHMM)", width=350)
    entry_horario.pack(pady=10)
    entry_horario.bind(
        "<KeyRelease>",
        lambda event: fmt.aplicar_mascara_e_validar(entry_horario, "horario"),
    )

    descricao = ctk.CTkTextbox(janela, width=350, height=100)
    descricao.pack(pady=10)

    # Preenchimento em caso de Edição
    if alarme_para_editar:
        entry_titulo.insert(0, alarme_para_editar.get("titulo", ""))
        
        # Resolve a categoria do alarme (trata tanto se for ID quanto Nome)
        cat_salva = str(alarme_para_editar.get("categoria", ""))
        nome_cat_atual = mapa_ids_para_nomes.get(cat_salva, cat_salva)
        if nome_cat_atual in nomes_categorias:
            combo_categoria.set(nome_cat_atual)
        elif nomes_categorias:
            combo_categoria.set(nomes_categorias[0])

        combo_prioridade.set(alarme_para_editar.get("prioridade", "🟢 Baixa"))
        entry_data.insert(0, alarme_para_editar.get("data", ""))
        entry_horario.insert(0, alarme_para_editar.get("horario", ""))
        descricao.insert("1.0", alarme_para_editar.get("descricao", ""))

    def salvar_alarme():
        titulo_texto = entry_titulo.get().strip()
        data_texto = entry_data.get().strip()
        horario_texto = entry_horario.get().strip()
        
        # Pega a categoria selecionada no ComboBox
        categoria_selecionada = combo_categoria.get()

        if not titulo_texto or not data_texto or not horario_texto:
            messagebox.showwarning(
                "Campos Vazios", "Por favor, preencha todos os campos obrigatórios."
            )
            return

        try:
            datetime.strptime(data_texto, "%d/%m/%Y")
            datetime.strptime(horario_texto, "%H:%M")
        except ValueError:
            messagebox.showerror("Erro Cadastral", "Data ou Horário inválidos.")
            return

        if (
            datetime.strptime(f"{data_texto} {horario_texto}", "%d/%m/%Y %H:%M")
            < datetime.now()
            and not alarme_para_editar
        ):
            messagebox.showerror("Cronologia Inválida", "Não agende no passado.")
            return

        # Busca o ID ou Objeto correspondente ao nome selecionado no banco
        # (Se seu banco salvar por nome direto, converte ou busca no mapa)
        cat_id = mapa_categorias.get(categoria_selecionada, categoria_selecionada) if 'mapa_categorias' in locals() else categoria_selecionada

        alarmes = db.carregar_alarmes()

        dados_alarme = {
            "id": alarme_para_editar["id"] if alarme_para_editar else str(uuid.uuid4()),
            "titulo": titulo_texto,
            "categoria": categoria_selecionada,      # Para exibição direta do nome/texto
            "categoria_id": cat_id,                  # Importante: Mantém o ID para busca de cores/dados no DB
            "prioridade": combo_prioridade.get(),
            "data": data_texto,
            "horario": horario_texto,
            "descricao": descricao.get("1.0", "end").strip(),
            "disparado": alarme_para_editar.get("disparado", False) if alarme_para_editar else False,
        }

        if alarme_para_editar:
            for idx, a in enumerate(alarmes):
                if a["id"] == alarme_para_editar["id"]:
                    alarmes[idx] = dados_alarme
                    break
            if card_visual:
                card_visual.destroy()
        else:
            alarmes.append(dados_alarme)

        db.salvar_alarmes(alarmes)
        recarregar_callback()
        janela.destroy()

    ctk.CTkButton(
        janela, text="💾 Salvar Alarme", command=salvar_alarme, width=350
    ).pack(pady=15)

def criar_card_alarme(app, content_panel, alarme_dados, recarregar_callback):
    id_alarme = alarme_dados["id"]
    cor_prioridade = "#2fa572"
    if "Alta" in alarme_dados.get("prioridade", ""):
        cor_prioridade = "#c84343"
    elif "Média" in alarme_dados.get("prioridade", ""):
        cor_prioridade = "#d9a71a"

    # Tenta buscar os dados da categoria no banco (Cor/ID)
    categoria_id = alarme_dados.get("categoria_id") or alarme_dados.get("categoria", "Geral")
    
    try:
        categoria_info = db.obter_categoria_por_id(categoria_id)
        cor_categoria = categoria_info.get("cor", "#2fa572") if isinstance(categoria_info, dict) else "#2fa572"
    except Exception:
        cor_categoria = "#2fa572"  # Cor padrão verde caso não ache a ID

    cor_card = "#2b2b2b" if not alarme_dados.get("disparado") else "#1e1e1e"

    card = ctk.CTkFrame(
        content_panel,
        height=120,
        corner_radius=12,
        fg_color=cor_card,
        border_width=1,
        border_color="#3a3a3a",
    )
    card.pack(fill="x", pady=8, padx=5)
    card.pack_propagate(False)

    # Barrinha lateral esquerda com a cor real da Categoria
    barra_categoria = ctk.CTkFrame(card, width=6, fg_color=cor_categoria, corner_radius=0)
    barra_categoria.pack(side="left", fill="y")

    info_frame = ctk.CTkFrame(card, fg_color="transparent")
    info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=12)

    linha_titulo = ctk.CTkFrame(info_frame, fg_color="transparent")
    linha_titulo.pack(fill="x", anchor="w")

    texto_titulo = (
        alarme_dados["titulo"]
        if not alarme_dados.get("disparado")
        else f"{alarme_dados['titulo']} (Disparado ✔)"
    )
    ctk.CTkLabel(
        linha_titulo,
        text=texto_titulo,
        font=("Segoe UI", 16, "bold"),
        text_color="#ffffff" if not alarme_dados.get("disparado") else "#707070",
    ).pack(side="left")

    ctk.CTkLabel(
        linha_titulo,
        text=alarme_dados.get("prioridade", "BAIXA").upper(),
        font=("Segoe UI", 10, "bold"),
        text_color="#ffffff",
        fg_color=cor_prioridade if not alarme_dados.get("disparado") else "#404040",
        corner_radius=6,
        padx=8,
        pady=2,
    ).pack(side="left", padx=15)

    # Exibe exatamente o texto da categoria gravada no dicionário do alarme
    categoria_exibicao = alarme_dados.get("categoria", "Geral")

    ctk.CTkLabel(
        info_frame,
        text=f"📂 {categoria_exibicao}   •   📅 {alarme_dados['data']} às {alarme_dados['horario']}",
        font=("Segoe UI", 12),
        text_color="#a0a0a0",
    ).pack(anchor="w", pady=(6, 0))

    frame_acoes = ctk.CTkFrame(card, fg_color="transparent")
    frame_acoes.pack(side="right", fill="y", padx=20, pady=12)

    def acao_excluir():
        if messagebox.askyesno(
            "Confirmar Exclusão", f"Excluir '{alarme_dados['titulo']}'?"
        ):
            lista = [a for a in db.carregar_alarmes() if a["id"] != id_alarme]
            db.salvar_alarmes(lista)
            card.destroy()

    ctk.CTkButton(
        frame_acoes,
        text="✏️ Editar",
        width=75,
        height=28,
        command=lambda: abrir_janela_alarme(
            app, content_panel, recarregar_callback, alarme_dados, card
        ),
    ).pack(side="top", pady=4)

    ctk.CTkButton(
        frame_acoes,
        text="🗑️ Excluir",
        width=75,
        height=28,
        fg_color="#3a1a1a",
        hover_color="#c84343",
        text_color="#ff9999",
        command=acao_excluir,
    ).pack(side="top", pady=4)


def carregar_tela_calendario(app, content_panel):
    # Título da Aba
    ctk.CTkLabel(
        content_panel, text="📅 Agenda & Calendário", font=("Segoe UI", 22, "bold")
    ).pack(pady=(10, 20), anchor="w", padx=10)

    # Container para dividir o Calendário dos Lembretes
    split_container = ctk.CTkFrame(content_panel, fg_color="transparent")
    split_container.pack(fill="both", expand=True)

    # Frame Esquerdo: O Calendário
    frame_cal = ctk.CTkFrame(split_container, fg_color="#2b2b2b", corner_radius=12)
    frame_cal.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    frame_cal.pack_propagate(False)

    cal = Calendar(
        frame_cal,
        selectmode="day",
        locale="pt_BR",
        date_pattern="dd/mm/yyyy",
        background="#1f538d",
        foreground="white",
        headersbackground="#1e1e1e",
        headersforeground="white",
        selectbackground="#2fa572",
        normalbackground="#2b2b2b",
        normalforeground="white",
        weekendbackground="#3a3a3a",
        weekendforeground="white",
    )
    cal.pack(fill="both", expand=True, padx=5, pady=5)

    # Frame Direito: Lista de Compromissos do Dia
    frame_compromissos = ctk.CTkFrame(
        split_container, fg_color="#1e1e1e", corner_radius=12, width=400
    )
    frame_compromissos.pack(side="right", fill="both", expand=False, padx=10, pady=5)
    frame_compromissos.pack_propagate(False)

    lbl_data_selecionada = ctk.CTkLabel(
        frame_compromissos,
        text="Selecione um dia...",
        font=("Segoe UI", 14, "bold"),
        text_color="#2fa572",
    )
    lbl_data_selecionada.pack(pady=15)

    # Sub-container scrollable para os mini-cards de lembretes do dia
    lista_scroll = ctk.CTkScrollableFrame(frame_compromissos, fg_color="transparent")
    lista_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def atualizar_agenda_do_dia(event=None):
        data_selecionada = cal.get_date()
        lbl_data_selecionada.configure(text=f"Alarmes para: {data_selecionada}")

        # Limpa listagem anterior
        for widget in lista_scroll.winfo_children():
            widget.destroy()

        # Carrega os alarmes direto do banco de dados
        todos_alarmes = db.carregar_alarmes()
        alarmes_filtrados = [a for a in todos_alarmes if a.get("data") == data_selecionada]

        if not alarmes_filtrados:
            ctk.CTkLabel(
                lista_scroll,
                text="✨ Nenhum alarme para este dia!",
                font=("Segoe UI", 12),
                text_color="#707070",
            ).pack(pady=40)
            return

        # Cria mini-cards simplificados para a agenda lateral
        for alarme in alarmes_filtrados:
            cat_info = db.obter_categoria_por_id(alarme.get("categoria_id", "4"))

            mini_card = ctk.CTkFrame(
                lista_scroll, fg_color="#2b2b2b", height=60, corner_radius=8
            )
            mini_card.pack(fill="x", pady=4)
            mini_card.pack_propagate(False)

            # Usando a cor da própria categoria no detalhe lateral do mini-card!
            detalhe = ctk.CTkFrame(mini_card, width=5, fg_color=cat_info["cor"])
            detalhe.pack(side="left", fill="y")

            # Textos do mini-card
            texto_frame = ctk.CTkFrame(mini_card, fg_color="transparent")
            texto_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

            ctk.CTkLabel(
                texto_frame,
                text=alarme["titulo"],
                font=("Segoe UI", 13, "bold"),
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                texto_frame,
                text=f"📂 {cat_info['nome']}",
                font=("Segoe UI", 10),
                text_color="#a0a0a0",
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                mini_card,
                text=alarme["horario"],
                font=("Segoe UI", 14, "bold"),
                text_color="#a0a0a0",
            ).pack(side="right", padx=15)

    # Vincula o clique do calendário para atualizar a lista automaticamente
    cal.bind("<<CalendarSelected>>", atualizar_agenda_do_dia)

    # Executa uma vez no início para o dia atual já vir preenchido
    atualizar_agenda_do_dia()