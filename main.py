from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import threading, random
from capture import start_sniff, janela_atual, lock, historico, PROTOS, IP_SERVIDOR, INTERFACE

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

threading.Thread(target=start_sniff, args=(INTERFACE,), daemon=True).start()

def gerar_dados_sinteticos():
    ips = [f"192.168.0.{i}" for i in range(2,6)]
    data = {}
    for ip in ips:
        entrada = random.randint(500,5000)
        saida = random.randint(300,4000)
        protocolos = {str(p): random.randint(0,entrada) for p in PROTOS}
        data[ip] = {"entrada": entrada, "saida": saida, "protocolos": protocolos}
    return data

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dados")
async def dados():
    with lock:
        if janela_atual:
            copia = {ip: {"entrada":v["entrada"], "saida":v["saida"], "protocolos":dict(v["protocolos"])} for ip,v in janela_atual.items()}
            return JSONResponse(copia)
    return JSONResponse(gerar_dados_sinteticos())

@app.get("/series")
async def series(ip: str = None, last: int = 20):
    resultado = []
    with lock:
        for j in list(historico)[-last:]:
            if ip:
                if ip in j["dados"]:
                    resultado.append({"timestamp": j["timestamp"], "dados": j["dados"][ip]})
            else:
                resultado.append({"timestamp": j["timestamp"], "dados": j["dados"]})
    return JSONResponse(resultado)

@app.get("/metadata")
async def metadata():
    return JSONResponse({"IP_SERVIDOR": IP_SERVIDOR, "protocolos": PROTOS})
