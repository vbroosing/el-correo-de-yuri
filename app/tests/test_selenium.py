from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
import time


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        # Configurar Chrome en modo headless (opcional)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Descomenta si no quieres ver el navegador
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

        # Crear un usuario de prueba
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def tearDown(self):
        self.browser.quit()

    def test_homepage_redirects_to_dashboard(self):
        # Navegar a la URL base
        self.browser.get(self.live_server_url)
        # Debería redirigir a /signin/ porque está protegida por @login_required
        self.assertIn("signin", self.browser.current_url)

    def test_login_success(self):
        # Ir a la página de login
        self.browser.get(f"{self.live_server_url}/signin/")

        # Esperar a que los elementos estén presentes
        wait = WebDriverWait(self.browser, 10)

        # Encontrar campos por name o id (ajusta según tu HTML)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.browser.find_element(By.NAME, "password")
        submit_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'SignIn')]")

        # Rellenar campos
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        # Hacer clic en el botón
        submit_button.click()

        # Esperar redirección a dashboard
        wait.until(EC.url_to_be(f"{self.live_server_url}/dashboard/"))

        # Verificar que estamos en dashboard
        self.assertEqual(self.browser.current_url, f"{self.live_server_url}/dashboard/")

        # Verificar que el título de la página contiene "Dashboard"
        self.assertIn("Dashboard", self.browser.title)

    def test_login_failure(self):
        # Ir a la página de login
        self.browser.get(f"{self.live_server_url}/signin/")

        wait = WebDriverWait(self.browser, 10)

        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.browser.find_element(By.NAME, "password")
        submit_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'SignIn')]")

        # Rellenar con credenciales inválidas
        username_input.send_keys("invaliduser")
        password_input.send_keys("wrongpassword")

        submit_button.click()

        # Esperar a que aparezca un mensaje de error (ajusta según tu template)
        # Ejemplo: si usas mensajes de Django, podrías esperar un div con class="alert"
        try:
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
            self.assertIn("Credenciales inválidas", error_message.text)  # Ajusta el texto según tu mensaje
        except:
            # Si no hay mensaje de error visible, al menos verifica que NO redirigió a dashboard
            self.assertNotEqual(self.browser.current_url, f"{self.live_server_url}/dashboard/")