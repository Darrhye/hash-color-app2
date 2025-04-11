import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

print("\n🎯 Análise Estatística Avançada - Blaze Double (Simulado)")
print("Este script simula os resultados de cores do jogo Double da Blaze e analisa padrões estatísticos para tomada de decisões.\n")

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
print("📋 Últimos 200 resultados (simulados):")
print(df[::-1].to_string(index=False))

# Frequência Absoluta e Relativa
frequencia = df['Cor_Num'].value_counts().sort_index()
frequencia.index = ['🔴 Vermelho', '⚫️ Preto', '⚪️ Branco']
percentual = (frequencia / len(df)) * 100

print("\n📊 Frequência de cada cor:")
for cor, freq, pct in zip(frequencia.index, frequencia.values, percentual):
    print(f"{cor}: {freq}x ({pct:.1f}%)")

# Gráfico de barras
plt.figure(figsize=(6, 4))
sns.countplot(x='Cor', data=df, order=['🔴 Vermelho', '⚫️ Preto', '⚪️ Branco'], palette=['red', 'black', 'gray'])
plt.title("Frequência das Cores")
plt.ylabel("Ocorrências")
plt.tight_layout()
plt.show()

# Matriz de transição (Markov)
print("\n🔄 Matriz de Transição de Cores:")
matriz = np.zeros((3,3))
for i in range(1, len(resultados)):
    matriz[resultados[i-1], resultados[i]] += 1

matriz_prob = matriz / matriz.sum(axis=1)[:, None]
matriz_df = pd.DataFrame(matriz_prob, columns=['🔴 Próx: Vermelho', '⚫️ Próx: Preto', '⚪️ Próx: Branco'],
                         index=['🔴 Atual: Vermelho', '⚫️ Atual: Preto', '⚪️ Atual: Branco'])
print(matriz_df.applymap(lambda x: f"{x:.2%}").to_string())

# Alerta branco ausente
branco_gap = (df['Cor_Num'][::-1] != 2).idxmax()
print("\n📢 Alerta:")
if branco_gap > 20:
    print(f"⚠️ Já se passaram {branco_gap} rodadas sem branco! Pode estar próximo.")
else:
    print(f"Último branco apareceu há {branco_gap} rodadas.")

# Sugestão de aposta (simples)
mais_frequente = percentual.idxmax()
print(f"\n🎯 Sugestão: a cor mais comum até agora é **{frequencia.index[mais_frequente]}**. Avalie a continuidade da tendência!")
