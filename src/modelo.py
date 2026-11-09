# -*- coding: utf-8 -*-
"""
modelo.py  -  Modelo predictivo y reglas de negocio.

Reproduce exactamente lo que ya se hizo en el informe predictivo:
  * Pregunta: cual sera el peso promedio final (kg por ave) de un lote.
  * 5 variables: alimento por ave, raza, galpon, dias de ciclo, tasa de mortalidad.
  * Random Forest de 100 arboles (random_state=42) y validacion Leave-One-Out.
  * Comparacion contra la linea base y contra la regresion lineal simple.
  * Reglas de decision A, B y C (umbrales 2.45 kg y 2.50 kg).

No usa Streamlit ni matplotlib: se puede probar por separado.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# ---- Variables (igual que el informe) --------------------------------------
CAT = ["raza", "ubicacion_galpon"]
NUM = ["alimento_por_ave_kg", "dias_ciclo", "tasa_mortalidad"]
OBJETIVO = "peso_final_kg"

# ---- Reglas y supuestos economicos tomados del informe ----------------------
UMBRAL_BAJO = 2.45        # menos de esto: alerta de bajo peso (escenario A)
UMBRAL_ALTO = 2.50        # desde esto: peso objetivo alcanzado (escenario B)
BANDA_ERROR = 0.04        # margen de error tipico en validacion (kg por ave)
PRECIO_KG = 11104         # COP por kg, promedio de las 12 ventas
COSTO_ALIMENTO_DIA_AVE = 7745 / 55   # COP por ave por dia (7.745 por lote de 55 aves)
PRECIO_CONCENTRADO_KG = 1912   # COP por kg de concentrado (compras registradas)
DIAS_ANTICIPO_B = 2       # la regla B exige al menos 2 dias de anticipacion

NOMBRES_ESCENARIO = {
    "A": "A. Alerta de bajo peso",
    "B": "B. Peso objetivo alcanzado",
    "C": "C. Peso en rango normal",
}


def crear_pipeline(modelo, cat=CAT, num=NUM) -> Pipeline:
    """One-Hot para las variables de texto; las numericas pasan sin cambios."""
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), cat),
        ("num", "passthrough", num)])
    return Pipeline([("pre", pre), ("modelo", modelo)])


def evaluar(pipe: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    """Metricas en entrenamiento (optimistas) y en Leave-One-Out (honestas)."""
    pipe.fit(X, y)
    p_tr = pipe.predict(X)
    p_loo = cross_val_predict(pipe, X, y, cv=LeaveOneOut())
    return dict(mae_tr=mean_absolute_error(y, p_tr), r2_tr=r2_score(y, p_tr),
                mae_loo=mean_absolute_error(y, p_loo), r2_loo=r2_score(y, p_loo),
                p_tr=p_tr, p_loo=p_loo)


def entrenar_todo(df: pd.DataFrame) -> dict:
    """
    Entrena los cuatro enfoques del informe y devuelve modelos y metricas.

    Claves del resultado: modelos (pipelines ya entrenados), resultados
    (metricas por enfoque), importancias (Series) y tabla (DataFrame).
    """
    X, y = df[CAT + NUM], df[OBJETIVO]
    modelos = {
        "Línea base (promedio)": (DummyRegressor(), X),
        "Regresión lineal (5 variables)": (crear_pipeline(LinearRegression()), X),
        "Random Forest (5 variables)": (
            crear_pipeline(RandomForestRegressor(n_estimators=100, random_state=42)), X),
        "Regresión lineal simple (alimento/ave)": (
            crear_pipeline(LinearRegression(), [], ["alimento_por_ave_kg"]),
            X[["alimento_por_ave_kg"]]),
    }
    resultados = {n: evaluar(m, Xi, y) for n, (m, Xi) in modelos.items()}
    tabla = pd.DataFrame({n: {k: r[k] for k in ["mae_tr", "r2_tr", "mae_loo", "r2_loo"]}
                          for n, r in resultados.items()}).T

    rf = modelos["Random Forest (5 variables)"][0]
    nombres = [n.split("__")[1].replace("raza_", "").replace("ubicacion_galpon_", "")
               for n in rf["pre"].get_feature_names_out()]
    imp = pd.Series(rf["modelo"].feature_importances_, index=nombres).sort_values()
    return {"modelos": {n: m for n, (m, _) in modelos.items()},
            "resultados": resultados, "tabla": tabla, "importancias": imp}


def predecir(entrenado: dict, raza: str, galpon: str, alimento: float,
             dias: int, tasa_mortalidad: float) -> dict:
    """
    Estima el peso final de un lote con el Random Forest (modelo principal) y
    con la regresion simple (segunda opinion). Devuelve kg por ave.
    """
    fila = pd.DataFrame([{"raza": raza, "ubicacion_galpon": galpon,
                          "alimento_por_ave_kg": alimento, "dias_ciclo": dias,
                          "tasa_mortalidad": tasa_mortalidad}])
    rf = entrenado["modelos"]["Random Forest (5 variables)"].predict(fila[CAT + NUM])[0]
    simple = entrenado["modelos"]["Regresión lineal simple (alimento/ave)"].predict(
        fila[["alimento_por_ave_kg"]])[0]
    return {"rf": float(rf), "simple": float(simple)}


def clasificar_escenario(peso: float, dias_para_cierre: int) -> str:
    """
    Reglas del informe:
      A: peso < 2.45 kg
      B: peso >= 2.50 kg y faltan al menos 2 dias para el cierre planificado
      C: cualquier otro caso (rango normal, o 2.50+ sin anticipacion suficiente)
    """
    if peso < UMBRAL_BAJO:
        return "A"
    if peso >= UMBRAL_ALTO and dias_para_cierre >= DIAS_ANTICIPO_B:
        return "B"
    return "C"


def accion_recomendada(escenario: str) -> str:
    """Texto de la accion de negocio para cada escenario (Tabla 13 del informe)."""
    return {
        "A": ("Revisar el lote hoy mismo: pesar una muestra, revisar el consumo de "
              "alimento por ave, las bajas y el ambiente. Posponer la entrega solo si "
              "se espera recuperar más de 50 g por ave en 4 días."),
        "B": ("Suspender el concentrado los últimos 2 días, adelantar la venta y avisar "
              "con tiempo a los clientes de mayor volumen (Pollo Fresco y Frigorífico "
              "del Norte)."),
        "C": ("Mantener el plan de alimentación y la fecha de venta, y seguir "
              "registrando el pesaje."),
    }[escenario]


def calcular_dinero(peso: float, aves_vivas: int, dias_para_cierre: int = 0,
                    precio_kg: float = PRECIO_KG, alimento_ave: float = 0.0) -> dict:
    """Ingreso esperado del lote y los valores economicos que usa el informe."""
    ingreso = peso * aves_vivas * precio_kg
    return {
        "concentrado_kg": alimento_ave * aves_vivas,
        "concentrado_cop": alimento_ave * aves_vivas * PRECIO_CONCENTRADO_KG,
        "ingreso": ingreso,
        "ingreso_bajo": (peso - BANDA_ERROR) * aves_vivas * precio_kg,
        "ingreso_alto": (peso + BANDA_ERROR) * aves_vivas * precio_kg,
        "costo_dia": COSTO_ALIMENTO_DIA_AVE * aves_vivas,
        "ahorro_adelanto": COSTO_ALIMENTO_DIA_AVE * aves_vivas * dias_para_cierre,
        "valor_50g": 0.05 * aves_vivas * precio_kg,
    }


def combinacion_vista(df: pd.DataFrame, raza: str, galpon: str) -> bool:
    """True si esa raza ya estuvo alguna vez en ese galpon (hay historial)."""
    return bool(((df["raza"] == raza) & (df["ubicacion_galpon"] == galpon)).any())


def curva_sensibilidad(entrenado: dict, base: dict, variable: str,
                       valores: np.ndarray) -> pd.DataFrame:
    """
    Cambia UNA variable en un rango y deja las demas fijas, para ver como
    responde la prediccion. variable: 'alimento_por_ave_kg', 'dias_ciclo'
    o 'tasa_mortalidad'.
    """
    filas = []
    for v in valores:
        d = dict(base)
        d[variable] = v
        p = predecir(entrenado, d["raza"], d["ubicacion_galpon"],
                     d["alimento_por_ave_kg"], d["dias_ciclo"], d["tasa_mortalidad"])
        filas.append({"valor": v, "rf": p["rf"], "simple": p["simple"]})
    return pd.DataFrame(filas)
