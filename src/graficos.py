# -*- coding: utf-8 -*-
"""
graficos.py  -  Graficas del dashboard (matplotlib).

Cada funcion recibe datos ya calculados y devuelve una figura. Se usan pocas
graficas y colores fijos para que el mensaje se entienda rapido:
azul = Random Forest, naranja = regresion simple / validacion, gris = promedio,
rojo = alerta de bajo peso, verde = peso objetivo.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

from src.modelo import BANDA_ERROR, UMBRAL_ALTO, UMBRAL_BAJO

AZUL, NARANJA, GRIS = "#1e3a8a", "#E67E22", "#7F8C8D"
ROJO, VERDE, TEAL = "#C0392B", "#1E8449", "#0d9488"

# Usa Arial si esta instalada; si no, una fuente equivalente.
_DISPONIBLES = {f.name for f in fm.fontManager.ttflist}
_FUENTE = next((f for f in ("Arial", "Liberation Sans", "DejaVu Sans") if f in _DISPONIBLES),
               "sans-serif")

plt.rcParams.update({
    "font.family": _FUENTE,
    "font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#222222", "axes.labelcolor": "#111111",
    "xtick.color": "#111111", "ytick.color": "#111111", "text.color": "#111111",
})


def fig_posicion(peso_rf: float, peso_simple: float, pesos_hist: np.ndarray):
    """Donde cae el peso estimado frente a los 12 lotes ya vendidos y las zonas A, C y B."""
    fig, ax = plt.subplots(figsize=(7, 3.2))
    lo, hi = 2.36, 2.60
    ax.axvspan(lo, UMBRAL_BAJO, color=ROJO, alpha=.13)
    ax.axvspan(UMBRAL_BAJO, UMBRAL_ALTO, color=GRIS, alpha=.13)
    ax.axvspan(UMBRAL_ALTO, hi, color=VERDE, alpha=.13)
    for x, t, c in [((lo + UMBRAL_BAJO) / 2, "A: revisar", ROJO),
                    ((UMBRAL_BAJO + UMBRAL_ALTO) / 2, "C: normal", "#444444"),
                    ((UMBRAL_ALTO + hi) / 2, "B: vender", VERDE)]:
        ax.text(x, 1.5, t, ha="center", color=c, fontsize=9,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=.85), zorder=6)
    # lotes historicos (apilados cuando se repiten)
    vistos = {}
    for w in np.round(pesos_hist, 3):
        vistos[w] = vistos.get(w, 0) + 1
        ax.scatter(w, 0.18 * vistos[w], s=55, color=GRIS, alpha=.8, zorder=3)
    ax.scatter([], [], s=55, color=GRIS, label="Lotes ya vendidos")
    # banda y estimaciones
    ax.axvspan(peso_rf - BANDA_ERROR, peso_rf + BANDA_ERROR, ymin=.0, ymax=.78,
               color=AZUL, alpha=.15, label="Margen de error (±0.04 kg)")
    ax.axvline(peso_rf, color=AZUL, lw=3, label=f"Random Forest: {peso_rf:.3f} kg")
    ax.axvline(peso_simple, color=NARANJA, lw=2.5, ls="--", label=f"Regresión simple: {peso_simple:.3f} kg")
    ax.set_xlim(lo, hi); ax.set_ylim(0, 1.65); ax.set_yticks([])
    ax.set_xlabel("Peso promedio por ave (kg)")
    ax.set_title("¿Dónde cae el peso estimado?")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.28), ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    return fig


def fig_sensibilidad(curva, etiqueta: str, valor_actual: float, peso_actual: float):
    """Como cambia el peso estimado si se mueve una sola variable y las demas quedan fijas."""
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.axhspan(2.30, UMBRAL_BAJO, color=ROJO, alpha=.10)
    ax.axhspan(UMBRAL_ALTO, 2.65, color=VERDE, alpha=.10)
    ax.plot(curva["valor"], curva["rf"], color=AZUL, lw=2.6, label="Random Forest")
    ax.plot(curva["valor"], curva["simple"], color=NARANJA, lw=2, ls="--", label="Regresión simple")
    ax.axhline(UMBRAL_BAJO, color=ROJO, lw=1, ls=":")
    ax.axhline(UMBRAL_ALTO, color=VERDE, lw=1, ls=":")
    ax.scatter([valor_actual], [peso_actual], s=110, color=AZUL, zorder=5, edgecolor="white")
    ax.annotate("Tu lote", (valor_actual, peso_actual), textcoords="offset points",
                xytext=(8, 10), fontsize=9, color=AZUL)
    ax.set_ylim(2.40, 2.58)
    ax.set_xlabel(etiqueta); ax.set_ylabel("Peso estimado (kg por ave)")
    ax.set_title("Qué pasa si cambia una sola variable")
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    ax.grid(alpha=.3)
    fig.tight_layout()
    return fig


def fig_escenarios(nombres, pesos_rf, pesos_simple):
    """Compara el peso estimado de varios escenarios contra los umbrales."""
    x = np.arange(len(nombres)); w = .36
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.axhspan(2.40, UMBRAL_BAJO, color=ROJO, alpha=.10)
    ax.axhspan(UMBRAL_ALTO, 2.56, color=VERDE, alpha=.10)
    b1 = ax.bar(x - w / 2, pesos_rf, w, color=AZUL, label="Random Forest")
    b2 = ax.bar(x + w / 2, pesos_simple, w, color=NARANJA, label="Regresión simple")
    ax.errorbar(x - w / 2, pesos_rf, yerr=BANDA_ERROR, fmt="none", ecolor="#111", capsize=4, lw=1.3)
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, 2.405, f"{b.get_height():.3f}", ha="center",
                va="bottom", fontsize=8, color="white")
    ax.axhline(UMBRAL_BAJO, color=ROJO, lw=1.2, ls=":"); ax.axhline(UMBRAL_ALTO, color=VERDE, lw=1.2, ls=":")
    ax.text(len(nombres) - .45, UMBRAL_BAJO - .003, "2.45 kg", color=ROJO, fontsize=8, ha="right", va="top")
    ax.text(len(nombres) - .45, UMBRAL_ALTO + .002, "2.50 kg", color=VERDE, fontsize=8, ha="right")
    ax.set_xticks(x); ax.set_xticklabels(nombres, fontsize=9)
    ax.set_ylim(2.40, 2.56); ax.set_ylabel("Peso estimado (kg por ave)")
    ax.set_title("Peso estimado en cada escenario")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    fig.tight_layout()
    return fig


def fig_validacion(tabla):
    """Error (MAE) de cada enfoque en validacion Leave-One-Out. Menos es mejor."""
    nombres = [n.replace(" (", "\n(") for n in tabla.index]
    vals = tabla["mae_loo"].values * 1000          # gramos
    base = tabla["mae_loo"].iloc[0] * 1000
    colores = [GRIS, NARANJA, AZUL, TEAL]
    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(nombres, vals, color=colores)
    ax.axhline(base, color=ROJO, lw=1.5, ls="--", label="Línea base: predecir siempre el promedio")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + .6, f"{v:.0f} g", ha="center", fontsize=9)
    ax.set_ylabel("Error promedio (gramos por ave)")
    ax.set_title("Error al estimar lotes que el modelo no conocía")
    ax.set_ylim(0, max(vals) * 1.25)
    ax.tick_params(axis="x", labelsize=8)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def fig_importancia(imp):
    """Que variables pesan mas dentro del Random Forest."""
    fig, ax = plt.subplots(figsize=(7, 3.8))
    imp = imp.tail(6)
    ax.barh(imp.index, imp.values, color=TEAL)
    for i, v in enumerate(imp.values):
        ax.text(v + .005, i, f"{v:.2f}", va="center", fontsize=9)
    ax.set_xlabel("Importancia relativa (suma = 1)")
    ax.set_title("Qué datos pesan más en la estimación")
    ax.grid(axis="x", alpha=.3)
    fig.tight_layout()
    return fig


def fig_historial(df):
    """Peso final de cada lote vendido, coloreado segun la zona de las reglas."""
    fig, ax = plt.subplots(figsize=(7, 3.6))
    colores = [ROJO if p < UMBRAL_BAJO else (VERDE if p >= UMBRAL_ALTO else GRIS)
               for p in df["peso_final_kg"]]
    ax.bar(df["id_lote"].astype(str), df["peso_final_kg"], color=colores)
    ax.axhline(UMBRAL_BAJO, color=ROJO, lw=1.2, ls=":"); ax.axhline(UMBRAL_ALTO, color=VERDE, lw=1.2, ls=":")
    ax.axhline(df["peso_final_kg"].mean(), color=AZUL, lw=1.5, ls="--",
               label=f"Promedio: {df['peso_final_kg'].mean():.2f} kg")
    ax.set_ylim(2.30, 2.60)
    ax.set_xlabel("Número de lote"); ax.set_ylabel("Peso final (kg por ave)")
    ax.set_title("Peso final de cada lote vendido")
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    fig.tight_layout()
    return fig
