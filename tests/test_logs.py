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
                                  headers={"Authorization": f"Bearer {token_a}"}
                                  )
    log_id = create_response.json()["id"]

    token_b = create_user_and_get_token("deleteb@test.com", "testpassword")
    response_b = client.delete(f"/logs/{log_id}",headers={"Authorization": f"Bearer {token_b}"})
    assert response_b.status_code == 404

def test_pagination():
    token = create_user_and_get_token("pagination@test.com", "testpassword")
    for i in range(5):
        client.post("/logs",
                      json= {"food": f"Test Food {i}",
                             "calories": 100,
                             "protein": 10,
                             "fiber": 2,
                             "date": "2026-05-26"
                             },
                      headers={"Authorization": f"Bearer {token}"}
                      )
    response = client.get("/logs?skip=0&limit=2",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_filter_food():
    token = create_user_and_get_token("filterfood@test.com", "testpassword")
    for i in range(2):
        client.post("/logs",
                    json= {"food": f"Chicken {i}",
                           "calories": 100,
                           "protein": 20,
                           "fiber": 2,
                           "date": "2026-05-26"
                           },
                    headers={"Authorization": f"Bearer {token}"}
                    )
    for i in range(2):
        client.post("/logs",
                    json= {"food": f"Veg Food {i}",
                           "calories": 100,
                           "protein": 5,
                           "fiber": 4,
                           "date": "2026-05-26"},
                    headers={"Authorization": f"Bearer {token}"}
                    )
    response = client.get("/logs?food=chicken",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_filter_calories():
    token = create_user_and_get_token("calories@test.com", "testpassword")
    for i in range(10):
        client.post("/logs",
                    json= {"food": f"Food {i}",
                           "calories": 100 + (i*100),
                           "protein": 10,
                           "fiber": 2,
                           "date": "2026-05-26"},
                    headers={"Authorization": f"Bearer {token}"}
                    )
    response = client.get("/logs?min_calories=300&max_calories=900",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7

def test_filter_date():
    token = create_user_and_get_token("date@test.com", "testpassword")
    client.post("/logs",
                json={
                    "food": "Food A",
                    "calories": 100,
                    "protein": 10,
                    "fiber": 2,
                    "date": "2026-05-26"
                },
                headers={"Authorization": f"Bearer {token}"}
                )
    client.post("/logs",
                json={
                    "food": "Food B",
                    "calories": 100,
                    "protein": 10,
                    "fiber": 2,
                    "date": "2026-05-25"
                },
                headers={"Authorization": f"Bearer {token}"}
                )
    client.post("/logs",
                json={
                    "food": "Food C",
                    "calories": 100,
                    "protein": 10,
                    "fiber": 2,
                    "date": "2026-05-21"
                },
                headers={"Authorization": f"Bearer {token}"}
                )
    response = client.get("/logs?start_date=2026-05-21&end_date=2026-05-25",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_sort():
    token = create_user_and_get_token("sort@test.com", "testpassword")
    client.post("/logs",
                json= {"food": "Food A",
                       "calories": 100,
                       "protein": 10,
                       "fiber": 2,
                       "date": "2026-05-26"
                       },
                headers={"Authorization": f"Bearer {token}"}
                )
    client.post("/logs",
                json= {"food": "Food B",
                       "calories": 100,
                       "protein": 10,
                       "fiber": 2,
                       "date": "2026-05-25"
                       },
                headers={"Authorization": f"Bearer {token}"}
                )
    client.post("/logs",
                json= {"food": "Food C",
                       "calories": 100,
                       "protein": 10,
                       "fiber": 2,
                       "date": "2026-05-21"},
                headers={"Authorization": f"Bearer {token}"}
                )
    response = client.get("/logs",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    dates = [log["date"] for log in data]
    assert dates == sorted(dates, reverse=True)
