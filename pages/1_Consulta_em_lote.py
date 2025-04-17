import streamlit as st
import requests
import time
import pandas as pd
import io

API_URL_BASE = "http://api.dbconsultas.com/api/v1"
TOKEN = "b51eb780-acfe-42c6-a67f-2e2f40951d45"
MODULO = "nome"

def consultar_nome(nome):
    url = f"{API_URL_BASE}/{TOKEN}/{MODULO}/{nome}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            # Ajuste conforme estrutura real da resposta
            telefone = dados.get("telefone", "Não encontrado")
            cpf = dados.get("cpf", "Não encontrado")
            return {"nome": nome, "telefone": telefone, "cpf": cpf, "status": "sucesso"}
        else:
            return {"nome": nome, "telefone": None, "cpf": None, "status": "falha"}
    except:
        return {"nome": nome, "telefone": None, "cpf": None, "status": "erro"}

st.title("Consulta em massa de Nomes - DBConsultas")

uploaded_file = st.file_uploader("Faça o upload do arquivo .txt com os nomes (1 por linha)", type=["txt"])

if uploaded_file is not None:
    nomes = uploaded_file.read().decode("utf-8").splitlines()
    nomes = [nome.strip() for nome in nomes if nome.strip()]
    
    if st.button("Iniciar consulta"):
        resultados = []
        sucesso = 0
        falha = 0

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, nome in enumerate(nomes):
            resultado = consultar_nome(nome)
            resultados.append(resultado)

            if resultado["status"] == "sucesso":
                sucesso += 1
            else:
                falha += 1

            progress_bar.progress((i + 1) / len(nomes))
            status_text.text(f"Processando {i + 1}/{len(nomes)}...")

            time.sleep(0.2)  # delay para não sobrecarregar

        st.success("Consulta finalizada!")

        df_resultado = pd.DataFrame(resultados)
        st.dataframe(df_resultado)

        # Métricas
        st.subheader("Resumo da Operação")
        st.metric("Total de nomes", len(nomes))
        st.metric("Consultas com sucesso", sucesso)
        st.metric("Falhas ou erros", falha)
        precisao = (sucesso / len(nomes)) * 100 if nomes else 0
        st.metric("Precisão (%)", f"{precisao:.2f}%")

        # Botão para download
        csv = df_resultado.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar resultados em CSV",
            data=csv,
            file_name="resultado_consultas.csv",
            mime="text/csv"
        )
