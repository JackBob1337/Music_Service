import pytest

class TestUserRegistration:
    def test_register_listener_success(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test@example.com",
                "password": "qwerty123",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": " "
            }
        )
        print("*" * 20)
        print(response.json())
        print("*" * 20)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_register_duplicate_email_listener(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test@example.com",
                "password": "qwerty123",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": "test_genre"
            }
        )
        print("*" * 20)
        print(response.json())
        print("*" * 20)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_duplicate_user_name_listener(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test_2@example.com",
                "password": "qwerty123",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": "test_genre"
            }
        )
        print("*" * 20)
        print(response.json())
        print("*" * 20)

        assert response.status_code == 400
        assert response.json()["detail"] == "Username already registered"

    def test_login_user(self, client):
        response = client.post(
            "/login",
            json = {
                "email": "test@example.com",
                "password": "qwerty123"
            }
        )

        data = response.json()

        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
        assert isinstance(data["access_token"], str) and len(data["access_token"]) > 0
        assert isinstance(data["refresh_token"], str) and len(data["refresh_token"]) > 0

