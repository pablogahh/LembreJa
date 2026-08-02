import json
import os
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
            {"id": "1", "nome": "Trabalho", "cor": "#FF5555"},   # Vermelho pastel
            {"id": "2", "nome": "Estudos", "cor": "#50FA7B"},    # Verde pastel
            {"id": "3", "nome": "Pessoal", "cor": "#8BE9FD"},    # Ciano/Azul
            {"id": "4", "nome": "Geral", "cor": "#BD93F9"}       # Roxo/Lilás
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
        return[]
    
def salvar_categorias(categorias):
    with open(ARQUIVO_CATEGORIAS, "w", encoding="utf-8",) as arquivo:
        json.dump(categorias, arquivo, indent=4, ensure_ascii=False)

def criar_categorias(nome, cor):
    import time
    categorias = carregar_categorias()

    nova_cat = {
        "id": str(int(time.time() * 1000)),
        "nome": nome,
        "cor": cor
    }
    categorias.append(nova_cat)
    salvar_categorias(categorias)
    return nova_cat
