from conftest import client

def test_signup():
    response = client.post("/signup",
                          json={
                              "email": "test@example.com",
                              "password": "testpassword"
                          }
                        )
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_login():
    client.post("/signup",
                json={
                    "email": "login@example.com",
                    "password": "testpassword"
                }
            )
    response = client.post("/login",
                           data={
                               "username": "login@example.com",
                               "password": "testpassword"
                           }
                        )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_current_user():
    client.post("/signup",
                json={
                    "email": "me@test.com",
                    "password": "testpassword"
                }
                )
    login_response = client.post("/login",
                                 data={
                                     "username": "me@test.com",
                                     "password": "testpassword"
                                 }
                                 )
    token = login_response.json()["access_token"]
    response = client.get("/me",
                          headers={"Authorization": f"Bearer {token}"}
                          )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@test.com"
    assert "hashed_password" not in data