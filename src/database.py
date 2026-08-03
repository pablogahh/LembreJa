import json
import os
import time
from datetime import datetime

ARQUIVO_ALARMES = "data/alarmes.json"
ARQUIVO_HISTORICO = "data/historico.json"
ARQUIVO_CATEGORIAS = "data/categorias.json"

if not os.path.exists("data"):
    os.makedirs("data")

def carregar_alarmes():
    if not os.path.exists(ARQUIVO_ALARMES):
        return []
    try:
        with open(ARQUIVO_ALARMES, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_alarmes(alarmes):
    with open(ARQUIVO_ALARMES, "w", encoding="utf-8") as arquivo:
        json.dump(alarmes, arquivo, indent=4, ensure_ascii=False)


def adicionar_alarme(titulo, horario, dias_semana=None, categoria_id="4", ativo=True):
    alarmes = carregar_alarmes()  # Corrigido: adicionados parênteses

    novo_alarme = {
        "id": str(int(time.time() * 1000)),
        "titulo": titulo,
        "horario": horario,
        "dias_semana": dias_semana or [],
        "categoria_id": categoria_id,
        "ativo": ativo,
    }

    alarmes.append(novo_alarme)
    salvar_alarmes(alarmes)
    return novo_alarme


def arquivar_no_historico(alarme):
    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
                historico = json.load(arquivo)
        except json.JSONDecodeError:
            historico = []

    alarme["arquivado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append(alarme)

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

def inicializar_categorias():
    if not os.path.exists(ARQUIVO_CATEGORIAS):
        categorias_padrao = [
            {"id": "1", "nome": "Trabalho", "cor": "#FF5555"},  # Vermelho pastel
            {"id": "2", "nome": "Estudos", "cor": "#50FA7B"},   # Verde pastel
            {"id": "3", "nome": "Pessoal", "cor": "#8BE9FD"},   # Ciano/Azul
            {"id": "4", "nome": "Geral", "cor": "#BD93F9"},     # Roxo/Lilás
        ]
        salvar_categorias(categorias_padrao)


def carregar_categorias():
    inicializar_categorias()
    if not os.path.exists(ARQUIVO_CATEGORIAS):
        return []
    try:
        with open(ARQUIVO_CATEGORIAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_categorias(categorias):
    with open(ARQUIVO_CATEGORIAS, "w", encoding="utf-8") as arquivo:
        json.dump(categorias, arquivo, indent=4, ensure_ascii=False)


def criar_categorias(nome, cor):
    categorias = carregar_categorias()

    nova_cat = {
        "id": str(int(time.time() * 1000)),
        "nome": nome,
        "cor": cor,
    }
    categorias.append(nova_cat)
    salvar_categorias(categorias)
    return nova_cat


def atualizar_categoria(categoria_id, novo_nome, nova_cor):
    categorias = carregar_categorias()
    for cat in categorias:
        if cat["id"] == str(categoria_id):
            cat["nome"] = novo_nome
            cat["cor"] = nova_cor
            break
    salvar_categorias(categorias)


def deletar_categoria(categoria_id):
    categorias = carregar_categorias()
    categorias = [c for c in categorias if c["id"] != str(categoria_id)]
    salvar_categorias(categorias)


def obter_categoria_por_id(categoria_id):
    categorias = carregar_categorias()
    for cat in categorias:
        if str(cat.get("id")) == str(categoria_id):
            return cat
    return {"id": "0", "nome": "Geral", "cor": "#BD93F9"}


def obter_alarmes_por_categoria(categoria_id):
    alarmes = carregar_alarmes()
    return [a for a in alarmes if str(a.get("categoria_id")) == str(categoria_id)]

def obter_estatisticas():
    alarmes = carregar_alarmes()
    categorias = carregar_categorias()
    historico = []

    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except json.JSONDecodeError:
            historico = []

    total_alarmes = len(alarmes)
    total_historico = len(historico)
    disparados = sum(1 for a in alarmes if a.get("disparado", False))
    ativos = total_alarmes - disparados

    # Contagem por Categoria
    contagem_categorias = {}
    for cat in categorias:
        cat_id = str(cat["id"])
        qtd = sum(1 for a in alarmes if str(a.get("categoria_id")) == cat_id)
        contagem_categorias[cat["nome"]] = {
            "qtd": qtd,
            "cor": cat["cor"],
            "porcentagem": (qtd / total_alarmes * 100) if total_alarmes > 0 else 0
        }

    # Categoria mais popular
    cat_mais_popular = "Nenhuma"
    max_qtd = 0
    for nome, dados in contagem_categorias.items():
        if dados["qtd"] > max_qtd:
            max_qtd = dados["qtd"]
            cat_mais_popular = nome

    return {
        "total_alarmes": total_alarmes,
        "ativos": ativos,
        "disparados": disparados,
        "historico": total_historico,
        "cat_mais_popular": cat_mais_popular,
        "detalhes_categorias": contagem_categorias
    }