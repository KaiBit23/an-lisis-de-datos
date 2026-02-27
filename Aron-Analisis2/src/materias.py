import pandas as pd
import json
import os

def procesar_datos():
    # Rutas de archivos - Ajustadas para ejecución desde src/
    input_path = os.path.join("..", "data", "datos_rendimiento_universidad.csv")
    output_csv_path = os.path.join("..", "data", "resultado_rendimiento.csv")
    output_json_path = os.path.join("..", "static", "dashboard_data.json")

    # Cargar archivo
    if not os.path.exists(input_path):
        print(f"Error: No se encuentra el archivo {input_path}")
        return

    df = pd.read_csv(input_path)
    
    # --- LIMPIEZA Y CONVERSIÓN DE TIPOS ---
    # Convertir 'calificacion' a numérico
    df['calificacion'] = pd.to_numeric(df['calificacion'], errors='coerce')
    # Convertir 'año' a numérico si existe
    if 'año' in df.columns:
        df['año'] = pd.to_numeric(df['año'], errors='coerce')
    
    # Eliminar nulos en columnas críticas
    df = df.dropna(subset=['calificacion', 'materia', 'carrera'])

    # Creamos una columna nueva para identificar reprobados
    df['estado'] = df['calificacion'].apply(lambda x: 'Reprobado' if x < 6 else 'Aprobado')

    # Guardar CSV modificado
    df.to_csv(output_csv_path, index=False)
    print(f"CSV modificado guardado en: {output_csv_path}")

    # --- Generar Estadísticas para el Dashboard ---
    
    # 1. Promedio General
    promedio_general = round(df['calificacion'].mean(), 2)

    # 2. Tasa de reprobación total
    tasa_reprobacion_total = round((df['estado'] == 'Reprobado').sum() / len(df) * 100, 1)

    # 3. Materias con mayor reprobación
    counts = df.groupby('materia').size()
    repro_counts = df[df['estado'] == 'Reprobado'].groupby('materia').size()
    reprobacion_materias = (repro_counts / counts * 100).fillna(0)
    
    top_reprobacion = reprobacion_materias.sort_values(ascending=False).head(5).to_dict()
    top_reprobacion_lista = [{"nombre": k, "porcentaje": round(v, 1)} for k, v in top_reprobacion.items()]

    # 4. Promedio por carrera
    promedios_carrera = df.groupby('carrera')['calificacion'].mean().sort_values(ascending=False).to_dict()
    promedios_carrera_lista = [{"carrera": k, "promedio": round(v, 1)} for k, v in promedios_carrera.items()]

    # 5. Estudiantes en riesgo (calificación < 6)
    estudiantes_riesgo = df[df['calificacion'] < 6].sort_values(by='calificacion').head(10)[['id_estudiante', 'carrera', 'materia', 'calificacion']].to_dict(orient='records')

    # 6. Tendencia por año
    if 'año' in df.columns:
        tendencia_anual = df.groupby('año')['calificacion'].mean().sort_index().to_dict()
        tendencia_lista = [{"año": int(k) if not pd.isna(k) else "N/A", "promedio": round(v, 2)} for k, v in tendencia_anual.items()]
    else:
        tendencia_lista = []

    # Consolidar datos
    dashboard_data = {
        "stats": {
            "promedio_general": promedio_general,
            "tasa_reprobacion": tasa_reprobacion_total,
            "estudiantes_riesgo_count": len(df[df['calificacion'] < 6])
        },
        "top_reprobacion": top_reprobacion_lista,
        "promedios_carrera": promedios_carrera_lista,
        "estudiantes_riesgo": estudiantes_riesgo,
        "tendencia": tendencia_lista
    }

    # Guardar JSON para el frontend
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=4, ensure_ascii=False)
    
    print(f"Datos del dashboard guardados en: {output_json_path}")

if __name__ == "__main__":
    procesar_datos()
