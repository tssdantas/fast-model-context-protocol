import sys, asyncio
sys.path.append('./src')
from client import clientMain
from mcpserver import serverMain
    
if __name__ == "__main__":
    validTransport = ['sse', 'stdio']
    if (len(sys.argv) > 1 and sys.argv[1] in validTransport):
        transport = sys.argv[1]
        serverMain(transport)
    else:
        asyncio.run(clientMain('api'))