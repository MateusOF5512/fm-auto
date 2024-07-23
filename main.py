from function import *

import streamlit as st


if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None

st.title("Automação Extração de Dados - FM Transportes")
st.markdown('---')

col1, col2 = st.columns([1, 1])
username = col1.text_input("Digite seu LOGIN no Tiny:")
password = col2.text_input("Digite sua SENHA no Tiny:", type="password")

send_button = st.button("Começar Automação")

# Lógica do Streamlit
if send_button:
    df = DataScraper(username, password)

    st.session_state.dataframe = df

# Mostrar o DataFrame no editor
if st.session_state.dataframe is not None:
    df_save = st.data_editor(st.session_state.dataframe)

    # Atualizar o DataFrame no estado da sessão com as edições
    st.session_state.dataframe = df_save

    # Formatando a data de hoje
    data_hoje = date.today()
    data_formatada = data_hoje.strftime("%d-%m")

    # Gerar o CSV para download
    download = df_save.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button(
        label="Download dos Dados em CSV",
        data=download,
        file_name=f"{data_formatada}.csv",
        mime='text/csv'
    )
else:
    st.warning("Clique no botão 'Começar Automação' para carregar e editar os dados.")




