from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    return psycopg2.connect(
        dbname="cryptoflow",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def generate_graph(monnaie: str, duree: str):
    conn = get_db_connection()
    query = """
    SELECT timestamp, price_usd FROM crypto_prices 
    WHERE LOWER(crypto_name) = LOWER(%s) AND timestamp >= NOW() - INTERVAL %s 
    ORDER BY timestamp;
    """
    df = pd.read_sql(query, conn, params=[monnaie.upper(), duree])
    conn.close()
    
    if df.empty:
        return None

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 7))

    primary_color = "#00ff88"
    background_color = "#1E1E1E"
    grid_color = "#444"
    text_color = "white"

    plt.plot(df['timestamp'], df['price_usd'], label=monnaie.upper(), color=primary_color, linewidth=2.5, alpha=0.9)
    plt.title(f"{monnaie.upper()} - Prix en USD", fontsize=14, fontweight='bold', color=text_color, pad=20)
    plt.xlabel("Date", fontsize=12, color=text_color)
    plt.ylabel("Prix (USD)", fontsize=12, color=text_color)
    plt.xticks(rotation=30, fontsize=10, color=text_color)
    plt.yticks(fontsize=10, color=text_color)
    plt.gca().set_facecolor(background_color)
    plt.gcf().set_facecolor(background_color)
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7, color=grid_color)
    legend = plt.legend()
    frame = legend.get_frame()
    frame.set_facecolor(background_color)
    frame.set_edgecolor(text_color)
    for text in legend.get_texts():
        text.set_color(text_color)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor=background_color)
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return img_base64

@app.get("/graph")
def graph(request: Request, monnaie: str = Query(...), duree: str = Query("7 days")):
    img_base64 = generate_graph(monnaie, duree)
    if not img_base64:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Aucune donnée trouvée."})
    return templates.TemplateResponse("index.html", {"request": request, "image": img_base64})