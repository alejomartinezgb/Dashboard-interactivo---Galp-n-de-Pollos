# -*- coding: utf-8 -*-
"""
escenarios.py  -  Tres escenarios de prueba y funcion para evaluarlos.

Los tres escenarios usan la raza y el galpon de los lotes que hoy figuran
"En Proceso" (13, 14 y 15) con valores hipoteticos de consumo, porque esos
lotes todavia no tienen pesajes registrados. Los tamanos de lote y las bajas
son los habituales de la finca. Sirven para probar como responde el modelo.
"""
from src import modelo

RAZA_C = "Gallina Criolla Pura"
RAZA_I = "Gallina Amarilla Isa Brown"
RAZA_L = "Gallina Blanca Lohmann"
G1 = "Galpón 1 - Pollitos"
G2 = "Galpón 2 - Producción"
G3 = "Galpón 3 - Venta"

ESCENARIOS = {
    "Escenario 1: poco alimento": dict(
        raza=RAZA_C, galpon=G2, ingresadas=55, bajas=2, alimento=3.30,
        dias=42, faltan=4, precio=modelo.PRECIO_KG),
    "Escenario 2: valores típicos": dict(
        raza=RAZA_I, galpon=G1, ingresadas=55, bajas=2, alimento=3.40,
        dias=45, faltan=3, precio=modelo.PRECIO_KG),
    "Escenario 3: buen consumo": dict(
        raza=RAZA_L, galpon=G3, ingresadas=60, bajas=2, alimento=3.53,
        dias=45, faltan=3, precio=modelo.PRECIO_KG),
}

# Valores con los que arranca el simulador
PERSONALIZADO = "Personalizado"
INICIAL = list(ESCENARIOS.values())[1]


def evaluar_escenario(entrenado: dict, p: dict) -> dict:
    """
    Recibe los valores del lote (diccionario con las claves de ESCENARIOS) y
    devuelve la estimacion, el escenario A/B/C, la accion y el dinero en juego.
    """
    vivas = p["ingresadas"] - p["bajas"]
    tasa = p["bajas"] / p["ingresadas"] * 100
    est = modelo.predecir(entrenado, p["raza"], p["galpon"], p["alimento"], p["dias"], tasa)
    esc = modelo.clasificar_escenario(est["rf"], p["faltan"])
    dinero = modelo.calcular_dinero(est["rf"], vivas, p["faltan"], p["precio"], p["alimento"])
    return {"aves_vivas": vivas, "tasa_mortalidad": tasa, "rf": est["rf"],
            "simple": est["simple"], "escenario": esc,
            "accion": modelo.accion_recomendada(esc), "dinero": dinero}
