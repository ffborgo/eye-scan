import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter

# Ubicación de la carpeta con los archivos CSV
folder_path = "/content/drive/MyDrive/Cosas de la facu/Experimentos Cuanticos II/datos TPFinal EC2/15G/OM3-corta"
file_names = ["1000mV-TR31-NoDFE.csv", "134mV-TR31-NoDFE.csv", "1000mV-TR7-NoDFE.csv", "523mV-TR31-NoDFE.csv"]
output_folder = folder_path

# Configuración de parámetros del heatmap
start_marker = "Scan Start"
end_marker = "Scan End"
sigma = 1

# Iterar sobre los archivos y procesar los datos
for file_name in file_names:
    data = []
    start_found = False
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r") as file:
        for line in file:
            if start_marker in line:
                start_found = True
                continue
            if end_marker in line:
                break
            if start_found and not line.startswith("2d statistical"):
                values = line.strip().split(",")[1:]  # Se omiten los valores de la primera columna
                data.append(values)

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Convertir las columnas numéricas a tipo float
    df = df.apply(pd.to_numeric)

    # Aplicar suavizado al DataFrame utilizando un filtro gaussiano
    df_smooth = gaussian_filter(df, sigma=sigma)

    # Ajustar el tamaño de la figura y la relación de aspecto del mapa de calor
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_aspect("auto")

    # Crear un mapa de calor (heatmap) utilizando seaborn con los datos suavizados y la paleta de colores "Crest"
    heatmap = sns.heatmap(df_smooth, cmap="coolwarm", cbar=False, linewidths=0, linecolor='white', annot=False, ax=ax)

#    plt.title(f"Heatmap suavizado de los datos extraídos - {file_name}", fontsize=16)
    plt.axis('off')  # Eliminar los ejes y los números de las filas y columnas

    # Agregar la colorbar
    cbar = heatmap.figure.colorbar(heatmap.collections[0])
    cbar.set_label("Profundidad", fontsize=12)

    # Guardar la imagen en la carpeta de salida
    output_file = "ojo15.png"  # Nombre del archivo de imagen
    output_path = os.path.join(output_folder, output_file)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

    plt.show()
