import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

st.set_page_config(page_title="Análise de Cores - Blaze Double", layout="wide")

st.title("🎯 Análise Estatística Avançada - Blaze Double (Simulado)")
st.markdown("Este app simula os resultados de cores do jogo Double da Blaze e analisa padrões estatísticos para tomada de decisões.")

# Simular resultados
cor_dict = {0: '🔴 Vermelho', 1: '⚫️ Preto', 2: '⚪️ Branco'}
cor_numeros = [0]*8 + [1]*8 + [2]  # distribuição Blaze realista

resultados = [random.choice(cor_numeros) for _ in range(200)]  # últimos 200 resultados
cores = [cor_dict[i] for i in resultados]
df = pd.DataFrame({
    'Rodada': list(range(1, 201)),
    'Cor_Num': resultados,
    'Cor': cores
})

# Mostrar tabela
st.subheader("📋 Últimos 200 resultados (simulados)")
st.dataframe(df[::-1], use_container_width=True)

# Frequência Absoluta e Relativa
st.subheader("📊 Frequência de cada cor")
frequencia = df['Cor_Num'].value_counts().sort_index()
frequencia.index = ['🔴 Vermelho', '⚫️ Preto', '⚪️ Branco']
percentual = (frequencia / len(df)) * 100

col1, col2 = st.columns(2)
col1.metric("🔴 Vermelho", f"{frequencia[0]}x", f"{percentual[0]:.1f}%")
col2.metric("⚫️ Preto", f"{frequencia[1]}x", f"{percentual[1]:.1f}%")
st.metric("⚪️ Branco", f"{frequencia[2]}x", f"{percentual[2]:.1f}%")

# Gráfico de barras
st.subheader("📈 Gráfico de Frequência")
fig, ax = plt.subplots()
sns.countplot(x='Cor', data=df, order=['🔴 Vermelho', '⚫️ Preto', '⚪️ Branco'], palette=['red', 'black', 'gray'], ax=ax)
ax.set_ylabel("Ocorrências")
st.pyplot(fig)

# Matriz de transição (Markov)
st.subheader("🔄 Matriz de Transição de Cores")
matriz = np.zeros((3,3))
for i in range(1, len(resultados)):
    matriz[resultados[i-1], resultados[i]] += 1

matriz_prob = matriz / matriz.sum(axis=1)[:, None]
matriz_df = pd.DataFrame(matriz_prob, columns=['🔴 Próx: Vermelho', '⚫️ Próx: Preto', '⚪️ Próx: Branco'],
                         index=['🔴 Atual: Vermelho', '⚫️ Atual: Preto', '⚪️ Atual: Branco'])

st.dataframe(matriz_df.style.format("{:.2%}"))

# Alerta branco ausente
branco_gap = (df['Cor_Num'][::-1] != 2).idxmax()
if branco_gap > 20:
    st.warning(f"⚠️ Atenção: Já se passaram {branco_gap} rodadas sem branco! Pode estar próximo.")
else:
    st.success(f"Último branco apareceu há {branco_gap} rodadas.")

# Sugestão de aposta (simples)
mais_frequente = percentual.idxmax()
st.info(f"🎯 Sugestão: a cor mais comum até agora é **{mais_frequente}**. Avalie a continuidade da tendência!")
