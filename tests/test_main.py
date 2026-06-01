import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from conftest import client

#First integration test
def test_root():
    response = client.get("/docs")
    assert response.status_code == 200