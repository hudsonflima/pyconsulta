import streamlit as st
import requests

# Configurações iniciais
API_URL_BASE = "http://api.dbconsultas.com/api/v1"
TOKEN = "b51eb780-acfe-42c6-a67f-2e2f40951d45"

st.title("Consulta DBConsultas - Individual")

modulo = st.selectbox("Selecione o módulo para consulta:", [
    "CPF", "TELEFONE", "NOME", "CEP", "EMAIL", "TITULO", 
    "NOME_MAE", "PLACA", "DATALINKCPF", "DATALINKTELEFONE", 
    "DATALINKNOME", "PIX", "DIVIDAS"
])

dado = st.text_input(f"Digite o {modulo}:")

if st.button("Consultar"):
    if not dado:
        st.warning("Por favor, preencha o campo antes de consultar.")
    else:
        url = f"{API_URL_BASE}/{TOKEN}/{modulo.lower()}/{dado}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                st.success("Consulta realizada com sucesso:")
                st.json(result)
            else:
                st.error(f"Erro na consulta: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
