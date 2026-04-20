import requests
from app.core.config import settings

def trigger_n8n(payload: dict) -> dict | None:
    try:
        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print('[n8n] Webhook timed out.')
        return None
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 'Unknown'
        text = e.response.text if e.response else 'No response text'
        print(f'[n8n] HTTP error: {status_code} — {text}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'[n8n] Webhook failed: {e}')
        return None
