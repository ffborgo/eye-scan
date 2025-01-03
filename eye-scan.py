import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter

# Ubicación de la carpeta con los archivos CSV
folder_path = "/datos"
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

    # Verificar si hay datos para procesar
    if len(data) > 0:
        # Crear un DataFrame con los datos
        df = pd.DataFrame(data)
        df = df.apply(pd.to_numeric, errors='coerce')  # Asegura que los datos no numéricos se conviertan en NaN

        # Aplicar suavizado al DataFrame utilizando un filtro gaussiano
        df_smooth = gaussian_filter(df, sigma=sigma)

        # Ajustar el tamaño de la figura y la relación de aspecto del mapa de calor
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.set_aspect("auto")

        # Crear un mapa de calor (heatmap) utilizando seaborn
        heatmap = sns.heatmap(df_smooth, cmap="coolwarm", cbar=False, linewidths=0, linecolor='white', annot=False, ax=ax)

        # Eliminar los ejes
        plt.axis('off')

        # Agregar la colorbar
        cbar = heatmap.figure.colorbar(heatmap.collections[0])
        cbar.set_label("Profundidad", fontsize=12)

        # Guardar la imagen en la carpeta de salida
        output_file = f"{file_name.split('.')[0]}_heatmap.png"
        output_path = os.path.join(output_folder, output_file)
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

        plt.show()
        plt.close()
    else:
        print(f"El archivo {file_name} está vacío o no contiene datos válidos.")
        continue  # Saltar al siguiente archivo
