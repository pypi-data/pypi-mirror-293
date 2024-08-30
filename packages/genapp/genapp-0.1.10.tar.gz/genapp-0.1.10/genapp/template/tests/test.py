import json

import httpx

base_url = "http://127.0.0.1:8000"
token_url = f"{base_url}/token"


client_id = "admin"
client_secret = "1"


token_response = httpx.post(
    token_url,
    data={"grant_type": "password",
          "username": client_id, "password": client_secret},
)

json = json.loads(token_response.text)

print(str(token_response.text))


protected_url = f"{base_url}/protected_route"

if "access_token" in json:

    access_token = json.get("access_token")

    response = httpx.get(protected_url, headers={
                         "Authorization": f"Bearer {access_token}"})
    print(str(response.text))
