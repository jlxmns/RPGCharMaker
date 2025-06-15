import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os

if "API_KEY" not in st.secrets:
    st.error("API_KEY not found in Streamlit secrets. Please add it to .streamlit/secrets.toml")
    st.stop() # Stop the app if API key is missing

api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def gerar_resposta_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"
    
def gerar_pdf(texto, nome_arquivo="ficha_personagem.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    try:
        for linha in texto.split("\n"):
            pdf.multi_cell(0, 10, linha.encode('latin-1', 'replace').decode('latin-1'))
    except Exception as e:
        st.error(f"Erro ao adicionar texto ao PDF: {e}")
        st.warning("Pode ser um problema de codificação de caracteres. Tentando continuar.")
        for linha in texto.split("\n"):
             pdf.multi_cell(0, 10, linha) # Fallback

    os.makedirs("temp", exist_ok=True)
    caminho_arquivo = os.path.join("temp", nome_arquivo)
    pdf.output(caminho_arquivo)
    return caminho_arquivo

genders = ["Homem", "Mulher", "Não binário", "Outro"]
alignment_options = ["Bom e leal", "Bom e neutro", "Bom e caótico", "Neutro e leal", "Verdadeiramente neutro",
                     "Neutro e caótico", "Mau e leal", "Mau e neutro", "Mau e caótico"]
style_options = ["Armas", "Magia", "Armas e Magia"]
experience_choices = ["Simples", "Moderada", "Complexa"]

st.set_page_config(
    page_title="Gerador de Personagem de RPG",
    page_icon="🚀",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>Gerador de Personagem de RPG</h1>", unsafe_allow_html=True)

if 'character_generated' not in st.session_state:
    st.session_state.character_generated = False
    st.session_state.generated_response = ""
    st.session_state.form_values = {
        "nome": "", "genero": "Homem", "idade": 22,
        "role": "", "alignment": "Bom e leal", "style": "Armas",
        "background": "", "motivation": "", "skill": "",
        "complexity": "Simples", "traits": "", "unique_feature_choice": "Não",
        "unique_feature": ""
    }

if not st.session_state.character_generated:
    col_esq, col_form, col_dir = st.columns([1, 2, 1])
    with col_form:
        st.markdown("<h2 style='text-align: center;'>🎲 Informações do Personagem</h2>", unsafe_allow_html=True)

        form_data = st.session_state.form_values

        nome = st.text_input("Qual o nome do personagem?", value=form_data["nome"], key="nome_initial")
        genero = st.selectbox("Qual o gênero do personagem?", genders, index=genders.index(form_data["genero"]), key="genero_initial")
        idade = st.number_input("Qual a idade do personagem?", min_value=22, value=form_data["idade"], key="idade_initial")

        role = st.text_input(
            "Qual tipo de papel você gostaria de desempenhar no grupo? Ex: lutador, suporte, furtivo, versátil, etc.", 
            value=form_data["role"], 
            key="role_initial"
        )

        alignment = st.selectbox(
            "Você diria que seu personagem é:", alignment_options, 
            index=alignment_options.index(form_data["alignment"]), 
            key="alignment_initial"
        )

        style = st.selectbox(
            "Quando você pensa no seu personagem, você pensa mais nele usando magia, armas ou uma combinação dos dois?", style_options, index=style_options.index(form_data["style"]), 
            key="style_initial"
        )

        background = st.text_input(
            "Como você descreveria a origem do seu personagem? Ex: nobre, criminoso, hermitão, sábio, artesão, etc.", 
            value=form_data["background"], 
            key="background_initial"
        )

        motivation = st.text_input(
            "O que mais motiva o seu personagem? Ex: vingança, curiosidade, justiça, redenção, etc.", 
            value=form_data["motivation"], 
            key="motivation_initial"
        )

        skill = st.text_input(
            "O que você diria que é a maior habilidade do seu personagem? Ex: ele é muito furtivo, ele sabe muito sobre história, etc", 
            value=form_data["skill"], 
            key="skill_initial"
        )

        complexity = st.selectbox(
            "Você prefere um personagem com jogabilidade mais simples ou mais complexa?", experience_choices, 
            index=experience_choices.index(form_data["complexity"]), 
            key="complexity_initial"
        )

        traits = st.text_input(
            "O seu personagem tem algum traço de personalidade notável? Ex: 'covarde, mas esperto', 'barulhento e orgulhoso', 'silencioso e apático', etc.",
            value=form_data["traits"], 
            key="traits_initial"
        )

        unique_feature_choice = st.selectbox(
            "Você quer que seu personagem tenha alguma característica misteriosa ou especial?", ["Não", "Sim"], 
            index=["Não", "Sim"].index(form_data["unique_feature_choice"]), 
            key="unique_feature_choice_initial"
        )

        unique_feature = None
        if unique_feature_choice == "Sim":
            unique_feature = st.text_input(
                "Informe a característica: (ex: espada amaldiçoada, companheiro animal, linhagem secreta", 
                value=form_data["unique_feature"], 
                key="unique_feature_initial"
            )

        current_form_values = {
            "nome": nome, 
            "genero": genero, 
            "idade": idade,
            "role": role, 
            "alignment": alignment, 
            "style": style,
            "background": background, 
            "motivation": motivation, 
            "skill": skill,
            "complexity": complexity, 
            "traits": traits, 
            "unique_feature_choice": unique_feature_choice,
            "unique_feature": unique_feature
        }

        if st.button("Gerar Personagem", key="generate_button_initial"):
            st.session_state.form_values = current_form_values # Save current state
            with st.spinner("Gerando Personagem"):
                prompt = (f"Crie uma ficha de personagem de Dungeons & Dragons 5e completa com base nas seguintes respostas:"
                          f"Papel que gostaria de desempenhar no grupo: {role}"
                          f"Alinhamento moral: {alignment}"
                          f"Estilo de luta: {style}"
                          f"Origem ou background do personagem: {background}"
                          f"Motivação ou meta: {motivation}"
                          f"A maior habilidade do personagem é: {skill}"
                          f"Preferência por complexidade em termos de jogabilidade: {complexity}"
                          f"Traços de personalidade notáveis: {traits}")
                if unique_feature:
                    prompt += f"Característica especial: {unique_feature}"
                prompt += ("Também inclua na ficha:"
                          f"Nome do personagem: {nome}"
                          f"Gênero: {genero}"
                          f"Idade: {idade}"
                          "Nível inicial: 1"
                          "A resposta deve estar formatada no formato padrão do D&D:"
                          "** Informações Gerais **\n" # Added \n for cleaner markdown
                          "Nome:\n"
                          "Raça:\n"
                          "Classe:\n"
                          "Background:\n"
                          "Alinhamento Moral:\n"
                          "Level:\n"
                          "Gênero:\n"
                          "Idade:\n"
                          "\n"
                          "** Salvaguardas ** (com Bonus Racial aplicado)\n"
                          "Força:\n"
                          "Destreza:\n"
                          "Constituição:\n"
                          "Inteligência:\n"
                          "Sabedoria:\n"
                          "Carisma:\n"
                          "\n"
                          "**Habilidades e Perícias **\n"
                          "Dado de Vida:\n"
                          "Perícias:\n"
                          "Proficiência com Ferramentas:\n"
                          "Idiomas:\n"
                          "\n"
                          "**Combate **\n"
                          "Classe de Armadura:\n"
                          "Iniciativa:\n"
                          "Deslocamento:\n"
                          "Pontos de Vida:\n"
                          "Ataques e Magias:\n"
                          "\n"
                          "** Equipamentos **\n"
                          "- Lista de equipamentos baseados na classe e background\n"
                          "\n"
                          "** Características e Talentos **\n"
                          "Habilidades raciais:\n"
                          "Habilidades de classe:\n"
                          "Características do background:\n"
                          "Característica especial:\n"
                          "\n"
                          "** Personalidade **\n"
                          "Traços de personalidade:\n"
                          "Ideais:\n"
                          "Vínculos:\n"
                          "Fraquezas:\n"
                          "\n"
                          "Faça que o personagem seja agradável de jogar, mecanicamente completo e balanceado para um jogo típico de D&D 5e Level 1. "
                          "Sinta-se livre para tomar escolhas lógicas quando as informações forem vagas."
                          )
                
                st.session_state.generated_response = gerar_resposta_gemini(prompt)
                st.session_state.character_generated = True
                st.rerun() # Use st.rerun() directly

else:
    # Layout after character generation: form on left, response on right
    col_form_left, col_ficha_right = st.columns([1, 2])

    with col_form_left:
        st.markdown("<h2>🎲 Informações do Personagem</h2>", unsafe_allow_html=True)

        # Retrieve values from session state to populate the form
        form_data = st.session_state.form_values

        nome = st.text_input("Qual o nome do personagem?", value=form_data["nome"], key="nome_rerun")
        genero = st.selectbox("Qual o gênero do personagem?", genders, index=genders.index(form_data["genero"]), key="genero_rerun")
        idade = st.number_input("Qual a idade do personagem?", min_value=22, value=form_data["idade"], key="idade_rerun")

        role = st.text_input("Qual tipo de papel você gostaria de desempenhar no grupo?", value=form_data["role"], key="role_rerun")
        alignment = st.selectbox("Você diria que seu personagem é:", alignment_options, index=alignment_options.index(form_data["alignment"]), key="alignment_rerun")
        style = st.selectbox("Quando você pensa no seu personagem, você pensa mais nele usando magia, armas ou uma combinação dos dois?", style_options, index=style_options.index(form_data["style"]), key="style_rerun")
        background = st.text_input("Como você descreveria a origem do seu personagem?", value=form_data["background"], key="background_rerun")
        motivation = st.text_input("O que mais motiva o seu personagem?", value=form_data["motivation"], key="motivation_rerun")
        skill = st.text_input("O que você diria que é a maior habilidade do seu personagem?", value=form_data["skill"], key="skill_rerun")
        complexity = st.selectbox("Você prefere um personagem com jogabilidade mais simples ou mais complexa?", experience_choices, index=experience_choices.index(form_data["complexity"]), key="complexity_rerun")
        traits = st.text_input("O seu personagem tem algum traço de personalidade notável?", value=form_data["traits"], key="traits_rerun")
        unique_feature_choice = st.selectbox("Você quer que seu personagem tenha alguma característica misteriosa ou especial?", ["Não", "Sim"], index=["Não", "Sim"].index(form_data["unique_feature_choice"]), key="unique_feature_choice_rerun")
        unique_feature = None
        if unique_feature_choice == "Sim":
            unique_feature = st.text_input("Informe a característica:", value=form_data["unique_feature"], key="unique_feature_rerun")

        # Capture current form values for re-generation
        current_form_values = {
            "nome": nome, "genero": genero, "idade": idade,
            "role": role, "alignment": alignment, "style": style,
            "background": background, "motivation": motivation, "skill": skill,
            "complexity": complexity, "traits": traits, "unique_feature_choice": unique_feature_choice,
            "unique_feature": unique_feature
        }

        if st.button("Gerar Novamente", key="generate_again_button"):
            st.session_state.form_values = current_form_values # Update saved state
            with st.spinner("Gerando Personagem Novamente"):
                prompt = (f"Crie uma ficha de personagem de Dungeons & Dragons 5e completa com base nas seguintes respostas:"
                          f"Papel que gostaria de desempenhar no grupo: {role}"
                          f"Alinhamento moral: {alignment}"
                          f"Estilo de luta: {style}"
                          f"Origem ou background do personagem: {background}"
                          f"Motivação ou meta: {motivation}"
                          f"A maior habilidade do personagem é: {skill}"
                          f"Preferência por complexidade em termos de jogabilidade: {complexity}"
                          f"Traços de personalidade notáveis: {traits}")
                if unique_feature:
                    prompt += f"Característica especial: {unique_feature}"
                prompt += ("Também inclua na ficha:"
                          f"Nome do personagem: {nome}"
                          f"Gênero: {genero}"
                          f"Idade: {idade}"
                          "Nível inicial: 1"
                          "A resposta deve estar formatada no formato padrão do D&D:"
                          "** Informações Gerais **\n"
                          "Nome:\n"
                          "Raça:\n"
                          "Classe:\n"
                          "Background:\n"
                          "Alinhamento Moral:\n"
                          "Level:\n"
                          "Gênero:\n"
                          "Idade:\n"
                          "\n"
                          "** Salvaguardas ** (com Bonus Racial aplicado)\n"
                          "Força:\n"
                          "Destreza:\n"
                          "Constituição:\n"
                          "Inteligência:\n"
                          "Sabedoria:\n"
                          "Carisma:\n"
                          "\n"
                          "**Habilidades e Perícias **\n"
                          "Dado de Vida:\n"
                          "Perícias:\n"
                          "Proficiência com Ferramentas:\n"
                          "Idiomas:\n"
                          "\n"
                          "**Combate **\n"
                          "Classe de Armadura:\n"
                          "Iniciativa:\n"
                          "Deslocamento:\n"
                          "Pontos de Vida:\n"
                          "Ataques e Magias:\n"
                          "\n"
                          "** Equipamentos **\n"
                          "- Lista de equipamentos baseados na classe e background\n"
                          "\n"
                          "** Características e Talentos **\n"
                          "Habilidades raciais:\n"
                          "Habilidades de classe:\n"
                          "Características do background:\n"
                          "Característica especial:\n"
                          "\n"
                          "** Personalidade **\n"
                          "Traços de personalidade:\n"
                          "Ideais:\n"
                          "Vínculos:\n"
                          "Fraquezas:\n"
                          "\n"
                          "Faça que o personagem seja agradável de jogar, mecanicamente completo e balanceado para um jogo típico de D&D 5e Level 1. "
                          "Sinta-se livre para tomar escolhas lógicas quando as informações forem vagas."
                          )
                st.session_state.generated_response = gerar_resposta_gemini(prompt)
                st.rerun() # Rerun to update the right column

    with col_ficha_right:
        st.markdown("<h2 style='text-align: center;'>📜 Ficha Gerada</h2>", unsafe_allow_html=True)
        if st.session_state.generated_response and len(st.session_state.generated_response.strip()) > 0:
            caminho_pdf = gerar_pdf(st.session_state.generated_response)
            with open(caminho_pdf, "rb") as file:
                st.download_button(
                    label="📄 Baixar Ficha em PDF",
                    data=file,
                    file_name="ficha_personagem.pdf",
                    mime="application/pdf"
                )
            st.write(st.session_state.generated_response)
        else:
            st.warning("Não foi possível gerar a ficha. A resposta está vazia.")