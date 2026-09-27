import requests
from flask import current_app

def get_dados_api_futebol(path: str, params: dict = None) -> tuple[dict | None, int]:
    """
    Realiza requisições para a API-Futebol injetando a chave de autenticação.
    """
    api_url = current_app.config.get('FOOTBALL_API_URL')
    api_key = current_app.config.get('FOOTBALL_API_KEY')

    url = f"{api_url}{path}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        # Retorna o JSON e o status code retornado pela API externa
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {"message": "Erro ao consultar provedor externo", "details": response.text}, response.status_code

    except requests.exceptions.Timeout:
        return {"message": "Tempo limite excedido ao consultar API externa"}, 504
    except requests.exceptions.RequestException as e:
        return {"message": f"Erro de conexão com API externa: {str(e)}"}, 503