# Daily Cosmos

## 🌙 Projeto Flask: Arquitetura MVC
### Academic project to develop a city's planetarium schedule featuring astronomical events, using Python's Flask library.

Este projeto é uma aplicação web desenvolvida com Flask, utilizando uma arquitetura organizada baseada em MVC (Model-View-Controller), integrada a um banco de dados PostgreSQL via SQLAlchemy.

## 🔧 Tecnologias:
- Python 3.11+ 🐍

- Flask 🧩

- SQLAlchemy 🧬

- PostgreSQL 🗂️

- dotenv (para variáveis de ambiente) 📦

- Jinja2 🧵

- Bootstrap

- JavaScrip (para interações visuais)

- JSON

## 🔄 Organização em Camadas

- models/: representa a estrutura das tabelas do banco.

- controllers/: lógica de negócio e validações.

- routes/: define as rotas.

- database.py: instancia o SQLAlchemy, para evitar variáveis globais diretas no main.

- create_app(): padrão de fábrica para criação da aplicação Flask, usado para manter tudo encapsulado.


```
projeto/
│
├── main.py                # Arquivo principal de execução
├── .env                   # Variáveis de ambiente (NÃO versionar)
├── app/
│   ├── __init__.py        # Função create_app com configuração da aplicação
│   ├── auth               # Define load_user para lidar com autenticação de usuario
│   ├── instance.py        # Inicia instancias globais
│   ├── models/            # Modelos do banco de dados
│   ├── controllers/       # Lógica e validações da aplicação
│   ├── routes/            # Definição de rotas
│   ├── templates/         # Arquivos HTML com o front-end
│   ├── static/            # Elementos estáticos como img, icons, style etc.
```

## 🚀 Executando

1. Crie um ambiente virtual.

2. Instale as dependências com:
``` Bash
pip install -r requirements.txt
```

3. Crie um arquivo .env com suas variáveis de conexão.

4. Execute com:
``` Bash 
python main.py
```
















