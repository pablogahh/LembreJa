# LembreJá - Gerenciador Inteligente de Alarmes e Lembretes
> Aplicação desktop desenvolvida em Python utilizando CustomTkinter para gerenciamento de alarmes, lembretes e produtividade. O projeto foi criado com foco no aprendizado de arquitetura de software, modularização e desenvolvimento de interfaces gráficas.

---

## Sobre o Projeto

O **LembreJá** é uma ferramenta desenvolvida em Python focada na gestão eficiente de tarefas e lembretes pessoais.

Iniciado como um projeto simples de estudo, o software passou por um processo completo de **refatoração e evolução arquitetural**, saindo de um script único para uma aplicação **modularizada com separação de responsabilidades**, garantindo um código limpo, testável e de fácil manutenção.

---

## Evolução e Arquitetura

O projeto evoluiu ao longo de três versões.
As versões anteriores permanecem disponíveis na pasta legacy para demonstrar a evolução da arquitetura e das boas práticas aplicadas durante o desenvolvimento:

* **`legacy/` (Versões Anteriores):** Contém os scripts iniciais em arquivo único (`v1` e `v2`), desenvolvidos para consolidar conceitos fundamentais de sintaxe, estruturas de dados e manipulação básica de arquivos.
* **`src/` (Versão Atual - LembreJá):** Arquitetura moderna e organizada em módulos independentes:
  * `app.py`: Ponto de entrada e fluxo principal da aplicação.
  * `components.py`: Componentes de interface de usuário e formatação do terminal.
  * `database.py`: Camada de persistência e manipulação dos dados.
  * `engine.py`: Regras de negócio e lógica das tarefas.

---

## Funcionalidades

- [x] **Gerenciamento de alarmes e lembretes:** Criação, edição e exclusão de lembretes com data, horário e descrição.
- [x] **Categorias personalizadas:** Organização dos lembretes por categorias para facilitar o gerenciamento.
- [x] **Dashboard de estatísticas:** Visualização de informações e indicadores sobre os lembretes cadastrados.
- [x] **Calendário integrado:** Consulta rápida dos lembretes programados por data.
- [x] **Histórico de atividades:** Registro automático dos lembretes concluídos para acompanhamento.
- [x] **Configurações do aplicativo:** Personalização de preferências e comportamento da aplicação.
- [x] **Tema Claro e Escuro:** Alternância entre modos de aparência para melhor experiência de uso.
- [x] **Validação inteligente de dados:** Verificação automática de datas e horários durante o cadastro.
- [x] **Processamento em segundo plano:** Monitoramento contínuo dos alarmes sem interromper a interface do usuário.
- [x] **Persistência de dados:** Armazenamento local das informações, preservando todos os dados entre as execuções do sistema.

---

## Tecnologias e Ferramentas

### Linguagens
- **Python 3.x**

### Interface Gráfica
- **CustomTkinter** – Desenvolvimento da interface desktop moderna.

### Persistência de Dados
- **JSON** – Armazenamento local das informações da aplicação.

### Bibliotecas da Linguagem
- **threading** – Processamento em segundo plano para monitoramento dos alarmes.
- **datetime** – Manipulação e validação de datas e horários.
- **os** – Gerenciamento de arquivos e diretórios.

### Controle de Versão
- **Git**
- **GitHub**

### Ambiente de Desenvolvimento
- **Visual Studio Code (VS Code)**

---

## Como Executar o Projeto

### Pré-requisitos

Antes de iniciar, certifique-se de possuir os seguintes requisitos:

- **Python 3.10 ou superior**
- **Git** instalado na máquina

### Instalação

1. Clone este repositório:

```bash
git clone https://github.com/pablogahh/LembreJa.git
```

2. Acesse o diretório do projeto:

```bash
cd LembreJa
```

3. (Opcional) Crie e ative um ambiente virtual:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute a aplicação:

```bash
python main.py
```

> **Observação:** Na primeira execução, o aplicativo criará automaticamente os arquivos e diretórios necessários para armazenar os dados do usuário.
