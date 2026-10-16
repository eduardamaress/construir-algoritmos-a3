import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")
token_sptrans = os.getenv("SPTRANS_TOKEN")

conexao = requests.Session()

url_autenticar = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token_sptrans}"
login_status = conexao.post(url_autenticar)
print(f"Autenticação realizada: {login_status.text}")

CODIGO_LINHA_ALVO = 1441

url_paradas = f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={CODIGO_LINHA_ALVO}"
resposta_paradas = conexao.get(url_paradas).json()
print(f"Quantidade de paradas mapeadas: {len(resposta_paradas)}")

url_posicao = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={CODIGO_LINHA_ALVO}"
dados_tempo_real = conexao.get(url_posicao).json()
lista_onibus = dados_tempo_real.get("vs", [])
print(f"Quantidade de ônibus ativos agora: {len(lista_onibus)}")

latitude_inicial = resposta_paradas[0]["py"]
longitude_inicial = resposta_paradas[0]["px"]

mapa_sptrans = Map(
    location=[latitude_inicial, longitude_inicial],
    zoom_start=13
)

for parada in resposta_paradas:
    Marker(
        location=[parada["py"], parada["px"]],
        popup=parada["np"],
        icon=Icon(color="pink", icon="info-sign")
    ).add_to(mapa_sptrans)

for veiculo in lista_onibus:
    Marker(
        location=[veiculo["py"], veiculo["px"]],
        popup=f"Prefixo: {veiculo['p']}",
        icon=Icon(color="darkpurple", icon="info-sign")
    ).add_to(mapa_sptrans)

mapa_sptrans.save("mapa.html")
print("Sucesso! O arquivo 'mapa.html' foi gerado corretamente.")
