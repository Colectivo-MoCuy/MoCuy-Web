# generar_dossier.py
# Versión actualizada: incorpora datos de Jonathan / La JomPa y paleta C
import os
import json
from jinja2 import Template
import pandas as pd

OUT_DIR = "."
EXCEL_PATH = "presupuesto_integrado_suenos_despiertos.xlsx"

# ---------------- Data (actualizados con tu info) ----------------
TITLE = "El País de los Sueños Despiertos"

# descripción/sinopsis
descripcion = ("El País de los Sueños Despiertos es una experiencia escénica inmersiva "
               "que integra danza, realidad virtual e inteligencia artificial. La obra "
               "invita a niños y niñas a explorar mundos oníricos donde la tierra, la energía "
               "y el cuerpo se entrelazan en formas simbólicas y poéticas.")

objetivo_general = ("Promover el desarrollo de la creatividad e imaginación infantil mediante "
                    "la integración entre arte y tecnología, generando experiencias lúdicas, "
                    "seguras y sensoriales que conecten el movimiento corporal con paisajes virtuales y colectivos.")

objetivos = [
    "Diseñar actividades interactivas que combinen recursos tecnológicos y expresiones artísticas para estimular la participación activa de los niños.",
    "Fomentar el uso consciente y creativo de herramientas digitales como medios de expresión y descubrimiento personal.",
    "Evaluar el impacto del proyecto en el fortalecimiento de la imaginación, la curiosidad y la capacidad de creación en los participantes."
]

# créditos y equipo
CREDITS = {
    "Dirección y creación": "Jonathan Xavier Pallo Ávila (La JomPa)",
    "Música": "Marcelo",
    "Diseño visual": "Fernanda Lara",
    "Concepto tecnológico": "Jonathan Pallo",
    "Intérpretes": "Melany Sancan, Laysing Chin, Dante Mullo, Andrew Mora",
    "Producción": "Jonathan Pallo, Uartes",
    "Colaboradores": "—"
}

# contacto
CONTACT = {
    "email": "3l.j0m.pa@gmail.com",
    "instagram": "@la_jompa",
    "telefono": "+5930978967253"
}

# presupuesto por defecto (si no hay excel)
budget_default = {
    "Área Artística": 7140,
    "Área Técnica": 4500,
    "Equipamiento": 5190,
    "Producción y Logística": 3550
}
total_default = sum(budget_default.values())

# cronograma por defecto
cronograma_fases = [
    {"fase":"Fase 1: Exploración e investigación","duracion":"Mes 1-6","descripcion":"Investigación, pruebas y diseño inicial","responsables":"Dirección + equipo artístico y técnico","resultado":"Bases conceptuales definidas"},
    {"fase":"Fase 2: Creación y composición escénica","duracion":"Mes 7-12","descripcion":"Desarrollo coreográfico, animación 3D y programación IA","responsables":"Todo el equipo","resultado":"Prototipo y escenas compuestas"},
    {"fase":"Fase 3: Integración, montaje y estreno","duracion":"Mes 13-18","descripcion":"Montaje técnico, ensayos y presentación final","responsables":"Todo el equipo","resultado":"Obra final presentada y evaluada"},
]

cronograma_semanal = [
    {"Semana":"1","Actividad":"Investigación conceptual y estética","Responsables":"Dirección y equipo artístico","Meta":"Referentes investigados","Estado":"Planeado"},
    {"Semana":"7","Actividad":"Exploración corporal y sensorial","Responsables":"Intérpretes y dirección","Meta":"Secuencias iniciales","Estado":"Planeado"},
    {"Semana":"13","Actividad":"Pruebas iniciales de VR e IA","Responsables":"Equipo técnico","Meta":"Dispositivos configurados","Estado":"Planeado"},
    {"Semana":"25","Actividad":"Composición coreográfica y digital","Responsables":"Dirección, intérpretes y técnicos","Meta":"Escenas en borrador","Estado":"Planeado"},
    {"Semana":"31","Actividad":"Modelado y animación 3D","Responsables":"Artista 3D / VR","Meta":"Ambientes en desarrollo","Estado":"Planeado"},
    {"Semana":"49","Actividad":"Montaje escénico y técnico","Responsables":"Dirección + técnicos","Meta":"Sistemas funcionando","Estado":"Planeado"},
    {"Semana":"61","Actividad":"Estreno y mediación con público infantil","Responsables":"Producción + mediación","Meta":"Presentación al público","Estado":"Planeado"},
]

# ---------------- Read excel if exists ----------------
def read_budget_from_excel(path):
    try:
        df = pd.read_excel(path, sheet_name=None)
    except Exception:
        return None, None, None
    budget = {}
    sheet_name = None
    for name in df.keys():
        if 'totales' in name.lower():
            sheet_name = name
            break
    if sheet_name is None:
        sheet_name = list(df.keys())[0]
    sheet = df[sheet_name]
    for idx, row in sheet.iterrows():
        first = str(row.iloc[0]) if not pd.isna(row.iloc[0]) else ""
        if not first:
            continue
        for key in budget_default.keys():
            if key.lower() in first.lower():
                val = row.iloc[1] if len(row) > 1 else 0
                try:
                    budget[key] = float(val)
                except:
                    budget[key] = budget_default[key]
    if not budget:
        return None, None, None
    total = sum(budget.values())
    return budget, total, sheet

