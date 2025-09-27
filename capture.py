from scapy.all import sniff, IP
from collections import defaultdict, deque
import threading, time

IP_SERVIDOR = "127.0.0.1"
INTERFACE = None
JANELA_SEG = 5
HISTORICO_JANELAS = 120

historico = deque(maxlen=HISTORICO_JANELAS)
janela_atual = defaultdict(lambda: {"entrada":0,"saida":0,"protocolos":defaultdict(int)})
lock = threading.Lock()
inicio_janela = time.time()

PROTOS = {1:'ICMP',6:'TCP',17:'UDP'}

def processa_pacote(pkt):
    global inicio_janela, janela_atual
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        tamanho = len(pkt)
        proto = pkt[IP].proto
        with lock:
            agora = time.time()
            if agora - inicio_janela >= JANELA_SEG:
                historico.append({"timestamp": inicio_janela, "dados": dict(janela_atual)})
                janela_atual = defaultdict(lambda: {"entrada":0,"saida":0,"protocolos":defaultdict(int)})
                inicio_janela = agora
            if dst == IP_SERVIDOR:
                janela_atual[src]["entrada"] += tamanho
                janela_atual[src]["protocolos"][proto] += tamanho
            elif src == IP_SERVIDOR:
                janela_atual[dst]["saida"] += tamanho
                janela_atual[dst]["protocolos"][proto] += tamanho

def start_sniff(iface=None):
    try:
        sniff(prn=processa_pacote, store=0, iface=iface)
    except Exception as e:
        print("Erro captura:", e)
