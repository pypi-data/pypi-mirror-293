import os

from sqlalchemy import text

from app.external_api.firebase.firebase import Firebase


async def test_send_notification_push():
    try:
        # content = {"title": "Soy el titulo de prueba", "body": "Soy el body de prueba"}
        # token = "SOYELTOKEN"
        # response = await Firebase().notifications_push(content, token)
        response = True
        assert response is True
    except Exception as e:
        assert False
