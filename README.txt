Alunas:
Danielle Lima da Silva - 2222130001
Mayra Sales da Costa - 2012082054

INSTRUÇÕES
----------
1) Instale dependências:
   Python (para rodar o programa): https://www.python.org/downloads/

   Windows: precisa ter o Npcap instalado (sem ele o Scapy não consegue capturar pacotes).
👉 baixar em: https://nmap.org/npcap/
   Linux/macOS: o Scapy usa bibliotecas nativas (libpcap), geralmente já vêm instaladas.

2) Abra o VSCODE no modo administrador e dê um git clone desse repositório

3) Crie e ative venv:
   python -m venv venv

   venv\Scripts\activate   (Windows)
   source venv/bin/activate  (Linux/macOS)

   pip install scapy fastapi uvicorn jinja2 aiofiles

4) Configure IP_SERVIDOR em capture.py (coloque o IP do servidor alvo).

5) Rode o servidor:
   python -m uvicorn main:app --reload (Windows/VSCODE)
   sudo python -m uvicorn main:app --reload (Linux)

6) Abra no navegador:
   http://127.0.0.1:8000

Recursos da API:
- /dados   → última janela
- /series  → série temporal (com ?ip=...)
- /metadata → metadados do alvo

Frontend:
- Gráfico de barras empilhadas por IP/protocolo em megabytes
- Drill-down por protocolo ao clicar em uma barra
