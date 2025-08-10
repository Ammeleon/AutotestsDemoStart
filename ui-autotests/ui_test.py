import os
import time
from base64 import b64encode
from pathlib import Path

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from pytest_html import extras


@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()

    # options.add_argument("--disable-features=PasswordLeakDetection")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--disable-infobars")
    #
    # options.add_experimental_option("prefs", {
    #     "credentials_enable_service": False,
    #     "profile.password_manager_enabled": False,
    #     "profile.default_content_setting_values.notifications": 2
    # })
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

def wait(seconds=2):
    time.sleep(seconds)

def test_login(browser):
    print("\n1. Тестирование авторизации...")
    browser.get("https://www.saucedemo.com")
    assert "Swag Labs" in browser.title
    #wait(2)
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    #wait(2)
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    #wait(2)
    browser.find_element(By.ID, "login-button").click()
    #wait(2)
    assert "inventory.html" in browser.current_url
    print("✅ Авторизация прошла успешно")


def test_add_to_cart(browser):
    print("\n2. Тестирование добавления товара в корзину...")
    #wait(2)
    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    #wait(2)
    assert browser.find_element(By.ID, "remove-sauce-labs-backpack").is_displayed()
    #wait(2)
    assert browser.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "1"
    print("✅ Товар успешно добавлен в корзину")


def test_checkout_process(browser):
    print("\n3. Тестирование оформления заказа...")
    #wait(2)
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "cart.html" in browser.current_url
    browser.find_element(By.ID, "checkout").click()
    #wait(2)
    browser.find_element(By.ID, "first-name").send_keys("Иван")
    #wait(2)
    browser.find_element(By.ID, "last-name").send_keys("Иванов")
    #wait(2)
    browser.find_element(By.ID, "postal-code").send_keys("123456")
    #wait(2)
    browser.find_element(By.ID, "continue").click()
    #wait(2)
    browser.find_element(By.ID, "finish").click()
    #wait(2)
    assert "Thank you for your order!" in browser.find_element(By.CLASS_NAME, "complete-header").text
    print("✅ Заказ успешно оформлен")


def test_logout(browser):
    print("\n4. Тестирование выхода из системы...")
    browser.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
    assert "https://www.saucedemo.com/" == browser.current_url
    print("✅ Выход из системы выполнен успешно")


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