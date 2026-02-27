import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cargar archivo usando ruta absoluta
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "data", "datos.csv")
df = pd.read_csv(file_path)

# Creamos una columna nueva para identificar reprobados
# Nota: Aquí generamos 'Reprobado' con R mayúscula
df['estado'] = df['calificacion'].apply(lambda x: 'Reprobado' if x < 6 else 'Aprobado')

print(df.info())

# Ver primeras filas
print(df.head())

# Ver valores nulos
print(df.isnull().sum())

# --- CORRECCIÓN AQUÍ ---
# Filtramos 'Reprobado' con R mayúscula para que coincida con la línea anterior
# Agrupamos por 'materia' como pediste
reprobacion = df[df['estado'] == 'Reprobado'].groupby('materia').size() / df.groupby('materia').size() * 100

# Ordenamos de mayor a menor
reprobacion = reprobacion.sort_values(ascending=False)

# Graficamos
reprobacion.head(5).plot(kind='bar', title='Top 5 Materias con Mayor Reprobación (%)')
plt.ylabel('Porcentaje (%)') # Añadimos etiqueta al eje Y
plt.savefig('grafico_reprobacion.png')
plt.close()

promedios_carrera = df.groupby('carrera')['calificacion'].mean().sort_values(ascending=False)
print(promedios_carrera)

# Gráfico de barras horizontales
sns.barplot(x=promedios_carrera.values, y=promedios_carrera.index)
plt.title('Promedio de Notas por Carrera')
plt.savefig('grafico_carreras.png')
plt.close()

tendencia = df.groupby('año')['calificacion'].mean()

tendencia.plot(kind='line', marker='o', title='Tendencia de Rendimiento Académico por Año')
plt.ylabel('Promedio General')
plt.savefig('grafico_tendencia.png')
plt.close()

# Ejemplo: Alumnos con más de 2 materias reprobadas en el último año
# Se cambió a 2024 porque es el último año disponible en los datos
riesgo = df[(df['estado'] == 'Reprobado') & (df['año'] == 2024)].groupby('id_estudiante').size()
alumnos_riesgo = riesgo[riesgo > 2]

# Corrección ortográfica: "académico"
print(f"Alerta: {len(alumnos_riesgo)} estudiantes en riesgo académico crítico en 2024.")
