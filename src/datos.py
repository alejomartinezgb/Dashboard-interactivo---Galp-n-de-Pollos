# -*- coding: utf-8 -*-
"""
datos.py  -  Capa de datos (ETL) del dashboard.

Aqui solo se lee la base de datos SQLite y se arman las tablas que usan
el modelo y el dashboard. No hay graficas ni logica de interfaz.

La ruta de la base es relativa al proyecto (data/galpon_avicola.db). Si se
quiere usar otra ruta, se puede definir la variable de entorno GALPON_DB.
"""
import os
import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_BD = Path(os.environ.get("GALPON_DB", RAIZ / "data" / "galpon_avicola.db"))

# Las 5 variables del modelo se calculan con SQL, igual que en el informe predictivo.
QUERY_LOTES = """
SELECT l.id_lote, l.fecha_ingreso, l.cantidad_inicial, l.raza, l.ubicacion_galpon,
       sp.fecha AS fecha_cierre,
       sp.peso_promedio AS peso_final_kg,
       sp.cantidad_viva AS aves_vivas,
       sp.alimento_consumido / sp.cantidad_viva AS alimento_por_ave_kg,
       CAST(julianday(sp.fecha) - julianday(l.fecha_ingreso) AS INTEGER) AS dias_ciclo,
       (SELECT COALESCE(SUM(m.cantidad), 0) FROM mortalidad m
         WHERE m.id_lote = l.id_lote) AS bajas,
       (SELECT COALESCE(SUM(m.cantidad), 0) FROM mortalidad m
         WHERE m.id_lote = l.id_lote) * 100.0 / l.cantidad_inicial AS tasa_mortalidad
FROM lote l
JOIN seguimiento_peso sp ON sp.id_lote = l.id_lote
WHERE l.estado = 'Finalizado'
ORDER BY l.id_lote;
"""

QUERY_PROCESO = """
SELECT id_lote, fecha_ingreso, cantidad_inicial, raza, ubicacion_galpon
FROM lote WHERE estado = 'En Proceso' ORDER BY id_lote;
"""

QUERY_VENTAS = """
SELECT dv.id_lote, v.fecha AS fecha_venta, c.nombre AS cliente, c.tipo_cliente,
       dv.cantidad_aves, dv.peso_total_kg, dv.precio_kg, v.total AS total_venta
FROM detalle_venta dv
JOIN venta v   ON v.id_venta = dv.id_venta
JOIN cliente c ON c.id_cliente = v.id_cliente
ORDER BY dv.id_lote;
"""


def conectar() -> sqlite3.Connection:
    """Abre la conexion a la base. Da un error claro si el archivo no existe."""
    if not RUTA_BD.exists():
        raise FileNotFoundError(
            f"No se encontro la base de datos en {RUTA_BD}. "
            "Ejecute primero:  python build_db.py")
    return sqlite3.connect(RUTA_BD)


def cargar_lotes_finalizados() -> pd.DataFrame:
    """Una fila por lote finalizado (12 filas) con las 5 variables del modelo."""
    con = conectar()
    try:
        df = pd.read_sql_query(QUERY_LOTES, con, parse_dates=["fecha_ingreso", "fecha_cierre"])
    finally:
        con.close()
    df["galpon"] = df["ubicacion_galpon"].str.extract(r"(Galpón \d)")
    return df


def cargar_lotes_en_proceso() -> pd.DataFrame:
    """Lotes 13 a 15, que todavia no tienen pesaje de cierre."""
    con = conectar()
    try:
        df = pd.read_sql_query(QUERY_PROCESO, con, parse_dates=["fecha_ingreso"])
    finally:
        con.close()
    return df


def cargar_ventas() -> pd.DataFrame:
    """Ventas por lote y cliente (para el detalle de cada lote)."""
    con = conectar()
    try:
        df = pd.read_sql_query(QUERY_VENTAS, con, parse_dates=["fecha_venta"])
    finally:
        con.close()
    return df


def indicadores(df: pd.DataFrame, ventas: pd.DataFrame) -> dict:
    """Indicadores del resumen del negocio para los lotes que se le pasen."""
    ids = set(df["id_lote"])
    v = ventas[ventas["id_lote"].isin(ids)]
    aves = int(df["cantidad_inicial"].sum())
    bajas = int(df["bajas"].sum())
    return {
        "lotes": len(df),
        "aves": aves,
        "bajas": bajas,
        "mortalidad": (bajas / aves * 100) if aves else 0.0,
        "peso_prom": float(df["peso_final_kg"].mean()) if len(df) else 0.0,
        "dias_prom": float(df["dias_ciclo"].mean()) if len(df) else 0.0,
        "ventas": float(v["total_venta"].sum()),
    }
