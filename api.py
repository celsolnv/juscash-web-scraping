import requests

def send_to_api(publications, api_url = "http://localhost:8080/api/publications/batch", token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTA3MDAyMDksImV4cCI6MTc1MDc4NjYwOSwic3ViIjoiMiJ9.bW-bhVX3xud8oLjyzp8oQwjxDXM78In1PdkshqgIAIs"):
    headers = {
        "Content-Type": "application/json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post(api_url, json=publications, headers=headers)
        response.raise_for_status()
        print("✅ Todos os dados enviados com sucesso!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Falha ao enviar os dados {e}")
        return None
