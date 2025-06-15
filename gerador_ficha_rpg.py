import streamlit as st
import google.generativeai as genai
import fitz
import os
import re

if "API_KEY" not in st.secrets:
    st.error("API_KEY não encontrada nos segredos do Streamlit. Adicione-a em .streamlit/secrets.toml")
    st.stop()

api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

PDF_TEMPLATE_PATH = "ficha_personagem_template.pdf"

def gerar_resposta_gemini(prompt):
    """Gera conteúdo usando a API do Gemini."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erro ao chamar a API do Gemini: {str(e)}")
        return None

def parse_character_data(text):
    """
    Analisa o texto gerado pelo Gemini e extrai os dados do personagem para um dicionário.
    Esta função usa expressões regulares para encontrar padrões 'Chave: Valor'.
    """
    data = {}
    pattern = re.compile(r"^\s*\*\*\s*(.*?)\s*\*\*\s*:\s*(.*?)\s*$", re.MULTILINE | re.IGNORECASE)
    
    simple_pattern = re.compile(r"^\s*([^:\n]+?)\s*:\s*(.*?)\s*$", re.MULTILINE)

    key_normalization = {
        "nome": "Nome",
        "raça": "Raça",
        "classe": "Classe",
        "background": "Antecedente",
        "alinhamento moral": "Tendência",
        "level": "Nível",
        "nível": "Nível",
        "gênero": "Gênero",
        "idade": "Idade",
        "força": "Força",
        "força bonus": "Força Bonus",
        "destreza": "Destreza",
        "destreza bonus": "Destreza Bonus",
        "constituição": "Constituição",
        "constituição bonus": "Constituição Bonus",
        "inteligência": "Inteligência",
        "inteligência bonus": "Inteligência Bonus",
        "sabedoria": "Sabedoria",
        "sabedoria bonus": "Sabedoria Bonus",
        "carisma": "Carisma",
        "carisma bonus": "Carisma Bonus",
        "bonus de inspiracão": "Bonus de Inspiracão",
        "bonus de proficiência": "Bonus de Proficiência",
        "força resistencia": "Força resistencia",
        "destreza resistencia": "Destreza resistencia",
        "constituição resistencia": "Constituição resistencia",
        "inteligência resistencia": "Inteligência resistencia",
        "sabedoria resistencia": "Sabedoria resistencia",
        "carisma resistencia": "Carisma resistencia",
        "pontos de vida": "PV Totais",
        "classe de armadura": "Classe de Armadura",
        "iniciativa": "Iniciativa",
        "deslocamento": "Deslocamento",
        "traços de personalidade": "Traços de Personalidade",
        "ideais": "Ideais",
        "vínculos": "Ligacões",
        "fraquezas": "Defeitos",
        "equipamentos": "Equipamentos"
    }
    
    lines = text.split('\n')
    current_section = ""
    for line in lines:
        match = simple_pattern.match(line)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            
            normalized_key = key_normalization.get(key)
            if normalized_key:
                value = re.sub(r'\s*\(\s*[+-]?\d+\s*\)\s*$', '', value)
                data[normalized_key] = value
            
    return data


def preencher_pdf(character_data, template_path):
    """
    Preenche um formulário PDF com os dados do personagem.

    Args:
        character_data (dict): Dicionário com os dados do personagem.
        template_path (str): Caminho para o arquivo PDF template.

    Returns:
        str: Caminho para o arquivo PDF preenchido.
    """
    if not os.path.exists(template_path):
        st.error(f"Arquivo de template não encontrado em: {template_path}")
        return None

    pdf_field_map = {
        "Nome": "CharacterName",
        "Classe": "ClassLevel",
        "Antecedente": "Background",
        "Raça": "Race ",
        "Tendência": "Alignment",
        "Nível": "ClassLevel",
        "Bonus de Inspiracão": "Inspiration",
        "Bonus de Proficiência": "ProfBonus",
        "Força": "STR",
        "Força Bonus": "STRmod",
        "Destreza": "DEX",
        "Destreza Bonus": "DEXmod ",
        "Constituição": "CON",
        "Constituição Bonus": "CONmod",
        "Inteligência": "INT",
        "Inteligência Bonus": "INTmod",
        "Sabedoria": "WIS",
        "Sabedoria Bonus": "WISmod",
        "Carisma": "CHA",
        "Carisma Bonus": "CHamod",
        "PV Totais": "HDTotal",
        "Classe de Armadura": "AC",
        "Iniciativa": "Initiative",
        "Deslocamento": "Speed",
        "Traços de Personalidade": "PersonalityTraits ",
        "Ideais": "Ideals",
        "Ligacões": "Bonds",
        "Defeitos": "Flaws",
        "Equipamentos": "Equipment",

        "Força_res": "ST Strength",
        "Destreza_res": "ST Dexterity",
        "Constituição_res": "ST Constitution",
        "Inteligência_res": "ST Intelligence",
        "Sabedoria_res": "ST Wisdom",
        "Carisma_res": "ST Charisma",
    }

    doc = fitz.open(template_path)
    
    for page in doc:
        for field in page.widgets():
            field_name = field.field_name
            for data_key, pdf_key in pdf_field_map.items():
                if pdf_key == field_name:
                    value_to_fill = character_data.get(data_key, "")
                    
                    field.field_value = str(value_to_fill)
                    field.update()
                    break

    os.makedirs("temp", exist_ok=True)
    output_path = os.path.join("temp", "ficha_preenchida.pdf")
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()
    
    return output_path

# Options
genders_options = ["Masculino", "Feminino", "Não binário", "Outro"]
races_options = ["Anão", "Elfo", "Halfling", "Humano", "Draconato", "Gnomo", "Meio-Elfo", "Meio-Orc", "Tiefling"]
subraces_options = {
    "Anão": ["Anão da Colina", "Anão da Montanha"],
    "Elfo": ["Alto Elfo", "Elfo da Floresta", "Elfo Negro (Drow)"],
    "Halfling": ["Halfling Pés-Leves", "Halfling Robusto"],
    "Humano": [],
    "Draconato": [],
    "Gnomo": ["Gnomo da Floresta", "Gnomo das Rochas"],
    "Meio-Elfo": [],
    "Meio-Orc": [],
    "Tiefling": []
}
alignment_options = ["Bom e leal", "Bom e neutro", "Bom e caótico", "Neutro e leal", "Verdadeiramente neutro",
                     "Neutro e caótico", "Mau e leal", "Mau e neutro", "Mau e caótico"]
attack_options = ["Físico", "Magia"]
style_options = ["Corpo a corpo", "Distância", "Versátil"]
complexity_options = ["Simples", "Moderada", "Complexa"]

st.set_page_config(page_title="Gerador de Ficha de D&D", page_icon="🎲", layout="wide")

st.markdown("<h1 style='text-align: center;'>Gerador de Personagem de D&D</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Preencha o formulário para que a IA crie uma ficha de personagem completa para você, pronta para baixar em PDF!</p>", unsafe_allow_html=True)


if 'character_generated' not in st.session_state:
    st.session_state.character_generated = False
    st.session_state.generated_response = ""
    st.session_state.form_values = {
        "nome": "", "genero": "Homem", "idade": 25, "role": "Lutador", 
        "alignment": "Bom e leal", "style": "Armas", "background": "Soldado",
        "motivation": "Proteger os inocentes", "skill": "Estrategista em combate",
        "complexity": "Simples", "traits": "Corajoso e um pouco teimoso", 
        "unique_feature_choice": "Não", "unique_feature": ""
    }

col_form, col_ficha = st.columns([1, 2])

with col_form:
    st.markdown("## 🎲 Crie seu Herói")
    with st.form(key="character_form"):
        form_data = st.session_state.form_values

        nome = st.text_input("Nome do personagem:", value=form_data["nome"])
        genero = st.selectbox("Gênero:", genders_options, index=0)
        race = st.selectbox("Raça:", races_options, index=1)
        subrace = None
        if(subraces_options[race]):
            subrace = st.selectbox("Escolha uma Sub-Raça de " + race, subraces_options[race], index=0)
            
        idade = st.number_input("Idade:", min_value=1, value=form_data["idade"])
        role = st.text_input("Papel no grupo (ex: suporte, tanque, dano):", value=form_data["role"])
        alignment = st.selectbox("Tendência (Alinhamento):", alignment_options, index=0)
        attack = st.selectbox("Como é o tipo de habilidade do seu personagem? Ele utiliza meios físicos (armas, flechas, punhos) ou magia?", attack_options, index=0)
        style = st.selectbox("Estilo de combate:", style_options, index=0)
        background = st.text_input("Origem (ex: nobre, artesão, eremita):", value=form_data["background"])
        motivation = st.text_input("Motivação (ex: vingança, poder):", value=form_data["motivation"])
        skill = st.text_input("Maior Habilidade (ex: furtividade, persuasão):", value=form_data["skill"])
        complexity = st.selectbox("Complexidade de jogabilidade:", complexity_options, index=0)
        traits = st.text_input("Traço de personalidade notável:", value=form_data["traits"])
        unique_feature_choice = st.radio("Adicionar característica única/misteriosa?", ("Não", "Sim"), index=0)
        unique_feature = st.text_input("Qual característica?", value=form_data["unique_feature"]) if unique_feature_choice == "Sim" else ""
        
        submit_button = st.form_submit_button(label="🐉 Gerar Ficha do Personagem")

if submit_button:
    with st.spinner("A IA está forjando seu personagem..."):
        st.session_state.form_values = {
            "nome": nome, "raca": race, "genero": genero, "idade": idade, "role": role, "alignment": alignment, 
            "style": style, "background": background, "motivation": motivation, "skill": skill,
            "complexity": complexity, "traits": traits, "unique_feature_choice": unique_feature_choice,
            "unique_feature": unique_feature
        }
        
        prompt = f"""
        Crie uma ficha de personagem de Dungeons & Dragons completa, nível 1, com base nas seguintes informações.
        Formate a resposta com 'Chave: Valor' para cada item.

        **Informações Gerais**:
        Nome: {nome}
        Raça: {race}
        Gênero: {genero}
        Idade: {idade}
        Papel Desejado: {role}
        Alinhamento Moral: {alignment}
        Estilo de Combate: {style}
        Origem: {background}
        Motivação: {motivation}
        Maior Habilidade: {skill}
        Complexidade de Jogo: {complexity}
        Traços de Personalidade: {traits}
        {'Característica Única: ' + unique_feature if unique_feature else ''}

        **Estrutura da Ficha (preencha com valores apropriados):**
        Nome: {nome}
        Raça: [Escolha uma raça que combine com as informações]
        Classe: [Escolha uma classe que combine com as informações]
        Background: {background}
        Alinhamento Moral: {alignment}
        Nível: 1
        Gênero: {genero}
        Idade: {idade}
        
        **Atributos (gere valores de 8 a 18 e calcule o bônus):**
        Força: [valor]
        Força Bonus: [bônus de força]
        Destreza: [valor]
        Destreza Bonus: [bônus de Destreza]
        Constituição: [valor]
        Constituição Bonus: [bônus de Constituição]
        Inteligência: [valor]
        Inteligência Bonus: [bônus de Inteligência]
        Sabedoria: [valor]
        Sabedoria Bonus: [bônus de Sabedoria]
        Carisma: [valor]
        Carisma Bonus: [bônus de Carisma]

        Bonus de Inspiracão: [valor]
        Bonus de Proficiência: [valor]
        
        Força resistencia: [valor],
        Destreza resistencia: [valor],
        Constituição resistencia: [valor],
        Inteligência resistencia: [valor],
        Sabedoria resistencia: [valor],
        Carisma resistencia: [valor],

        **Combate:**
        Classe de Armadura: [valor numérico simples]
        Iniciativa: [bônus de Destreza]
        Deslocamento: [valor m]
        Pontos de Vida: [valor total (valor + valor com base na constituição)]
        
        **Personalidade:**
        Traços de Personalidade: {traits}
        Ideais: [Gere um ideal com base no alinhamento e background resumido em 3 ou 4 palavras]
        Ligacões: [Gere um vínculo com base na motivação resumido em 3 ou 4 palavras]
        Fraquezas: [Gere uma fraqueza que crie roleplay interessante resumido em 3 ou 4 palavras]

        **Equipamentos:**
        Equipamentos: [Liste os equipamentos iniciais da classe e background em texto simples separados por quebra de linha]
        """
        
        generated_text = gerar_resposta_gemini(prompt)
        
        if generated_text:
            st.session_state.generated_response = generated_text
            st.session_state.character_generated = True
        else:
            st.session_state.character_generated = False
            st.error("Falha ao gerar o personagem. Tente novamente.")


with col_ficha:
    st.markdown("## 📜 Ficha Gerada")
    if st.session_state.character_generated:
        texto_gerado = st.session_state.generated_response

        dados_personagem = parse_character_data(texto_gerado)

        caminho_pdf_preenchido = preencher_pdf(dados_personagem, PDF_TEMPLATE_PATH)
        
        if caminho_pdf_preenchido:
            with open(caminho_pdf_preenchido, "rb") as file:
                st.download_button(
                    label="📄 Baixar Ficha em PDF",
                    data=file,
                    file_name=f"ficha_{dados_personagem.get('Nome', 'personagem').replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
        
        st.write(texto_gerado)
            
    else:
        st.info("Preencha o formulário à esquerda e clique em 'Gerar Ficha do Personagem' para criar sua ficha.")