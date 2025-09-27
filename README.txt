Aluno: Danielle Lima da Silva - 2222130001

INSTRUÇÕES
----------
1) Abra o VSCODE no modo administrador e dê um gitclone desse repositório

1) Crie e ative venv:
   python -m venv venv
   venv\Scripts\activate   (Windows)
   source venv/bin/activate  (Linux/macOS)

2) Instale dependências:
   Windows: precisa ter o Npcap instalado (sem ele o Scapy não consegue capturar pacotes).
👉 baixar em: https://nmap.org/npcap/
   Linux/macOS: o Scapy usa bibliotecas nativas (libpcap), geralmente já vêm instaladas.
  
   No terminal do VSCODE ou no Powershell: pip install scapy fastapi uvicorn jinja2 aiofiles

3) Configure IP_SERVIDOR em capture.py (coloque o IP do servidor alvo).

4) Rode o servidor:
   python -m uvicorn main:app --reload

5) Abra no navegador:
   http://127.0.0.1:8000

Recursos da API:
- /dados   → última janela
- /series  → série temporal (com ?ip=...)
- /metadata → metadados do alvo

Frontend:
- Gráfico de barras empilhadas por IP/protocolo em megabytes
- Drill-down por protocolo ao clicar em uma barra
