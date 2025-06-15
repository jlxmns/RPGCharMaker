# 🎲 Gerador de Ficha de Personagem de D&D com IA

Este projeto é uma aplicação web construída com Streamlit que utiliza o poder da API do Google Gemini para criar fichas de personagem de Dungeons & Dragons 5ª Edição de forma automática e personalizada.

A aplicação pega as informações fornecidas por você, gera uma ficha completa e a preenche em um PDF, pronto para ser baixado e usado na sua próxima aventura!

# ✨ Funcionalidades
**Interface Intuitiva:** Um formulário simples e direto para você definir as principais características do seu herói.

**Geração com IA:** Utiliza o modelo gemini-2.0-flash da Google para criar detalhes coesos e criativos para o personagem, incluindo atributos, habilidades e personalidade.

**Customização Detalhada:** Escolha nome, raça, alinhamento, motivação, estilo de combate e muito mais.

**Preenchimento Automático de PDF:** Os dados gerados pela IA são automaticamente inseridos em uma ficha de personagem padrão de D&amp;D 5e.

**Download Instantâneo:** Baixe a ficha preenchida em formato PDF com um único clique.

# ⚙️ Como Funciona

O fluxo da aplicação é dividido em quatro etapas principais:

**Coleta de Dados:** O usuário preenche o formulário na interface web com as especificações do personagem desejado.

**Geração do Prompt:** A aplicação compila as respostas do formulário em um prompt detalhado e estruturado.

**Chamada à API Gemini:** O prompt é enviado para a API do Google Gemini, que gera uma resposta em texto contendo todos os dados da ficha do personagem no formato "Chave: Valor".

**Preenchimento do PDF:** O texto de resposta é analisado (parsed) e os dados extraídos são usados para preencher os campos de um template PDF (ficha_personagem_template.pdf) utilizando a biblioteca PyMuPDF (fitz).

**Exibição e Download:** A ficha gerada é exibida na tela e um botão de download para o PDF preenchido é disponibilizado.

# 🚀 Instalação e Execução Local

Para executar este projeto em sua máquina local, siga os passos abaixo.

Pré-requisitos:

**Python 3.8 ou superior**

**Uma chave de API do Google AI Studio**

**1. Clone o Repositório**
   
```bash
git clone https://github.com/jlxmns/RPGCharMaker
```

**2. Crie um Ambiente Virtual (Recomendado)**
   
```bash
# Windows
python -m venv streamlit_env
.\streamlit_env\Scripts\activate

# macOS / Linux
python3 -m venv streamlit_env
source streamlit_env/bin/activate
```

**3. Instale as Dependências**

Crie um arquivo requirements.txt com o seguinte conteúdo:

```plaintext
streamlit
google-generativeai
PyMuPDF
```

E então, instale as bibliotecas:
```bash
pip install -r requirements.txt
```

**4. Configure a Chave de API**

A aplicação utiliza o sistema de segredos do Streamlit para gerenciar a chave de API.

Crie uma pasta chamada .streamlit na raiz do seu projeto.

Dentro dela, crie um arquivo chamado secrets.toml.

Adicione sua chave de API ao arquivo da seguinte forma:

```Ini, TOML
# .streamlit/secrets.toml
API_KEY = "SUA_CHAVE_API_DO_GOOGLE_AQUI"
```


**5. Garanta o Template da Ficha**
   
Certifique-se de que o arquivo ficha_personagem_template.pdf está presente na raiz do projeto. Este arquivo é o modelo que será preenchido.

**6. Execute a Aplicação**
   
Salve o código fornecido em um arquivo (ex: app.py) e execute o seguinte comando no seu terminal:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

📂 Estrutura de Arquivos
A estrutura de pastas e arquivos do projeto deve ser a seguinte:
```
/seu-repositorio
|-- .streamlit/
|   |-- secrets.toml       # Armazena sua chave de API
|-- temp/
|   |-- (Pasta criada em tempo de execução para PDFs)
|-- app.py                 # O código principal da aplicação
|-- ficha_personagem_template.pdf # O template da ficha
|-- requirements.txt       # Lista de dependências Python
|-- README.md              # Este arquivo
```
🛠️ Tecnologias Utilizadas

Backend & Frontend: Streamlit

Inteligência Artificial: Google Gemini API

Manipulação de PDF: PyMuPDF (fitz)

Linguagem: Python
