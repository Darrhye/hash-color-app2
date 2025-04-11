import streamlit as st
import hashlib

st.set_page_config(page_title="Gerador de Hash com Cores", layout="wide")

st.title("🎨 Visualizador de Cores Futuras (com base em Hash)")
st.markdown("Insira a hash final e veja os 100 resultados anteriores com cores codificadas:")

# Entrada do usuário
final_seed = st.text_input("Digite a hash final (64 caracteres hex):", 
                           value="41bf80956355675cc47c0dfa2a39d2dfb58b14e401263d59688e1d91cc24e6dd")

count = st.slider("Quantidade de resultados:", 10, 200, 100)

# Função para determinar a cor visual e nome
def get_color_info(hash_hex):
    number = int(hash_hex, 16)
    if number % 15 == 0:
        return "#ffffff", "Branco ⚪️"
    elif number % 2 == 0:
        return "#000000", "Preto ⚫️"
    else:
        return "#ff0000", "Vermelho 🔴"

# Função para gerar hashes reversas e cores
def generate_colored_chain(seed, count):
    results = []
    current_hash = seed
    for i in range(count):
        color_hex, color_name = get_color_info(current_hash)
        results.append((i + 1, current_hash, color_hex, color_name))
        current_hash = hashlib.sha256(bytes.fromhex(current_hash)).hexdigest()
    return results

# Exibir resultados
if st.button("🔄 Mostrar Cores Futuras"):
    if len(final_seed) != 64:
        st.error("A hash precisa ter 64 caracteres hexadecimais.")
    else:
        results = generate_colored_chain(final_seed, count)

        st.markdown("### 🧾 Tabela de Resultados")
        st.markdown("""
        <style>
        .hash-table {
            border-collapse: collapse;
            width: 100%;
        }
        .hash-table th, .hash-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            font-family: monospace;
        }
        .color-box {
            width: 40px;
            height: 20px;
            display: inline-block;
            border: 1px solid #888;
            border-radius: 3px;
        }
        </style>
        """, unsafe_allow_html=True)

        table_html = "<table class='hash-table'><tr><th>#</th><th>Hash</th><th>Cor</th><th>Visual</th></tr>"
        for index, h, hex_color, name in results:
            table_html += f"""
            <tr>
                <td>{index}</td>
                <td>{h}</td>
                <td>{name}</td>
                <td><div class="color-box" style="background-color:{hex_color};"></div></td>
            </tr>
            """
        table_html += "</table>"

        st.markdown(table_html, unsafe_allow_html=True)
