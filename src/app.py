import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


@st.cache
def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados


def grafico_comparativo(dados_2019, dados_2020, dados_2021, causa, estado='BRASIL'):

    if estado == "BRASIL":
        total_2019 = dados_2019.groupby('tipo_doenca').sum()
        total_2020 = dados_2020.groupby('tipo_doenca').sum()
        total_2021 = dados_2021.groupby('tipo_doenca').sum()

        lista = [int(total_2019.loc[causa]),
                 int(total_2020.loc[causa]),
                 int(total_2021.loc[causa])]
    else:
        total_2019 = dados_2019.groupby(['uf', 'tipo_doenca']).sum()
        total_2020 = dados_2020.groupby(['uf', 'tipo_doenca']).sum()
        total_2021 = dados_2021.groupby(['uf', 'tipo_doenca']).sum()

        lista = [int(total_2019.loc[estado, causa] if (
            estado, causa) in total_2019.index else 0),
            int(total_2020.loc[estado, causa] if (
                estado, causa) in total_2020.index else 0),
            int(total_2021.loc[estado, causa] if (
                estado, causa) in total_2021.index else 0)]

    dados = pd.DataFrame({'Total': lista, 'Ano': [2019, 2020, 2021]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x='Ano', y='Total', data=dados)
    ax.set_title(f'Óbitos por {causa} - {estado}')

    return fig


def main():
    obitos_2019 = carrega_dados('dados/obitos-2019.csv')
    obitos_2020 = carrega_dados('dados/obitos-2020.csv')
    obitos_2021 = carrega_dados('dados/obitos-2021.csv')

    tipo_doenca = obitos_2020['tipo_doenca'].unique()
    estado = np.append(obitos_2020['uf'].unique(), 'BRASIL')

    st.title('Análise de Óbitos 2019-2021')
    st.markdown('Este trabalho analisa dados dos **óbitos 2019-2021**')
    st.markdown('Dados de 2021 parciais')

    opcao_1 = st.sidebar.selectbox('Selecione o tipo de doença', tipo_doenca)
    opcao_2 = st.sidebar.selectbox('Selecione o estado', estado)
    figura = grafico_comparativo(
        obitos_2019, obitos_2020, obitos_2021, opcao_1, opcao_2)

    st.pyplot(figura)

    # obitos_2019 = carrega_dados('dados/obitos-2019.csv')
    # st.dataframe(obitos_2019)


if __name__ == '__main__':
    main()
