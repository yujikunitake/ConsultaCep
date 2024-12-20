import requests
from app.models import CEP


def consultar_cep_por_estado_cidade_logradouro(estado: str, cidade: str, logradouro: str):
    url = f"https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/"
    r = requests.get(url)

    if r.status_code == 200:
        resultados = r.json()

        if isinstance(resultados, list):
            return [CEP(**cep) for cep in resultados]
        elif "erro" in resultados:
            raise ValueError(f"Erro: {resultados.get('erro')}")
        else:
            return [CEP(**resultados)]
    else:
        raise Exception(f"Erro ao consultar CEPs: {r.status_code}")
