# Patrimonio Vivo

Requiere Python 3.13 y [uv](https://docs.astral.sh/uv/getting-started/installation/). Ejecutar desde la carpeta que contiene `manage.py`.

## Instalar dependencias

```powershell
uv venv --python 3.13 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## Configurar la base de datos

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py loaddata datos_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
```

La base de datos SQLite se crea en `db.sqlite3`. `loaddata` carga las categorías y los lugares de ejemplo.

## Ejecutar la aplicación

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Aplicación: <http://127.0.0.1:8000/>. Administración: <http://127.0.0.1:8000/admin/>.
