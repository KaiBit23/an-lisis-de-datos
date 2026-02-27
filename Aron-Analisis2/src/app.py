from flask import Flask, render_template
import pandas as pd
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "datos.csv")

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, "src", "templates"))

def get_stats():
    # Cargar y procesar datos
    df = pd.read_csv(DATA_PATH)
    
    # 1. Cálculos de resumen
    avg_grade = df['calificacion'].mean()
    fail_rate = (df['calificacion'] < 6).mean() * 100
    at_risk_count = len(df[df['calificacion'] < 6])
    
    # 2. Top materias con mayor reprobación
    subjects = df[df['calificacion'] < 6].groupby('materia').size() / df.groupby('materia').size() * 100
    top_subjects = subjects.sort_values(ascending=False).head(5).items()
    
    # 3. Promedio por carrera
    careers_avg = df.groupby('carrera')['calificacion'].mean().sort_values(ascending=False).items()
    
    # 4. Lista de alumnos en riesgo (primeros 5)
    at_risk_list = df[df['calificacion'] < 6].sort_values('calificacion').head(5).to_dict('records')
    
    return {
        'avg_grade': f"{avg_grade:.2f}",
        'fail_rate': f"{fail_rate:.1f}",
        'at_risk_count': f"{at_risk_count:02d}",
        'top_subjects': top_subjects,
        'careers_avg': careers_avg,
        'at_risk_list': at_risk_list
    }

@app.route("/")
def index():
    stats = get_stats()
    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
