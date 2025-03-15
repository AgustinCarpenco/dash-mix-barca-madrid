import pandas as pd
import os

def load_and_process_data():
    """
    Carga el archivo CSV y procesa los datos para su uso en el dashboard.
    """
    # Obtener la ruta absoluta del archivo CSV
    filepath = os.path.join(os.path.dirname(__file__), "Estadisticas_de_Partidos.csv")

    # Cargar el archivo CSV
    df = pd.read_csv(filepath)

    # Ver estructura
    print("Vista previa de los datos:\n", df.head())

    # Verificar valores nulos
    print("\nValores nulos por columna:\n", df.isnull().sum())

    # Reemplazar valores nulos con 0
    df.fillna(0, inplace=True)

    # Renombrar columnas para evitar problemas con espacios
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

    # Crear nuevas métricas
    df["total_goles"] = df["goles_local"] + df["goles_visitante"]
    df["promedio_goles_partido"] = df["total_goles"] / df["promedio_de_goles"]

    # Ver cambios
    print("\nDatos procesados:\n", df.head())

    return df
