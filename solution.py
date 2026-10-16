# pip install requests python-dotenv folium
import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

# 1. Carregar credenciais do arquivo .env
load_dotenv(".env")
token_sptrans = os.getenv("SPTRANS_TOKEN")

# Criar sessão persistente para as requisições
conexao = requests.Session()

# Etapa 1: Autenticação na API Olho Vivo
url_autenticar = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token_sptrans}"
login_status = conexao.post(url_autenticar)
print(f"Autenticação realizada: {login_status.text}")

# Linha escolhida: 695X (Terminal Jabaquara) -> Código: 1441
# (Diferente da linha 2506 utilizada nos slides do professor)
CODIGO_LINHA_ALVO = 1441

# Etapa 2: Busca por paradas da linha selecionada
url_paradas = f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={CODIGO_LINHA_ALVO}"
resposta_paradas = conexao.get(url_paradas).json()
print(f"Quantidade de paradas mapeadas: {len(resposta_paradas)}")

# Etapa 3: Busca pelas posições dos veículos em tempo real
url_posicao = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={CODIGO_LINHA_ALVO}"
dados_tempo_real = conexao.get(url_posicao).json()
lista_onibus = dados_tempo_real.get("vs", [])
print(f"Quantidade de ônibus ativos agora: {len(lista_onibus)}")

# Etapa 4: Criação e configuração do mapa interativo
# Centraliza o mapa na primeira parada encontrada
latitude_inicial = resposta_paradas[0]["py"]
longitude_inicial = resposta_paradas[0]["px"]

mapa_sptrans = Map(
    location=[latitude_inicial, longitude_inicial],
    zoom_start=13
)

# Renderizar os pins das Paradas de Ônibus (Cor: Verde)
for parada in resposta_paradas:
    Marker(
        location=[parada["py"], parada["px"]],
        popup=parada["np"],
        icon=Icon(color="pink", icon="info-sign")
    ).add_to(mapa_sptrans)

# Renderizar os pins dos Ônibus em tempo real (Cor: Laranja)
for veiculo in lista_onibus:
    Marker(
        location=[veiculo["py"], veiculo["px"]],
        popup=f"Prefixo: {veiculo['p']}",
        icon=Icon(color="darkpurple", icon="info-sign")
    ).add_to(mapa_sptrans)

# Salvar o arquivo final do mapa
mapa_sptrans.save("mapa.html")
print("Sucesso! O arquivo 'mapa.html' foi gerado corretamente.")
