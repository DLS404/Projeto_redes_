from scapy.all import sniff, IP
from collections import defaultdict
import threading

# ATENÇÃO: altere para o IP do servidor que você quer monitorar
IP_SERVIDOR = "127.0.0.1"

# Estrutura de dados compartilhada entre sniff e API
trafego = defaultdict(lambda: {"entrada": 0, "saida": 0, "protocolos": defaultdict(int)})
trafego_lock = threading.Lock()

def processa_pacote(pkt):
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        tamanho = len(pkt)
        protocolo = pkt[IP].proto

        with trafego_lock:
            if dst == IP_SERVIDOR:
                trafego[src]["entrada"] += tamanho
                trafego[src]["protocolos"][protocolo] += tamanho
            elif src == IP_SERVIDOR:
                trafego[dst]["saida"] += tamanho
                trafego[dst]["protocolos"][protocolo] += tamanho

def start_sniff(iface=None, filter=None):
    """Inicia a captura. 
    - iface: opcional, nome da interface para capturar (ex: 'Ethernet0' ou 'eth0')
    - filter: opcional, BPF filter
    """
    try:
        sniff(prn=processa_pacote, store=0, iface=iface, filter=filter)
    except Exception as e:
        # Falha ao iniciar captura (permissões, npcap, etc.)
        print('start_sniff error:', e)

if __name__ == "__main__":
    import threading, time
    thread = threading.Thread(target=start_sniff, daemon=True)
    thread.start()
    try:
        while True:
            with trafego_lock:
                print(dict(trafego))
                trafego.clear()
    except KeyboardInterrupt:
        print("Exiting...")    