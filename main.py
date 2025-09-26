from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import threading, random, time
from capture import start_sniff, trafego, trafego_lock

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicia captura em thread separada (interface e filtro opcionais)
threading.Thread(target=start_sniff, daemon=True).start()

PROTO_NAMES = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

def gerar_dados_sinteticos():
    # gera alguns IPs aleatórios com tráfego
    ips = [f"192.168.0.{i}" for i in range(2,6)]
    data = {}
    for ip in ips:
        entrada = random.randint(500, 5000)
        saida = random.randint(300, 4000)
        protocolos = {str(6): random.randint(0, entrada), str(17): random.randint(0, saida), str(1): random.randint(0, 200)}
        data[ip] = {"entrada": entrada, "saida": saida, "protocolos": protocolos}
    return data

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dados")
async def dados():
    # Retorna dados reais se houver (capturados pelo sniff). Caso contrário, retorna dados sintéticos.
    with trafego_lock:
        if trafego:
            copia = {ip: {"entrada": v["entrada"], "saida": v["saida"], "protocolos": dict(v["protocolos"])} for ip, v in trafego.items()}
            trafego.clear()
            return JSONResponse(copia)
    # sem dados reais -> gerar sintéticos
    return JSONResponse(gerar_dados_sinteticos())
