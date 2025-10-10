import pytest

class TestUserRegistration:
    def test_register_listener_success(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test@example.com",
                "password": "abcD1234!",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": " "
            }
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
    
    def test_password_validation_fall(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test@example.com",
                "password": "asdfasdfasdf",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": " "
            }
        )
        assert response.status_code == 422
        
    def test_user_name_validation(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "Антон_123",
                "email": "test@example.com",
                "password": "abcD1234!",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": "test_genre"
            }
        )
        assert response.status_code == 422
        
    def test_register_duplicate_email(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test@example.com",
                "password": "abcD1234!",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": "test_genre"
            }
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_duplicate_user_name(self, client):
        response = client.post(
            "/register/listener",
            json = {
                "user_name": "test_user",
                "email": "test_2@example.com",
                "password": "abcD1234!",
                "date_of_birthday": "2000-10-10",
                "gender": "test_gender",
                "favorite_genre": "test_genre"
            }
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already registered"

    def test_login_user(self, client):
        response = client.post(
            "/login",
            json = {
                "email": "test@example.com",
                "password": "abcD1234!"
            }
        )
        data = response.json()
        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
