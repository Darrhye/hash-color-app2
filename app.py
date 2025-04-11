import streamlit as st
import hashlib

st.set_page_config(page_title="Gerador de Hash com Cores", layout="wide")

st.title("🎲 Gerador de Resultados com Cores (Baseado em Hash)")
st.markdown("Insira a hash final e veja os 100 resultados anteriores com cores determinadas.")

# Input do usuário
final_seed = st.text_input("Digite a hash final (hexadecimal):", 
                           value="41bf80956355675cc47c0dfa2a39d2dfb58b14e401263d59688e1d91cc24e6dd")

count = st.slider("Quantidade de resultados anteriores:", 10, 200, 100)

# Função para determinar a cor
def get_color_from_hash(hash_hex):
    number = int(hash_hex, 16)
    if number % 15 == 0:
        return "⚪️ Branco"
    elif number % 2 == 0:
        return "⚫️ Preto"
    else:
        return "🔴 Vermelho"

# Geração reversa
def generate_reverse_chain_with_colors(seed, count):
    chain = [seed]
    results = [(1, seed, get_color_from_hash(seed))]

    for i in range(1, count):
        prev_hash = hashlib.sha256(bytes.fromhex(chain[-1])).hexdigest()
        chain.append(prev_hash)
        color = get_color_from_hash(prev_hash)
        results.append((i+1, prev_hash, color))
    
    return results

if st.button("🔄 Gerar Resultados"):
    if len(final_seed) != 64:
        st.error("A hash deve ter exatamente 64 caracteres (hexadecimal).")
    else:
        results = generate_reverse_chain_with_colors(final_seed, count)

        st.markdown("### 🧾 Resultados")
        for index, hash_val, color in results:
            st.write(f"{index}: `{hash_val}` → {color}")
