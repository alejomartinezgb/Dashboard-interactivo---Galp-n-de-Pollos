# Dashboard predictivo del galpón avícola (Finca San Quintín, Guayabal)

Proyecto de aula de Business Analytics, Universidad de Cundinamarca.
Integrantes: Yair Mora, Nicolas Martínez, Wilmer León, David Saavedra y Gabriel Charry.

Este dashboard es la continuación del informe predictivo del grupo. Usa la misma base de
datos, las mismas cinco variables y el mismo modelo (Random Forest de 100 árboles con
validación Leave-One-Out). No cambia nada de lo ya entregado: solo permite probar valores y
ver qué responde el modelo.

## Qué pregunta responde

¿Cuál será el peso promedio final (kg por ave) de un lote al cierre de su ciclo, y qué
conviene hacer con ese resultado (revisar el lote, venderlo antes o mantener el plan)?

## Qué se puede hacer en el dashboard

| Pestaña | Qué permite |
|---|---|
| Simulador | Cambiar raza, galpón, aves, bajas, alimento por ave, días de ciclo, días para el cierre y precio. Muestra el peso estimado, el escenario A/B/C, la acción recomendada y el dinero en juego. |
| Comparar escenarios | Pone lado a lado los tres escenarios de prueba y la simulación actual. |
| Qué tan confiable es | Muestra el error del modelo frente al promedio y qué variables pesan más. |
| Historial de lotes | Filtra por fecha, galpón y raza, y permite abrir el detalle de un lote (ventas y estimación) y llevarlo al simulador. |

## Estructura del proyecto

```
dashboard_galpon/
├── app.py                 # Interfaz (Streamlit)
├── build_db.py            # Convierte el .sql en la base SQLite
├── requirements.txt
├── .streamlit/config.toml # Colores del dashboard
├── data/
│   ├── galpon_avicola.sql # Base original (volcado de MariaDB)
│   └── galpon_avicola.db  # Base SQLite que lee el dashboard
└── src/
    ├── datos.py           # Conexión y consultas SQL (ETL)
    ├── modelo.py          # Modelo, validación y reglas de negocio
    ├── escenarios.py      # Los tres escenarios de prueba
    └── graficos.py        # Gráficas
```

## Cómo ejecutarlo en su computador

1. Instalar Python 3.10 o superior.
2. Abrir una terminal dentro de la carpeta del proyecto e instalar las librerías:
   ```
   pip install -r requirements.txt
   ```
3. Si la carpeta `data` no tiene el archivo `galpon_avicola.db`, crearlo con:
   ```
   python build_db.py
   ```
4. Abrir el dashboard:
   ```
   streamlit run app.py
   ```
   Se abre solo en el navegador, en la dirección http://localhost:8501.

La ruta de la base de datos es relativa a la carpeta del proyecto. Si se quiere usar otra
base, se puede definir la variable de entorno `GALPON_DB` con la ruta del archivo.

## Cómo ejecutarlo en Google Colab

En una celda nueva, después de subir la carpeta del proyecto al panel de archivos:

```
!pip install -q streamlit
!npm install -q localtunnel
!streamlit run app.py &>/content/log.txt &
!curl -s ipv4.icanhazip.com
!npx localtunnel --port 8501
```

El comando `curl` muestra una dirección IP; se copia y se pega como contraseña en la página
que abre el enlace de localtunnel.

## Qué tan confiable es el modelo

Con los 12 lotes finalizados, el Random Forest se equivoca unos 42 g por ave al estimar lotes
que no conocía, casi igual que predecir siempre el promedio (41 g). Por eso el dashboard
muestra siempre un margen de error de ± 0.04 kg y una segunda estimación con regresión
simple. Las estimaciones son una guía para el administrador, no un dato exacto.

## Datos y supuestos

* Datos: tablas `lote`, `seguimiento_peso`, `mortalidad`, `detalle_venta`, `venta` y `cliente`.
* Umbrales de decisión: menos de 2.45 kg (alerta A), 2.50 kg o más con al menos 2 días de
  anticipación (venta anticipada B), y el resto es rango normal (C).
* Precio de venta: $ 11.104 por kg (promedio de las 12 ventas). Concentrado: $ 1.912 por kg.
* Los lotes 13, 14 y 15 siguen en proceso y no tienen pesajes. Los escenarios de prueba usan
  valores hipotéticos de consumo para esos lotes.
