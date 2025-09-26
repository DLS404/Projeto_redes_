Aluno: Danielle Lima da Silva - 2222130001

INSTRUÇÕES RÁPIDAS - VERSÃO HÍBRIDA
----------------------------------
1) Abra o projeto no VS Code.
2) Crie e ative um virtualenv:
   python -m venv venv
   venv\Scripts\Activate   (Windows PowerShell)
   source venv/bin/activate  (Linux/macOS)
3) Instale dependências:
   pip install scapy fastapi uvicorn jinja2 aiofiles
4) Edite capture.py e altere IP_SERVIDOR para o IP do servidor que deseja monitorar.
   - Para usar interface específica, altere a chamada em main.py para passar iface na função start_sniff.
5) Execute o servidor:
   python -m uvicorn main:app --reload
6) Abra no navegador:
   http://127.0.0.1:8000
FUNCIONAMENTO
- O endpoint /dados retorna dados capturados se houver. Caso contrário, gera dados sintéticos automaticamente.
- Clique em uma barra para abrir um modal com um gráfico de pizza mostrando breakdown por protocolo (nomes traduzidos quando possível).
- Use o botão 'Forçar Dados Sintéticos' para ver rapidamente o comportamento sem tráfego real.
NOTAS
- Captura de pacotes pode exigir execução como administrador/root.
- Em Windows, instale Npcap; em Linux, execute com privilégios suficientes.
