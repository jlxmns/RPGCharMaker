import streamlit as st
import google.generativeai as genai

api_key = st.secrets("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


def gerar_resposta_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# Options
genders = ["Homem", "Mulher", "Não binário", "Outro"]
alignment_options = ["Bom e leal", "Bom e neutro", "Bom e caótico", "Neutro e leal", "Verdadeiramente neutro",
                     "Neutro e caótico", "Mau e leal", "Mau e neutro", "Mau e caótico"]
style_options = ["Armas", "Magia", "Armas e Magia"]
experience_choices = ["Simples", "Moderada", "Complexa"]

# Configuração da página
st.set_page_config(page_title="Gerador de Personagem de RPG", page_icon="🚀")

st.title("Gerador de Personagem de RPG")

# Infos básicas
nome = st.text_input("Qual o nome do personagem?")
genero = st.selectbox("Qual o gênero do personagem?", genders)
idade = st.number_input("Qual a idade do personagem?", min_value=12)

# Sobre a classe
role = st.text_input("Qual tipo de papel você gostaria de desempenhar no grupo? Ex: lutador, suporte, furtivo, versátil, etc.")
alignment = st.selectbox("Você diria que seu personagem é:", alignment_options)
style = st.selectbox("Quando você pensa no seu personagem, você pensa mais nele usando magia, armas ou uma combinação dos dois?", style_options)
background = st.text_input("Como você descreveria a origem do seu personagem? Ex: nobre, criminoso, hermitão, sábio, artesão, etc.")
motivation = st.text_input("O que mais motiva o seu personagem? Ex: vingança, curiosidade, justiça, redençãom, etc.")
skill = st.text_input("O que você diria que é a maior habilidade do seu personagem? Ex: ele é muito furtivo, ele sabe muito sobre história, etc")
complexity = st.selectbox("Você prefere um personagem com jogabilidade mais simples ou mais complexa?", experience_choices)
traits = st.text_input("O seu personagem tem algum traço de personalidade notável? Ex: 'covarde, mas esperto', 'barulhento e orgulhoso', 'silencioso e apático', etc.")
unique_feature_choice = st.selectbox("Você quer que seu personagem tenha alguma característica misteriosa ou especial?", ["Não", "Sim"])
unique_feature = None
if unique_feature_choice == "Sim":
    unique_feature = st.text_input("Informe a característica: (ex: espada amaldiçoada, companheiro animal, linhagem secreta")

if st.button("Gerar Personagem"):
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
                   "** Informações Gerais **"
                   "Nome:"
                   "Raça:"
                   "Classe:"
                   "Background:"
                   "Alinhamento Moral:"
                   "Level:"
                   "Gênero:"
                   "Idade:"
                   ""
                   "** Salvaguardas ** (com Bonus Racial aplicado)"
                   "Força:"
                   "Destreza:"
                   "Constituição:"
                   "Inteligência"
                   "Sabedoria:"
                   "Carisma:"
                   ""
                   "**Habilidades e Perícias **"
                   "Dado de Vida:"
                   "Perícias:"
                   "Proficiência com Ferramentas:"
                   "Idiomas:"
                   ""
                   "**Combate **"
                   "Classe de Armadura:"
                   "Iniciativa:"
                   "Deslocamento:"
                   "Pontos de Vida:"
                   "Ataques e Magias:"
                   ""
                   "** Equipamentos **"
                   "- Lista de equipamentos baseados na classe e background"
                   ""
                   "** Características e Talentos **"
                   "Habilidades raciais:"
                   "Habilidades de classe:"
                   "Características do background:"
                   "Característica especial:"
                   ""
                   "** Personalidade **"
                   "Traços de personalidade:"
                   "Ideais:"
                   "Vínculos:"
                   "Fraquezas:"
                   ""
                   "Faça que o personagem seja agradável de jogar, mecanicamente completo e balanceado para um jogo típico de D&D 5e Level 1. "
                   "Sinta-se livre para tomar escolhar lógicas quando as informações forem vagas."
                   )
        resposta = gerar_resposta_gemini(prompt)
        st.write(resposta)
