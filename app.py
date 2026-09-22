"""Punto de entrada compatible para despliegues como Render (gunicorn app:app).
"""
from config.wsgi import application

# Render a menudo busca 'app' por defecto al iniciar gunicorn
app = application
