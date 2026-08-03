# LembreJá - Gerenciador de Lembretes (CLI)

> Aplicação em Python para criação, organização e persistência de lembretes diários executada via Linha de Comando (CLI).

---

## Sobre o Projeto

O **LembreJá** é uma ferramenta desenvolvida em Python focada na gestão eficiente de tarefas e lembretes pessoais diretamente pelo terminal. 

Iniciado como um projeto simples de estudo, o software passou por um processo completo de **refatoração e evolução arquitetural**, saindo de um script único para uma aplicação **modularizada com separação de responsabilidades**, garantindo um código limpo, testável e de fácil manutenção.

---

## Evolução e Arquitetura

O projeto reflete a maturidade no aprendizado de engenharia de software e está dividido em fases:

* **`legacy/` (Versões Anteriores):** Contém os scripts iniciais em arquivo único (`v1` e `v2`), desenvolvidos para consolidar conceitos fundamentais de sintaxe, estruturas de dados e manipulação básica de arquivos.
* **`src/` (Versão Atual - LembreJá):** Arquitetura moderna e organizada em módulos independentes:
  * `app.py`: Ponto de entrada e fluxo principal da aplicação.
  * `components.py`: Componentes de interface de usuário e formatação do terminal.
  * `database.py`: Camada de persistência e manipulação dos dados.
  * `engine.py`: Regras de negócio e lógica das tarefas.

---

## Funcionalidades

- [x] **Criar novos lembretes:** Adição rápida de tarefas com categorias e prazos.
- [x] **Listar lembretes:** Visualização organizada com status e formatação no terminal.
- [x] **Gerenciar status:** Marcar lembretes como concluídos ou pendentes.
- [x] **Remover lembretes:** Exclusão individual de itens da lista.
- [x] **Persistência de Dados:** Salvamento automático das informações para não perder dados ao fechar o terminal.

---

## Tecnologias e Ferramentas

* **Linguagem:** Python 3.x
* **Versionamento:** Git & GitHub
* **Ambiente de Desenvolvimento:** Visual Studio Code (VS Code)

---

## Como Executar o Projeto

### Pré-requisitos
* Ter o **Python 3.8+** instalado na máquina.

### Passo a passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/pablogahh/LembreJa.git](https://github.com/pablogahh/LembreJa.git)
