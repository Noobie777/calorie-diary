from conftest import client
#helpers

def create_user_and_get_token(email, password):
    client.post("/signup",
                json={
                    "email": email,
                    "password": password
                }
                )
    login_response = client.post("/login",
                                 data={
                                     "username":email,
                                     "password":password
                                 })
    token = login_response.json()["access_token"]
    return token

def test_create_logs():
    token = create_user_and_get_token("logs@test.com","testpassword")
    response = client.post("/logs",
                           json={
                               "food": "Test Food",
                               "calories": 500,
                               "protein": 30,
                               "fiber": 5,
                               "date": "2026-05-21"
                           },
                           headers={"Authorization": f"Bearer {token}"
                                    }
                           )
    assert response.status_code == 200
    data = response.json()
    assert data["food"] == "Test Food"
    assert data["calories"] == 500

def test_user_cannot_access_other_users_logs():
    token_a = create_user_and_get_token("usera@test.com", "testpassword")
    create_response = client.post("/logs",
                                  json={
                                      "food": "Test Food A",
                                      "calories": 100,
                                      "protein": 10,
                                      "fiber": 2,
                                      "date": "2026-05-21"
                                  },
                                  headers={"Authorization": f"Bearer {token_a}"
                                           }
                                  )
    log_id = create_response.json()["id"]

    token_b = create_user_and_get_token("userb@test.com", "testpassword")
    response = client.get(f"/logs/{log_id}",
                          headers={"Authorization": f"Bearer {token_b}"})
    assert response.status_code == 404

def test_user_cannot_update_other_users_logs():
    token_a = create_user_and_get_token("updatea@test.com", "testpassword")
    create_response = client.post("/logs",
                                  json={
                                      "food": "Test Food A",
                                      "calories": 100,
                                      "protein": 10,
                                      "fiber": 2,
                                      "date": "2026-05-21"
                                  },
                                  headers={"Authorization": f"Bearer {token_a}"}
                                  )
    log_id = create_response.json()["id"]

    token_b = create_user_and_get_token("updateb@test.com", "testpassword")
    response_b = client.put(f"/logs/{log_id}",
                            json={
                                "food": "Test Food B",
                                "calories": 100,
                                "protein": 10,
                                "fiber": 2,
                                "date": "2026-05-21"
                            },
                            headers={"Authorization": f"Bearer {token_b}"})
    assert response_b.status_code == 404

def test_user_cannot_delete_other_users_logs():
    token_a = create_user_and_get_token("deletea@test.com", "testpassword")
    create_response = client.post("/logs",
                                  json={
                                      "food": "Delete Food A",
                                      "calories": 100,
                                      "protein": 10,
                                      "fiber": 2,
                                      "date": "2026-05-21"
                                  },
                                  headers={"Authorization": f"Bearer {token_a}"
                                           }
                                  )
    log_id = create_response.json()["id"]

    token_b = create_user_and_get_token("deleteb@test.com", "testpassword")
    response_b = client.delete(f"/logs/{log_id}",headers={"Authorization": f"Bearer {token_b}"})
    assert response_b.status_code == 404