import json
import polars as pl
from requests import post
import streamlit as st

#função main do programa
def main() -> None:
    Frontend()


#classe construtora do frontend
class Frontend():

    #método construtor
    def __init__(self):

        #url da API
        self.API_URL = "https://pi-cloud.onrender.com/analyze"
        
        #configurações base do front
        st.set_page_config(
            page_title="ClimateDataViewer",
            page_icon="📊",
            layout="wide"
        )

        #quadrante para o upload do arquivo csv
        file = st.file_uploader("Envie o CSV", type="csv")

        #mapping dos dados do csv
        if file:
            self.data_mapping(file)

    #função de mapping
    def data_mapping(self, file) -> None:

        #reseta o ponteiro do arquivo para evitar bugs
        file.seek(0)

        #cria o dataframe com os dados do csv
        df = pl.read_csv(file, separator=",")


        columns = df.columns
        st.write("Colunas encontradas:", columns)

        mapping = {}

        options = [
            "Ignorar",
            "Data",
            "Precipitação",
            "Temperatura",
        ]

        #container para a seleção dos dados para o mapping
        with st.container(border=True):
            st.subheader("Mapeamento de colunas")

            #colunas do container (melhora UI)
            col1, col2 = st.columns(2)

            #itera o índice e o valor das columns do df
            for i, col in enumerate(columns):

                #separa os dados entre as colunas
                target = col1 if i % 2 == 0 else col2

                #cria as selectbox
                with target:
                    selected = st.selectbox(
                        f"Coluna '{col}' representa:",
                        options,
                        key=f"map_{col}_{i}"
                    )

                mapping[col] = selected


        #botão para a análise
        if st.button("Analisar dados"):

            #reseta o ponteiro do arquivo
            file.seek(0)

            #passa os parâmetros do arquivo a ser enviado para a API
            files = {
                "file": (file.name, file.getvalue(), "text/csv")
            }

            #passa os parâmetros dos dados a serem enviados para a API
            data = {
                "mapping": json.dumps(mapping)
            }

            #tentar:
            try:

                #envia dados para a API
                response = post(
                    self.API_URL,
                    files=files,
                    data=data
                )

                #se houver resposta positiva, exibir os dados
                if response.status_code == 200:

                    result = response.json()

                    precipitacao_stats = result["precipitacao"]
                    temperatura_stats = result["temperatura"]

                    st.subheader("Resultados da análise")

                    self.exibir_dados_precipitacao(stats=precipitacao_stats)
                    self.exibir_dados_temperatura(stats=temperatura_stats)

                #senão, apontar erro
                else:

                    st.error("Erro ao processar os dados.")
                    st.error(response.text)

            except Exception as e:
                st.error(str(e))

    #função para exibir dados de precipitação
    def exibir_dados_precipitacao(self, stats):
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🌧 Total precipitação",
            f"{stats['total_precipitacao']:.2f} mm"
        )

        c2.metric(
            "📊 Média precipitação",
            f"{stats['media_precipitacao']:.2f} mm"
        )

        c3.metric(
            "📉 Desvio padrão precipitação",
            f"{stats['desvio_padrao_precipitacao']:.2f}"
        )

        c4.metric(
            "☀ Dias secos",
            stats["dias_secos"]
        )

    #função para exibir dados de temperatura
    def exibir_dados_temperatura(self, stats):
        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "🌧 Total temperatura",
            f"{stats['total_temperatura']:.2f} °C"
        )

        c2.metric(
            "📊 Média temperatura",
            f"{stats['media_temperatura']:.2f} °C"
        )

        c3.metric(
            "📉 Desvio padrão temperatura",
            f"{stats['desvio_padrao_temperatura']:.2f}"
        )

        c4.metric(
            "Temperatura Mínima",
            stats["temperatura_minima"]
        )

        c5.metric(
            "Temperatura Máxima",
            stats["temperatura_maxima"]
        )

if __name__ == "__main__":
    main()