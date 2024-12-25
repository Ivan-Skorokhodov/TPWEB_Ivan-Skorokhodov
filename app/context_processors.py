from django.conf import settings
import requests
import jwt
import time


def get_centrifugo_token(user_id):
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5*60}
    token = jwt.encode(
        claims, settings.CENTRIFUGO_SECRET_KEY, algorithm="HS256")
    return {"token": token, "ws_url": settings.CENTRIFUGO_WS_URL}


def global_settings(request):
    json_data = []
    response = requests.get(
        settings.QUOTE_URL,
        headers={"X-API-KEY": settings.QUOTE_API_KEY},
    )

    if response.status_code == 200:

        try:
            json_data = response.json()
        except requests.exceptions.JSONDecodeError:
            json_data = ["empty quote"]
            print(f"Ошибка при декодировании JSON: {response.text}")

        print(json_data[0])

    return {"daily_quote": json_data[0], **get_centrifugo_token(request.user.id)}
