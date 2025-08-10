import pytest
import requests
import time
from datetime import datetime
import os
import json


# Вспомогательная функция для пауз между запросами
def wait(seconds=1):
    time.sleep(seconds)


# Базовый URL тестового API
BASE_URL = "https://jsonplaceholder.typicode.com"


def print_request_response(request_method, url, request_body=None, response=None):
    """Печатает информацию о запросе и ответе"""
    print(f"\n{'=' * 50}")
    print(f"Запрос: {request_method} {url}")
    if request_body:
        print("Тело запроса:")
        print(json.dumps(request_body, indent=2))
    if response:
        print(f"Код ответа: {response.status_code}")
        print("Тело ответа:")
        print(json.dumps(response.json(), indent=2))
    print(f"{'=' * 50}\n")


def test_get_posts():
    """Тест получения списка постов"""
    print("\n1. Тест получения списка постов...")
    wait(0.5)

    url = f"{BASE_URL}/posts"
    response = requests.get(url)

    print_request_response("GET", url, None, response)

    assert response.status_code == 200
    assert len(response.json()) > 0
    print(f"✅ Получено {len(response.json())} постов")


def test_create_post():
    """Тест создания нового поста"""
    print("\n2. Тест создания поста...")
    wait(1)

    url = f"{BASE_URL}/posts"
    new_post = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }

    response = requests.post(url, json=new_post)
    wait(0.5)

    print_request_response("POST", url, new_post, response)

    assert response.status_code == 201
    created_post = response.json()
    assert created_post["id"] is not None
    assert created_post["title"] == new_post["title"]
    print(f"✅ Создан пост с ID {created_post['id']}")


def test_update_post():
    """Тест обновления поста"""
    print("\n3. Тест обновления поста....")
    wait(1)

    # Сначала получаем существующий пост
    post_id = 1
    get_url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(get_url)

    print_request_response("GET", get_url, None, response)

    assert response.status_code == 200
    wait(0.5)

    # Обновляем пост
    put_url = f"{BASE_URL}/posts/{post_id}"
    updated_data = {
        "title": "Updated Title",
        "body": "Updated body content"
    }

    response = requests.put(put_url, json=updated_data)
    wait(0.5)

    print_request_response("PUT", put_url, updated_data, response)

    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["title"] == updated_data["title"]
    print(f"✅ Пост {post_id} успешно обновлен")


def test_delete_post():
    """Тест удаления поста"""
    print("\n4. Тест удаления поста...")
    wait(1)

    post_id = 1
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url)
    wait(0.5)

    print_request_response("DELETE", url, None, response)

    assert response.status_code == 200
    print(f"✅ Пост {post_id} помечен как удаленный")


def test_get_comments_for_post():
    """Тест получения комментариев к посту"""
    print("\n5. Тест получения комментариев...")
    wait(1)

    post_id = 1
    url = f"{BASE_URL}/posts/{post_id}/comments"
    response = requests.get(url)
    wait(0.5)

    print_request_response("GET", url, None, response)

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    print(f"✅ Получено {len(comments)} комментариев для поста {post_id}")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    # Добавляем информацию о времени выполнения тестов
    session.config._metadata["Test Time"] = time.strftime("%Y-%m-%d %H:%M:%S")


# Хук для изменения метаданных в отчете
def pytest_configure(config):
    config._metadata["Project"] = "Sauce Demo"
    config._metadata["Tester"] = "Your Name"
    # Удаляем стандартные метаданные, которые не нужны
    config._metadata.pop("Packages", None)
    config._metadata.pop("Plugins", None)