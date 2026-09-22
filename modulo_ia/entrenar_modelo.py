# modulo_ia/entrenar_modelo.py
import os
import sys
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Asegurar compatibilidad de caracteres UTF-8 (emojis) en terminales de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def entrenar_y_guardar_modelo():
    """Entrena un modelo Random Forest para clasificar el riesgo de abandono de clientes

    y lo guarda en formato binario .joblib.
    """
    # 1. Datos de entrenamiento simulados: [frecuencia_compra, monto_promedio, dias_ultima_compra]
    # Ej: Clasificación de Riesgo de Cliente / Abandono (0: Riesgo Bajo, 1: Riesgo Alto)
    X = np.array([
        [15, 150000, 2],   # Cliente activo y recurrente
        [12, 120000, 5],   # Cliente activo
        [2,   15000, 45],  # Cliente inactivo / Riesgo Alto
        [1,   10000, 60],  # Cliente inactivo / Riesgo Alto
        [20, 200000, 1],   # Cliente VIP
        [3,   25000, 30],  # Cliente en riesgo
    ])

    # Etiquetas (0 - Bajo Riesgo, 1 - Alto Riesgo)
    y = np.array([0, 0, 1, 1, 0, 1])

    # 2. Entrenar el clasificador Random Forest
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    clf.fit(X, y)

    # 3. Guardar el modelo en un archivo binario .joblib
    ruta_guardado = os.path.join(os.path.dirname(__file__), 'modelo_clasificacion.joblib')
    joblib.dump(clf, ruta_guardado)
    print(f"✅ Modelo de IA entrenado y guardado exitosamente en: {ruta_guardado}")


if __name__ == '__main__':
    entrenar_y_guardar_modelo()
