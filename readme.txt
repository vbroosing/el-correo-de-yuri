INSTALACIÓN
py -m venv venv
git init
git clone https://github.com/vbroosing/el-correo-de-yuri.git
cd venv/Scripts
.\activate
cd ../..
pip install django
pip install selenium
pip install webdriver_manager
py manage.py migrate

EJECUCIÓN
py manage.py runserver
py manage.py test app