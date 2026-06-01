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

def test_refresh_token():
    client.post("/signup",
                json={
                    "email": "refresh@test.com",
                    "password": "testpassword"
                })
    login_response = client.post("/login",
                                 data={
                                     "username": "refresh@test.com",
                                     "password": "testpassword"
                                 })
    access_token = login_response.json()["access_token"]
    refresh_token = login_response.json()["refresh_token"]
    refresh_response = client.post("/refresh",json ={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    new_access_token = data["access_token"]
    assert new_access_token != access_token
    assert "access_token" in data
    still_logged_in_response = client.get("/me",
                                          headers={"Authorization": f"Bearer {new_access_token}"}
                                          )
    assert still_logged_in_response.status_code == 200

def test_invalid_refresh_token():
    client.post("/signup",
                json={
                    "email": "invalidrefresh@test.com",
                    "password": "testpassword"
                })
    login_response = client.post("/login",
                                 data= {
                                     "username": "invalidrefresh@test.com",
                                     "password": "testpassword"
                                 })
    invalid_token = "asbdajbdhajsbdsabca34uo3UO3909E9Pnjkasbcnmsabncjkackajc12e1e2sjackadsadnajscnans"
    refresh_response = client.post("/refresh",json ={"refresh_token": invalid_token})
    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Invalid refresh token"

def test_refresh_token_rotation():
    client.post("/signup",
                json={
                    "email": "refreshrotation@test.com",
                    "password": "testpassword"
                })
    login_response = client.post("/login",
                                 data={
                                     "username":"refreshrotation@test.com",
                                     "password":"testpassword"
                                 })
    old_refresh_token = login_response.json()["refresh_token"]
    refresh_response = client.post("/refresh",json ={"refresh_token": old_refresh_token})
    assert refresh_response.status_code == 200
    new_refresh_token = refresh_response.json()["refresh_token"]
    refresh_response_2 = client.post("/refresh",json ={"refresh_token": old_refresh_token})
    assert refresh_response_2.status_code == 401
    refresh_response_3 = client.post("/refresh",json ={"refresh_token": new_refresh_token})
    assert refresh_response_3.status_code == 200

def test_logout():
    client.post("/signup",
                json={
                    "email": "logout@test.com",
                    "password": "testpassword"
                })
    login_response = client.post("/login",
                                 data={
                                     "username": "logout@test.com",
                                     "password": "testpassword"
                                 })
    refresh_token = login_response.json()["refresh_token"]
    logout_response = client.post("/logout",
                                  json={
                                      "refresh_token": refresh_token
                                  })
    assert logout_response.status_code == 200
    refresh_response = client.post("/refresh",json ={"refresh_token": refresh_token})
    assert refresh_response.status_code == 401
