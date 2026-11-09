# -*- coding: utf-8 -*-
"""
app.py  -  Dashboard interactivo "Simulando predicciones"
Galpón avícola, Finca San Quintín (Guayabal).

Este archivo solo arma la pantalla. La lectura de datos esta en src/datos.py,
el modelo y las reglas en src/modelo.py, los escenarios en src/escenarios.py
y las graficas en src/graficos.py.

Ejecutar:  streamlit run app.py
"""
import numpy as np
import pandas as pd
import streamlit as st

from src import datos, escenarios, graficos, modelo

st.set_page_config(page_title="Simulador de peso | San Quintín", page_icon="🐔",
                   layout="wide")

# ----------------------------------------------------------------------------
# Estilo: paleta azul y verde azulado de la finca, letra Arial
# ----------------------------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"], .stMarkdown, label, button { font-family: Arial, sans-serif !important; }
.encabezado { background: linear-gradient(135deg,#1e3a8a,#1e293b); color:#fff;
              padding:18px 24px; border-radius:8px; margin-bottom:12px; }
.encabezado h1 { color:#fff; font-size:26px; margin:0; }
.encabezado p { color:#e2e8f0; margin:4px 0 0 0; font-size:14px; }
</style>
<div class="encabezado">
  <h1>Simulador del peso final de un lote</h1>
  <p>Finca San Quintín (Guayabal) · Escriba los datos de un lote y vea el peso estimado,
  qué conviene hacer y cuánto dinero está en juego.</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Carga de datos y entrenamiento (se hace una sola vez y se guarda en memoria)
# ----------------------------------------------------------------------------
@st.cache_data
def cargar():
    """Lee la base de datos SQLite y devuelve las tablas que usa el dashboard."""
    return (datos.cargar_lotes_finalizados(), datos.cargar_lotes_en_proceso(),
            datos.cargar_ventas())


@st.cache_resource
def entrenar(df):
    """Entrena los cuatro enfoques del informe (Random Forest, lineal, simple y base)."""
    return modelo.entrenar_todo(df)


try:
    df, en_proceso, ventas = cargar()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

ent = entrenar(df)
RF = "Random Forest (5 variables)"
mae_rf = ent["tabla"].loc[RF, "mae_loo"] * 1000
mae_base = ent["tabla"].iloc[0]["mae_loo"] * 1000
peso_prom_hist = float(df["peso_final_kg"].mean())

RAZAS = sorted(df["raza"].unique())
GALPONES = sorted(df["ubicacion_galpon"].unique())

# ----------------------------------------------------------------------------
# Estado de los controles (permite cargar escenarios y lotes con un clic)
# ----------------------------------------------------------------------------
CLAVES = {"raza": "k_raza", "galpon": "k_galpon", "ingresadas": "k_ingresadas",
          "bajas": "k_bajas", "alimento": "k_alimento", "dias": "k_dias",
          "faltan": "k_faltan", "precio": "k_precio"}


def poner_valores(valores: dict) -> None:
    """Copia un diccionario de valores a los controles del simulador."""
    for campo, clave in CLAVES.items():
        st.session_state[clave] = valores[campo]


if "k_raza" not in st.session_state:
    poner_valores(escenarios.INICIAL)
    st.session_state["k_preset"] = escenarios.PERSONALIZADO


def al_elegir_escenario() -> None:
    """Callback: al elegir un escenario de prueba se llenan los controles."""
    nombre = st.session_state["k_preset"]
    if nombre in escenarios.ESCENARIOS:
        poner_valores(escenarios.ESCENARIOS[nombre])


def al_cambiar_manual() -> None:
    """Callback: si la persona mueve un control, el escenario pasa a 'Personalizado'."""
    st.session_state["k_preset"] = escenarios.PERSONALIZADO


def cargar_lote_historico(fila: dict) -> None:
    """Callback del boton del historial: lleva un lote real al simulador."""
    poner_valores({
        "raza": fila["raza"], "galpon": fila["ubicacion_galpon"],
        "ingresadas": int(fila["cantidad_inicial"]), "bajas": int(fila["bajas"]),
        "alimento": float(min(max(round(fila["alimento_por_ave_kg"], 2), 3.30), 3.55)),
        "dias": int(min(max(fila["dias_ciclo"], 40), 54)),
        "faltan": 3, "precio": st.session_state["k_precio"]})
    st.session_state["k_preset"] = escenarios.PERSONALIZADO


# ----------------------------------------------------------------------------
# Barra lateral: datos del lote
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("Datos del lote")
    st.selectbox("Escenario de prueba", [escenarios.PERSONALIZADO] + list(escenarios.ESCENARIOS),
                 key="k_preset", on_change=al_elegir_escenario,
                 help="Carga valores de ejemplo. Después puede cambiarlos a mano.")
    st.selectbox("Raza", RAZAS, key="k_raza", on_change=al_cambiar_manual)
    st.selectbox("Galpón", GALPONES, key="k_galpon", on_change=al_cambiar_manual)
    st.number_input("Aves ingresadas", min_value=40, max_value=80, step=1,
                    key="k_ingresadas", on_change=al_cambiar_manual)
    st.slider("Bajas (aves muertas)", 0, 6, key="k_bajas", on_change=al_cambiar_manual)
    st.slider("Alimento por ave (kg)", 3.30, 3.55, step=0.01, key="k_alimento",
              on_change=al_cambiar_manual)
    st.slider("Días de ciclo", 40, 54, key="k_dias", on_change=al_cambiar_manual)
    st.slider("Días que faltan para el cierre planificado", 0, 10, key="k_faltan",
              on_change=al_cambiar_manual)
    st.number_input("Precio de venta (COP por kg)", min_value=8000, max_value=15000,
                    step=100, key="k_precio", on_change=al_cambiar_manual)
    st.caption("Los rangos corresponden a lo observado en los 12 lotes vendidos. "
               "Fuera de ese rango el modelo no tiene experiencia.")
    st.sidebar.markdown("---")
    st.sidebar.caption("**Base conectada:** `data/galpon_avicola.db`")
    st.sidebar.caption("12 lotes finalizados | 3 en proceso")

# Valores actuales del simulador
p = {campo: st.session_state[clave] for campo, clave in CLAVES.items()}
if p["bajas"] >= p["ingresadas"]:
    st.error("Las bajas no pueden ser iguales o mayores a las aves ingresadas.")
    st.stop()
res = escenarios.evaluar_escenario(ent, p)
din = res["dinero"]

tab1, tab2, tab3, tab4 = st.tabs(["Simulador", "Comparar escenarios",
                                  "Qué tan confiable es", "Historial de lotes"])

# ============================================================================
# PESTAÑA 1: SIMULADOR
# ============================================================================
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Peso estimado por ave", f"{res['rf']:.3f} kg",
              delta=f"{res['rf'] - peso_prom_hist:+.3f} kg frente al promedio")
    c2.metric("Margen de error", f"± {modelo.BANDA_ERROR:.2f} kg",
              help="Error típico del modelo al estimar lotes que no conocía.")
    c3.metric("Ingreso esperado", f"$ {din['ingreso']:,.0f}".replace(",", "."),
              help="Peso estimado × aves vivas × precio por kg.")
    c4.metric("Mortalidad del lote", f"{res['tasa_mortalidad']:.1f} %",
              help="Bajas ÷ aves ingresadas. En la finca ha estado entre 2.2 % y 4.0 %.")

    nombre_esc = modelo.NOMBRES_ESCENARIO[res["escenario"]]
    if res["escenario"] == "A":
        st.error(f"**{nombre_esc}.** {res['accion']}")
    elif res["escenario"] == "B":
        st.success(f"**{nombre_esc}.** {res['accion']}")
    else:
        st.info(f"**{nombre_esc}.** {res['accion']}")
        if res["rf"] >= modelo.UMBRAL_ALTO and p["faltan"] < modelo.DIAS_ANTICIPO_B:
            st.caption("El peso llegó al objetivo, pero faltan menos de 2 días para el cierre; "
                       "por eso se mantiene la fecha de venta.")

    # Avisos de honestidad sobre el modelo
    if not modelo.combinacion_vista(df, p["raza"], p["galpon"]):
        st.warning("Esa raza nunca ha estado en ese galpón. El modelo no tiene datos de "
                   "esa combinación y su estimación es menos confiable.")
    if not (2.0 <= res["tasa_mortalidad"] <= 4.1):
        st.warning("La mortalidad está fuera del rango que ha visto el modelo (2.2 % a 4.0 %).")
    st.caption(f"Estimación orientativa. Al probar con lotes que no conocía, el Random Forest "
               f"se equivocó {mae_rf:.0f} g por ave y el promedio simple {mae_base:.0f} g, "
               f"así que se muestra también la regresión simple y el margen de error.")

    g1, g2 = st.columns(2)
    with g1:
        fig = graficos.fig_posicion(res["rf"], res["simple"], df["peso_final_kg"].values)
        st.pyplot(fig)
    with g2:
        etiquetas = {"Alimento por ave (kg)": ("alimento_por_ave_kg", np.arange(3.30, 3.5501, 0.01)),
                     "Días de ciclo": ("dias_ciclo", np.arange(40, 55, 1)),
                     "Mortalidad (%)": ("tasa_mortalidad", np.arange(2.0, 4.01, 0.1))}
        eleg = st.radio("Variable que se mueve en la gráfica", list(etiquetas), horizontal=True)
        var, rango = etiquetas[eleg]
        base = {"raza": p["raza"], "ubicacion_galpon": p["galpon"],
                "alimento_por_ave_kg": p["alimento"], "dias_ciclo": p["dias"],
                "tasa_mortalidad": res["tasa_mortalidad"]}
        curva = modelo.curva_sensibilidad(ent, base, var, rango)
        actual = {"alimento_por_ave_kg": p["alimento"], "dias_ciclo": p["dias"],
                  "tasa_mortalidad": res["tasa_mortalidad"]}[var]
        fig = graficos.fig_sensibilidad(curva, eleg, actual, res["rf"])
        st.pyplot(fig)

    with st.expander("Dinero en juego y compra de concentrado", expanded=True):
        fmt = lambda v: f"$ {v:,.0f}".replace(",", ".")
        tabla = pd.DataFrame({
            "Concepto": ["Ingreso esperado del lote",
                         "Ingreso si el peso real es 40 g menor",
                         "Ingreso si el peso real es 40 g mayor",
                         "Valor de un error de 50 g por ave en este lote",
                         "Concentrado necesario para el ciclo",
                         "Costo de ese concentrado",
                         "Costo de mantener el lote un día más",
                         "Ahorro de alimento si se vende antes de lo planificado"],
            "Valor": [fmt(din["ingreso"]), fmt(din["ingreso_bajo"]), fmt(din["ingreso_alto"]),
                      fmt(din["valor_50g"]), f"{din['concentrado_kg']:,.0f} kg".replace(",", "."),
                      fmt(din["concentrado_cop"]), fmt(din["costo_dia"]),
                      fmt(din["ahorro_adelanto"])]})
        st.dataframe(tabla, hide_index=True)
        st.caption("Supuestos del informe: concentrado a $ 1.912 por kg y un costo de alimento "
                   "de $ 7.745 por día para un lote de 55 aves.")

# ============================================================================
# PESTAÑA 2: COMPARAR ESCENARIOS
# ============================================================================
with tab2:
    st.subheader("Los tres escenarios de prueba y el lote que tiene en pantalla")
    filas, nombres, pesos_rf, pesos_s = [], [], [], []
    casos = dict(escenarios.ESCENARIOS)
    casos["Su simulación actual"] = p
    for nombre, valores in casos.items():
        r = escenarios.evaluar_escenario(ent, valores)
        corto = nombre.split(":")[0]
        filas.append({
            "Escenario": nombre, "Raza": valores["raza"].replace("Gallina ", ""),
            "Galpón": valores["galpon"].split(" - ")[0],
            "Alimento por ave (kg)": valores["alimento"], "Días de ciclo": valores["dias"],
            "Bajas": valores["bajas"], "Peso Random Forest (kg)": round(r["rf"], 3),
            "Peso regresión simple (kg)": round(r["simple"], 3),
            "Decisión": modelo.NOMBRES_ESCENARIO[r["escenario"]],
            "Ingreso esperado (COP)": f"{r['dinero']['ingreso']:,.0f}".replace(",", ".")})
        nombres.append(corto); pesos_rf.append(r["rf"]); pesos_s.append(r["simple"])
    st.dataframe(pd.DataFrame(filas), hide_index=True)
    fig = graficos.fig_escenarios(nombres, pesos_rf, pesos_s)
    st.pyplot(fig)
    st.caption("Las barras negras muestran el margen de error de ± 0.04 kg del Random Forest. "
               "Cuando una barra queda cerca de una línea punteada, la decisión es menos segura.")

# ============================================================================
# PESTAÑA 3: QUÉ TAN CONFIABLE ES
# ============================================================================
with tab3:
    st.subheader("Qué tan confiable es la estimación")
    st.write("Para saberlo se le pidió al modelo adivinar el peso de cada lote sin haberlo visto "
             "(validación Leave-One-Out). Es la prueba más honesta cuando solo hay 12 lotes.")
    k1, k2, k3 = st.columns(3)
    k1.metric("Error del Random Forest", f"{mae_rf:.0f} g por ave")
    k2.metric("Error de predecir siempre el promedio", f"{mae_base:.0f} g por ave")
    k3.metric("Error de la regresión simple",
              f"{ent['tabla'].iloc[3]['mae_loo'] * 1000:.0f} g por ave")
    g1, g2 = st.columns(2)
    with g1:
        fig = graficos.fig_validacion(ent["tabla"])
        st.pyplot(fig)
    with g2:
        fig = graficos.fig_importancia(ent["importancias"])
        st.pyplot(fig)
    st.info("**En simple:** con 12 lotes el modelo todavía no supera al promedio. Por eso la "
            "recomendación del informe es usar las alertas con revisión del administrador y "
            "empezar a pesar los lotes cada semana. El dato que más pesa es el alimento por ave.")
    tabla_t = ent["tabla"].copy()
    tabla_t.columns = ["Error en entrenamiento (kg)", "R² en entrenamiento",
                       "Error en validación (kg)", "R² en validación"]
    with st.expander("Ver la tabla completa de métricas"):
        st.dataframe(tabla_t.round(4))

# ============================================================================
# PESTAÑA 4: HISTORIAL DE LOTES
# ============================================================================
with tab4:
    st.subheader("Historial de los lotes vendidos")
    f1, f2, f3 = st.columns(3)
    f_min, f_max = df["fecha_ingreso"].min().date(), df["fecha_ingreso"].max().date()
    rango = f1.date_input("Fecha de ingreso del lote", value=(f_min, f_max),
                          min_value=f_min, max_value=f_max)
    gal_sel = f2.multiselect("Galpón", GALPONES, default=GALPONES)
    raza_sel = f3.multiselect("Raza", RAZAS, default=RAZAS)
    ini, fin = (rango[0], rango[1]) if isinstance(rango, (tuple, list)) and len(rango) == 2 \
        else (f_min, f_max)
    filtrado = df[(df["fecha_ingreso"].dt.date >= ini) & (df["fecha_ingreso"].dt.date <= fin)
                  & (df["ubicacion_galpon"].isin(gal_sel)) & (df["raza"].isin(raza_sel))]

    if filtrado.empty:
        st.warning("No hay lotes con esos filtros. Amplíe el rango de fechas o elija más opciones.")
    else:
        ind = datos.indicadores(filtrado, ventas)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Lotes", ind["lotes"])
        m2.metric("Aves criadas", ind["aves"])
        m3.metric("Mortalidad", f"{ind['mortalidad']:.1f} %")
        m4.metric("Peso promedio", f"{ind['peso_prom']:.2f} kg")
        m5.metric("Ventas", f"$ {ind['ventas']:,.0f}".replace(",", "."))
        fig = graficos.fig_historial(filtrado)
        st.pyplot(fig)

        st.markdown("**Detalle de un lote** (elija uno para ver sus ventas y cómo lo estimó el modelo)")
        ids = filtrado["id_lote"].tolist()
        lote_id = st.selectbox("Lote", ids, format_func=lambda i: f"Lote {i}")
        fila = filtrado[filtrado["id_lote"] == lote_id].iloc[0]
        pos = int(df.index[df["id_lote"] == lote_id][0])
        estimado = float(ent["resultados"][RF]["p_loo"][pos])
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Peso real", f"{fila['peso_final_kg']:.2f} kg")
        d2.metric("Estimado sin conocerlo", f"{estimado:.3f} kg",
                  delta=f"{estimado - fila['peso_final_kg']:+.3f} kg")
        d3.metric("Alimento por ave", f"{fila['alimento_por_ave_kg']:.2f} kg")
        d4.metric("Días de ciclo", f"{int(fila['dias_ciclo'])}")
        st.write(f"{fila['raza']} · {fila['ubicacion_galpon']} · "
                 f"ingresó el {fila['fecha_ingreso']:%d/%m/%Y} con {int(fila['cantidad_inicial'])} "
                 f"aves y tuvo {int(fila['bajas'])} bajas.")
        v = ventas[ventas["id_lote"] == lote_id][
            ["fecha_venta", "cliente", "tipo_cliente", "cantidad_aves", "peso_total_kg",
             "precio_kg", "total_venta"]].copy()
        v["fecha_venta"] = v["fecha_venta"].dt.strftime("%d/%m/%Y")
        v.columns = ["Fecha", "Cliente", "Tipo", "Aves", "Peso total (kg)", "Precio por kg",
                     "Total (COP)"]
        st.dataframe(v, hide_index=True)
        st.button("Llevar este lote al simulador", on_click=cargar_lote_historico,
                  args=(fila.to_dict(),))
        st.caption("Después de pulsar el botón, abra la pestaña Simulador para ver la estimación.")