# ---------------- Templates (igual que antes, texto central actualizado) ----------------
HTML_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{{ title }}</title>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="print.css" media="print">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="hero-inner">
        <h1>{{ title }}</h1>
        <p class="subtitle">Proyecto interdisciplinario — danza, VR, IA y artes visuales</p>
        <p class="byline"><strong>Dirección y creación:</strong> {{ director }}</p>
      </div>
    </section>

    <section id="descripcion" class="panel">
      <h2>Descripción General</h2>
      <p>{{ descripcion }}</p>
    </section>

    <section id="objetivos" class="panel">
      <h2>Objetivo General</h2>
      <p>{{ objetivo_general }}</p>
      <h3>Objetivos Específicos</h3>
      <ul>
        {% for o in objetivos %}
        <li>{{ o }}</li>
        {% endfor %}
      </ul>
    </section>

    <section id="cronograma" class="panel">
      <h2>Cronograma (Fases)</h2>
      <div class="table-wrap">
        <table class="fases">
          <thead><tr><th>Fase</th><th>Duración</th><th>Descripción</th><th>Responsables</th><th>Resultado esperado</th></tr></thead>
          <tbody>
          {% for f in cronograma_fases %}
            <tr>
              <td>{{ f.fase }}</td><td>{{ f.duracion }}</td><td>{{ f.descripcion }}</td><td>{{ f.responsables }}</td><td>{{ f.resultado }}</td>
            </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>

      <h3>Cronograma Semanal (extracto)</h3>
      <div class="table-wrap">
        <table class="semanal">
          <thead><tr><th>Semana</th><th>Actividad</th><th>Responsables</th><th>Meta</th><th>Estado</th></tr></thead>
          <tbody>
          {% for s in cronograma_semanal %}
            <tr>
              <td>{{ s.Semana }}</td><td>{{ s.Actividad }}</td><td>{{ s.Responsables }}</td><td>{{ s.Meta }}</td><td>{{ s.Estado }}</td>
            </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
    </section>

    <section id="presupuesto" class="panel">
      <h2>Desglose Presupuestal</h2>
      <div class="budget-wrap">
        <div id="chart_presupuesto" class="chart"></div>
        <div class="budget-table">
          <table class="budget">
            <thead><tr><th>Área</th><th>Total (USD)</th></tr></thead>
            <tbody>
            {% for k,v in presupuesto.items() %}
              <tr><td>{{ k }}</td><td>${{ "{:,.2f}".format(v) }}</td></tr>
            {% endfor %}
            <tr class="total"><td><strong>TOTAL GENERAL</strong></td><td><strong>${{ "{:,.2f}".format(total_general) }}</strong></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="alcance" class="panel">
      <h2>Alcance estimado de público</h2>
      <p>Estimación: 800 - 1500 espectadores en la primera etapa; talleres y funciones en centros educativos y festivales.</p>
      <div id="chart_alcance" class="chart small"></div>
    </section>

    <section id="equipo" class="panel">
      <h2>Equipo y Créditos</h2>
      <ul>
        {% for k,v in credits.items() %}
          <li><strong>{{ k }}:</strong> {{ v }}</li>
        {% endfor %}
      </ul>
    </section>

    <section id="contacto" class="panel">
      <h2>Contacto</h2>
      <p>Email: {{ contact.email }}</p>
      <p>Instagram: {{ contact.instagram }}</p>
      {% if contact.telefono %}<p>Teléfono: {{ contact.telefono }}</p>{% endif %}
    </section>

    <footer class="site-footer">
      <p>Generated: {{ fecha }}</p>
    </footer>
  </main>

  <script>
    window.DOSSIER_DATA = {
      "presupuesto": {{ presupuesto_json|safe }},
      "total_general": {{ total_general }},
      "alcance": {"Centros educativos":45,"Familias":30,"Festivales y espacios":15,"Instituciones/ONGs":10}
    };
  </script>
  <script src="script.js"></script>
</body>
</html>
"""

# ---------------- CSS actualizado (paleta C: mezcla azul-frío + violeta suave) ----------------
CSS_CONTENT = """
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&family=Lato:wght@300;400;700&display=swap');

:root{
  --bg:#0f1724; /* azul muy oscuro */
  --panel:#181a2a;
  --accent:#6A5FBF; /* violeta suave */
  --muted:#A69DDF;
  --accent2:#4aa3d8; /* cian / acento frío */
  --soft:#CFF2F8;
  --text:#EAE8F9;
  --glass: rgba(255,255,255,0.03);
}

