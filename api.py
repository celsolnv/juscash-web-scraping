import requests

def send_to_api(publications, api_url, token=None):
    headers = {
        "Content-Type": "application/json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post(api_url, json=publications, headers=headers)
        response.raise_for_status()
        print("✅ All data sent successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send data: {e}")
        return None
