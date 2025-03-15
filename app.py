import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 📌 Ruta al archivo CSV
CSV_PATH = "/Users/agustin/Documents/Agustin_2025/Master en Python/Modulo_9/Actividad colaborativa/dash-mix-barca-madrid/data/Estadisticas_de_Partidos.csv"

# 📌 Cargar los datos locales
df = pd.read_csv(CSV_PATH)

# 📌 Normalizar los nombres de las columnas
df.columns = df.columns.str.strip()

# 📌 Convertir la columna de fecha a formato datetime
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# 📌 Verificar y convertir columnas numéricas
columnas_numericas = ["Goles Local", "Goles Visitante", "Promedio de Goles"]
for col in columnas_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 📌 Lista de equipos únicos
equipos_disponibles = ["Todos"] + df["Equipo"].unique().tolist()

# 📌 Crear la app de Dash
app = dash.Dash(__name__)
server = app.server  # Para despliegue

# 📌 Diseño de la aplicación
app.layout = html.Div([
    html.H1("📊 Estadísticas de Partidos", style={"textAlign": "center", "color": "#333"}),

    # 📌 Filtro de equipo
    html.Div([
        html.Label("Selecciona un equipo:", style={"fontSize": "18px", "marginRight": "10px"}),
        dcc.Dropdown(
            id="equipo-dropdown",
            options=[{"label": equipo, "value": equipo} for equipo in equipos_disponibles],
            value="Todos",
            clearable=False,
            style={"width": "50%", "marginBottom": "20px"}
        ),
    ], style={"textAlign": "center"}),

    # 📊 Gráfico de Promedio de Goles por Fecha
    dcc.Graph(id="promedio-goles"),

    # 📊 Gráfico de Total de Goles Locales vs Visitantes
    dcc.Graph(id="total-goles"),
])

# 📌 Callbacks para actualizar gráficos dinámicamente
@app.callback(
    [Output("promedio-goles", "figure"),
     Output("total-goles", "figure")],
    [Input("equipo-dropdown", "value")]
)
def actualizar_graficos(equipo_seleccionado):
    # 📌 Filtrar datos según el equipo seleccionado
    if equipo_seleccionado != "Todos":
        df_filtrado = df[df["Equipo"] == equipo_seleccionado]
    else:
        df_filtrado = df

    # 📊 **Gráfico de Promedio de Goles por Fecha**
    fig_promedio_goles = px.line(
        df_filtrado,
        x="Fecha",
        y="Promedio de Goles",
        title="📈 Promedio de Goles por Fecha",
        labels={"Promedio de Goles": "Promedio por Partido", "Fecha": "Fecha"},
        line_shape="spline",
        color_discrete_sequence=["#1f77b4"]
    )
    fig_promedio_goles.update_layout(xaxis_title="Fecha", yaxis_title="Promedio de Goles", template="plotly_white")

    # 📊 **Gráfico de Total de Goles Locales vs Visitantes**
    total_goles = pd.DataFrame({
        "Condición": ["Local", "Visitante"],
        "Total de Goles": [df_filtrado["Goles Local"].sum(), df_filtrado["Goles Visitante"].sum()]
    })
    
    fig_total_goles = px.bar(
        total_goles,
        x="Condición",
        y="Total de Goles",
        text="Total de Goles",
        title="⚽ Total de Goles Locales vs Visitantes",
        labels={"Total de Goles": "Goles Totales", "Condición": "Condición"},
        color="Condición",
        color_discrete_map={"Local": "#2E86C1", "Visitante": "#E74C3C"}
    )
    fig_total_goles.update_traces(textposition="outside")
    fig_total_goles.update_layout(template="plotly_white")

    return fig_promedio_goles, fig_total_goles


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
