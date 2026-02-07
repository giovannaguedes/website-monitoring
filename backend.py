import asyncio
import websockets
import json
import psutil
import random
from datetime import datetime

class TrafficMonitor:
    def __init__(self):
        self.active_monitoring = False
        self.target_domain = None
        
    def get_network_stats(self):
        """Simula dados de tráfego de rede (substituir por pcap real)"""
        net_io = psutil.net_io_counters()
        
        return {
            'bandwidth': round(random.uniform(0.5, 5.0), 2),  # MB/s
            'packets': f"{random.randint(100, 1000):,}",
            'efficiency': random.randint(70, 95),
            'timestamp': datetime.now().isoformat(),
            'domain': self.target_domain or 'all'
        }

async def handle_client(websocket, path):
    monitor = TrafficMonitor()
    
    async for message in websocket:
        try:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'start_capture':
                monitor.target_domain = data.get('domain', '')
                monitor.active_monitoring = True
                
                # Envia dados simulados periodicamente
                while monitor.active_monitoring:
                    if websocket.open:
                        stats = monitor.get_network_stats()
                        await websocket.send(json.dumps(stats))
                        await asyncio.sleep(1)  # Atualiza a cada 1s
                    else:
                        break
                        
            elif action == 'stop_capture':
                monitor.active_monitoring = False
                
        except Exception as e:
            print(f"Erro: {e}")

async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("✅ Servidor WebSocket rodando em ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())