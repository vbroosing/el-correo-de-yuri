from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User, Group
import time

class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        # Configurar Chrome en modo headless (opcional)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Comenta esto si quieres ver el navegador
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
        
        # Crear grupos necesarios para las pruebas
        self.grupo_trabajador, _ = Group.objects.get_or_create(name='Trabajador')
        self.grupo_jefe, _ = Group.objects.get_or_create(name='Jefe RRHH')

    def tearDown(self):
        self.browser.quit()

    def _login(self):
        """Método auxiliar para iniciar sesión"""
        self.browser.get(f"{self.live_server_url}/signin/")
        wait = WebDriverWait(self.browser, 10)
        
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.browser.find_element(By.NAME, "password")
        submit_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'SignIn')]")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()
        
        # Esperar a que cargue el dashboard
        wait.until(EC.url_to_be(f"{self.live_server_url}/dashboard/"))

    def test_homepage_redirects_to_dashboard(self):
        # Navegar a la URL base (protegida) debería redirigir al login
        self.browser.get(self.live_server_url)
        self.assertIn("signin", self.browser.current_url)

    def test_login_success(self):
        self._login()
        # Verificar que estamos en dashboard
        self.assertEqual(self.browser.current_url, f"{self.live_server_url}/dashboard/")
        self.assertIn("Dashboard", self.browser.title)

    def test_login_failure(self):
        self.browser.get(f"{self.live_server_url}/signin/")
        wait = WebDriverWait(self.browser, 10)

        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.browser.find_element(By.NAME, "password")
        submit_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'SignIn')]")

        # Rellenar con credenciales inválidas
        username_input.send_keys("invaliduser")
        password_input.send_keys("wrongpassword")
        submit_button.click()

        # Verificar que NO redirigió a dashboard (se mantiene en signin o muestra error)
        self.assertNotEqual(self.browser.current_url, f"{self.live_server_url}/dashboard/")

    def test_trabajador_dashboard_elements(self):
        """
        Prueba que un usuario con el rol 'Trabajador' vea las opciones correctas
        en el dashboard.
        """
        # Asignar grupo Trabajador al usuario
        self.user.groups.add(self.grupo_trabajador)
        self.user.save()

        self._login()

        # Verificar presencia de elementos específicos del Trabajador
        wait = WebDriverWait(self.browser, 10)
        
        # Buscar el botón de "MODIFICAR DATOS PERSONALES"
        boton_modificar = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'MODIFICAR DATOS PERSONALES')]")
        ))
        self.assertIsNotNone(boton_modificar)

        # Buscar el botón de "MARCAR"
        boton_marcar = self.browser.find_element(By.XPATH, "//a[contains(text(), 'MARCAR')]")
        self.assertIsNotNone(boton_marcar)

        # Navegar a la página de marcado
        boton_marcar.click()
        
        # Verificar que llegamos a la página de marcado
        wait.until(EC.url_contains("marcado"))
        self.assertIn("Marcar Asistencia", self.browser.title)

    def test_logout(self):
        """
        Prueba el flujo de cierre de sesión.
        """
        self._login()

        wait = WebDriverWait(self.browser, 10)
        
        # Encontrar el enlace de Logout en el navbar
        logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
        logout_link.click()

        # Verificar que redirige al Home o que ya no muestra "Dashboard" en el menú
        # En tu views.py, signout renderiza 'home.html'
        
        # Esperamos ver el título del Home
        titulo_home = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'El Correo de Yuri')]")
        ))
        self.assertTrue(titulo_home.is_displayed())
        
        # Verificar que aparece "SignIn" nuevamente en el navbar o cuerpo
        signin_link = self.browser.find_element(By.LINK_TEXT, "SignIn")
        self.assertTrue(signin_link.is_displayed())