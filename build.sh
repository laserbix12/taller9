#!/usr/bin/env bash
# salir inmediatamente ante cualquier error
set -o errexit

pip install -r requirements.txt

# Entrenar el modelo de IA durante la fase de compilación
python modulo_ia/entrenar_modelo.py

python manage.py collectstatic --no-input
python manage.py migrate
