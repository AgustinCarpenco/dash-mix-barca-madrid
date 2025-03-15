import pandas as pd
import os

def load_and_process_data():
    """
    Carga el archivo CSV y procesa los datos para su uso en el dashboard.
    """
    # Obtener la ruta absoluta del archivo CSV
    filepath = os.path.join(os.path.dirname(__file__), "data", "Estadisticas_de_Partidos.csv")

    # Verificar si el archivo existe
    if not os.path.exists(filepath):
        print(f"⚠️ Error: No se encontró el archivo {filepath}")
        return None

    # Cargar el archivo CSV
    df = pd.read_csv(filepath)

    # Mostrar las primeras filas para verificar estructura
    print("Vista previa de los datos:\n", df.head())

    # Renombrar columnas para evitar problemas con espacios
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

    # Verificar si las columnas esperadas están presentes
    required_columns = {"goles_local", "goles_visitante", "promedio_de_goles"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"⚠️ Error: Faltan las columnas {missing_columns} en el archivo CSV.")
        return None

    # Crear nuevas métricas
    df["total_goles"] = df["goles_local"] + df["goles_visitante"]
    df["promedio_goles_partido"] = df["total_goles"] / df["promedio_de_goles"]

    # Ver cambios
    print("\nDatos procesados:\n", df.head())

    return df

# Ejecutar solo si este script se ejecuta directamente
if __name__ == "__main__":
    df = load_and_process_data()
    if df is not None:
        print("\n✅ Procesamiento de datos completado con éxito.")

