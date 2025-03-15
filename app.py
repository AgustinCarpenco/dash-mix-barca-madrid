import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
server = app.server  # Para despliegue en plataformas como Render o AWS

# 📌 Cargar los datos
df_barcelona = pd.read_csv("data/barcelona_stats.csv")
df_madrid = pd.read_csv("data/real_madrid_stats.csv")

# Agregar columna de "Club" para poder filtrar en conjunto
df_barcelona["Club"] = "Barcelona"
df_madrid["Club"] = "Real Madrid"

# Combinar ambos DataFrames
df = pd.concat([df_barcelona, df_madrid], ignore_index=True)

# 📌 Layout del Dashboard
app.layout = html.Div([
    html.H1("📊 Dashboard de Estadísticas de Barcelona y Real Madrid", style={"textAlign": "center"}),

    # Filtro de equipo
    html.Label("Selecciona un equipo:"),
    dcc.Dropdown(
        id="equipo-dropdown",
        options=[
            {"label": "Barcelona", "value": "Barcelona"},
            {"label": "Real Madrid", "value": "Real Madrid"},
            {"label": "Ambos", "value": "Ambos"}
        ],
        value="Ambos",
        clearable=False
    ),

    # 📊 Gráfico de Goles y Asistencias
    dcc.Graph(id="goles-asistencias"),

    # 📊 Gráfico de Disparos y Precisión de Pases
    dcc.Graph(id="disparos-pases"),
])

# 📌 Callbacks para actualizar gráficos dinámicamente
@app.callback(
    [Output("goles-asistencias", "figure"),
     Output("disparos-pases", "figure")],
    [Input("equipo-dropdown", "value")]
)
def actualizar_graficos(equipo_seleccionado):
    # Filtrar datos según el equipo seleccionado
    if equipo_seleccionado == "Barcelona":
        df_filtrado = df[df["Club"] == "Barcelona"]
    elif equipo_seleccionado == "Real Madrid":
        df_filtrado = df[df["Club"] == "Real Madrid"]
    else:
        df_filtrado = df  # Ambos equipos

    # 📊 Gráfico de Goles y Asistencias
    fig_goles_asistencias = px.bar(
        df_filtrado.sort_values("Goles", ascending=False),
        x="Nombre", y=["Goles", "Asistencias"],
        title="⚽ Goles y Asistencias por Jugador",
        labels={"value": "Cantidad", "variable": "Estadística"},
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # 📊 Gráfico de Disparos por Partido y Precisión de Pases
    fig_disparos_pases = px.scatter(
        df_filtrado,
        x="Disparos por Partido", y="Precisión de Pases (%)",
        size="Goles", color="Club",
        title="🎯 Precisión de Pases vs Disparos por Partido",
        hover_name="Nombre",
        color_discrete_map={"Barcelona": "blue", "Real Madrid": "red"}
    )

    return fig_goles_asistencias, fig_disparos_pases

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
