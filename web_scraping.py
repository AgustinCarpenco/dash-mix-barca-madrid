import requests
import pandas as pd
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URLs de WhoScored para cada equipo
URLS = {
    "Barcelona": "https://www.whoscored.com/teams/65/archive/spain-barcelona?stageId=17702",
    "Real Madrid": "https://www.whoscored.com/teams/52/archive/spain-real-madrid?stageId=17702"
}

# Configurar opciones de Chrome para Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

def scrape_team_stats(team_name, url):
    """
    Usa Selenium para extraer la tabla de estadísticas del equipo desde WhoScored.

    Args:
        team_name (str): Nombre del equipo.
        url (str): URL de la página de estadísticas.

    Returns:
        pd.DataFrame: DataFrame con las estadísticas del equipo.
    """
    print(f"🔄 Abriendo navegador para {team_name}...")

    # Inicializar WebDriver con WebDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Esperar a que cargue la página

        # Buscar la tabla de estadísticas
        try:
            table = driver.find_element(By.XPATH, "/html/body/div[4]/div[6]")
        except:
            print(f"⚠️ No se encontró la tabla de {team_name}.")
            return None

        # Obtener los encabezados de la tabla
        headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
        print(f"📌 Encabezados obtenidos para {team_name}: {headers} (Total: {len(headers)})")

        # Obtener filas de la tabla
        rows = table.find_elements(By.TAG_NAME, "tr")

        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                data.append([col.text.strip() for col in cols])

        # Convertir a DataFrame con los encabezados
        df = pd.DataFrame(data, columns=headers)

        print(f"✅ Datos extraídos de {team_name} correctamente.")
        return df

    finally:
        driver.quit()  # Cerrar el navegador

def clean_team_stats(df, team_name):
    """
    Limpia y estructura los datos extraídos de WhoScored.

    Args:
        df (pd.DataFrame): DataFrame con los datos crudos.
        team_name (str): Nombre del equipo.

    Returns:
        pd.DataFrame: DataFrame limpio y estructurado.
    """
    # 🔹 Ver los nombres de las columnas extraídas
    print(f"📌 Columnas obtenidas para {team_name}: {df.columns.tolist()} (Total: {len(df.columns)})")

    # Definir nombres correctos de columnas
    column_names = [
        "Jugador", "Altura (cm)", "Peso (kg)", "Partidos", "Minutos", 
        "Goles", "Asistencias", "Tarjetas Amarillas", "Tarjetas Rojas", 
        "Disparos por Partido", "Precisión de Pases (%)", "Duelos Aéreos Ganados", 
        "Hombre del Partido", "Calificación WhoScored"
    ]

    # Ajustar nombres de columnas si la tabla tiene más columnas de lo esperado
    if len(df.columns) > len(column_names):
        df = df.iloc[:, :len(column_names)]  # Tomar solo las primeras columnas
    elif len(df.columns) < len(column_names):
        print(f"⚠️ {team_name} tiene menos columnas de las esperadas. Verifica la tabla.")

    # Asignar los nombres de las columnas
    df.columns = column_names[:len(df.columns)]

    # 📌 **Separar nombre, edad y posición**
    jugador_info = df["Jugador"].str.extract(r'(?P<Numero>\d+)\s+(?P<Nombre>.+?)\s+(?P<Edad>\d+),\s*(?P<Posicion>.+)')
    
    # Fusionar los nuevos valores en el DataFrame
    df = pd.concat([jugador_info, df], axis=1)

    # Eliminar la columna original "Jugador"
    df.drop(columns=["Jugador", "Numero"], inplace=True)

    # Convertir valores numéricos correctamente
    numeric_cols = ["Edad", "Altura (cm)", "Peso (kg)", "Partidos", "Minutos", "Goles", 
                    "Asistencias", "Tarjetas Amarillas", "Tarjetas Rojas", 
                    "Disparos por Partido", "Precisión de Pases (%)", 
                    "Duelos Aéreos Ganados", "Hombre del Partido", "Calificación WhoScored"]
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Convierte y pone NaN si hay errores

    # Reemplazar "-" por 0 en columnas numéricas
    df.fillna(0, inplace=True)

    # Agregar la columna de equipo
    df["Equipo"] = team_name

    return df

def save_team_stats():
    """
    Guarda las estadísticas de Barcelona y Real Madrid en archivos CSV.
    """
    os.makedirs("data", exist_ok=True)

    all_data = []

    for team, url in URLS.items():
        df = scrape_team_stats(team, url)
        if df is not None:
            # LIMPIAR LOS DATOS
            df = clean_team_stats(df, team)

            all_data.append(df)
            filepath = f"data/{team.lower().replace(' ', '_')}_stats.csv"
            df.to_csv(filepath, index=False)
            print(f"✅ Estadísticas de {team} guardadas en '{filepath}'.")
        
        time.sleep(5)  # Esperar entre solicitudes para evitar bloqueos

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        df_all.to_csv("data/la_liga_2019_2020_stats.csv", index=False)
        print("✅ Estadísticas combinadas guardadas en 'data/la_liga_2019_2020_stats.csv'.")

if __name__ == "__main__":
    save_team_stats()
