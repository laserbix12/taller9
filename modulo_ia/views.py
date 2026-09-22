# modulo_ia/views.py
import os
import joblib
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from drf_spectacular.utils import extend_schema, inline_serializer

# Cargar la ruta del modelo guardado
RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modelo_clasificacion.joblib')


class PredictIAView(APIView):
    permission_classes = [permissions.AllowAny]  # Permite consumo para pruebas públicas

    @extend_schema(
        summary="Inferencia de IA / Predicción de Riesgo",
        description="Recibe métricas del usuario y retorna una predicción procesada con Machine Learning.",
        request=inline_serializer(
            name="PredictInput",
            fields={
                'frecuencia_compra': serializers.IntegerField(default=5),
                'monto_promedio': serializers.FloatField(default=50000.0),
                'dias_ultima_compra': serializers.IntegerField(default=10)
            }
        ),
        responses={
            200: inline_serializer(
                name="PredictOutput",
                fields={
                    'prediccion': serializers.CharField(),
                    'codigo_riesgo': serializers.IntegerField(),
                    'probabilidad_riesgo': serializers.FloatField()
                }
            )
        }
    )
    def post(self, request):
        try:
            datos = request.data
            frecuencia = float(datos.get('frecuencia_compra', 0))
            monto = float(datos.get('monto_promedio', 0))
            dias = float(datos.get('dias_ultima_compra', 0))

            # Verificar si el modelo existe
            if not os.path.exists(RUTA_MODELO):
                return Response(
                    {"error": "El archivo del modelo de IA no se encuentra en el servidor."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            modelo = joblib.load(RUTA_MODELO)

            # Formatear la entrada para el modelo
            entrada = np.array([[frecuencia, monto, dias]])
            prediccion = modelo.predict(entrada)[0]
            probabilidades = modelo.predict_proba(entrada)[0]

            resultado_texto = (
                "Alto Riesgo de Abandono"
                if prediccion == 1
                else "Bajo Riesgo / Cliente Activo"
            )

            return Response({
                "status": "success",
                "prediccion": resultado_texto,
                "codigo_riesgo": int(prediccion),
                "probabilidad_riesgo": round(float(probabilidades[prediccion]), 4)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al procesar la inferencia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