*{box-sizing:border-box}
html,body{height:100%;margin:0;font-family:'Lato',sans-serif;background:linear-gradient(180deg,#0b0e18 0%, #151b2a 60%), url('assets/fondo.png') center/cover no-repeat fixed; color:var(--text); -webkit-font-smoothing:antialiased;}
.page{max-width:1000px;margin:0 auto;padding:40px;}
.hero{padding:120px 20px;border-radius:12px;text-align:center;background:linear-gradient(180deg, rgba(20,22,35,0.45), rgba(16,18,30,0.35));backdrop-filter: blur(4px);}
.hero h1{font-family:'Cinzel Decorative', serif;font-size:44px;margin:0;color:var(--muted);letter-spacing:1px}
.hero .subtitle{margin-top:10px;color:var(--soft);font-size:16px}
.hero .byline{margin-top:12px;color:var(--accent2);font-weight:600}

.panel{margin:36px 0;padding:26px;border-radius:10px;background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));box-shadow:0 6px 18px rgba(5,8,20,0.6);border:1px solid rgba(255,255,255,0.03)}
.panel h2{font-family:'Cinzel Decorative', serif;color:var(--accent);margin-top:0}
.panel p, .panel li{color:var(--text);line-height:1.5}

.table-wrap{overflow:auto}
.fases, .semanal, .budget{width:100%;border-collapse:collapse}
.fases th, .semanal th, .budget th{background:rgba(106,95,191,0.12);padding:8px;text-align:left;font-weight:700}
.fases td, .semanal td, .budget td{padding:8px;border-top:1px solid rgba(255,255,255,0.03)}
.budget-wrap{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
.chart{flex:1 1 420px;height:320px;background:transparent}
.chart.small{height:240px}
.budget-table{flex:0 0 320px}

.total td{border-top:2px solid rgba(255,255,255,0.06)}

.site-footer{padding:18px;text-align:center;opacity:0.85;color:var(--muted);font-size:13px}

/* responsive */
@media (max-width:900px){
  .page{padding:20px}
  .hero{padding:80px 20px}
  .budget-wrap{flex-direction:column}
}
"""

SCRIPT_JS = """
document.addEventListener('DOMContentLoaded', function(){
  const data = window.DOSSIER_DATA || {};
  const presupuesto = data.presupuesto || {};
  const total = data.total_general || 0;

  const labels = Object.keys(presupuesto);
  const values = labels.map(l => presupuesto[l]);

  const pieData = [{ type:'pie', labels: labels, values: values, textinfo:'label+percent', hoverinfo:'label+value', marker:{line:{color:'#0f1724',width:1}} }];
  const pieLayout = { margin:{t:10,b:10,l:10,r:10}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', legend:{font:{color:'#EAE8F9'}} };
  Plotly.newPlot('chart_presupuesto', pieData, pieLayout, {responsive:true});

  const aLabels = Object.keys(data.alcance || {});
  const aValues = aLabels.map(k => data.alcance[k]);
  const alcData = [{ type:'pie', labels:aLabels, values:aValues, textinfo:'label+percent' }];
  const alcLayout = { margin:{t:10,b:10,l:10,r:10} };
  Plotly.newPlot('chart_alcance', alcData, alcLayout, {responsive:true});
});
"""

PRINT_CSS = """
@page { size: A4; margin: 12mm; }
html,body{background:white !important;color:#1D1A33 !important}
.page{max-width:170mm;margin:0 auto;padding:10mm;background:white}
.hero{padding:20mm 10mm;border-radius:4mm;background:white;box-shadow:none}
.panel{background:white;border: none;box-shadow:none;padding:6mm}
.hero h1{color:#2F275A}
.panel h2{color:#433D7B}
.chart{page-break-inside:avoid}
table{color:#1D1A33}
.site-footer{color:#666;opacity:1}
"""

# --------------- Renderizar y escribir archivos ---------------
def render_all():
    presupuesto = budget_default.copy()
    total_gen = total_default
    b, total_x, sheet = read_budget_from_excel(EXCEL_PATH)
    if b:
        presupuesto = b
        total_gen = total_x

    presupuesto_json = json.dumps(presupuesto)

    html = Template(HTML_TEMPLATE).render(
        title=TITLE,
        descripcion=descripcion,
        objetivo_general=objetivo_general,
        objetivos=objetivos,
        cronograma_fases=cronograma_fases,
        cronograma_semanal=cronograma_semanal,
        presupuesto=presupuesto,
        presupuesto_json=presupuesto_json,
        total_general=total_gen,
        fecha=pd.Timestamp.now().strftime("%Y-%m-%d"),
        director=CREDITS["Dirección y creación"],
        credits=CREDITS,
        contact=CONTACT
    )

    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(OUT_DIR, "styles.css"), "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT)
    with open(os.path.join(OUT_DIR, "script.js"), "w", encoding="utf-8") as f:
        f.write(SCRIPT_JS)
    with open(os.path.join(OUT_DIR, "print.css"), "w", encoding="utf-8") as f:
        f.write(PRINT_CSS)

    print("Archivos generados: index.html, styles.css, script.js, print.css")
    print("Coloca tu imagen de fondo en: assets/fondo.png (crea carpeta assets y pon la imagen allí).")

if __name__ == "__main__":
    render_all()