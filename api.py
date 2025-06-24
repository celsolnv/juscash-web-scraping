import requests

def send_to_api(publications, api_url = "https://juscash-test.site/api/publications/batch", token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTA3Mjg3ODcsImV4cCI6MTc1MDgxNTE4Nywic3ViIjoiMSJ9.7PzrqppnnLjp1PiEaunA2PzHSQSog5Pq9Y0osuqhu-s"):
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
