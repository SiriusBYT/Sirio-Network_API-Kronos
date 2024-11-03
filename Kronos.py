# Server Modules
import socket # API's Native Language 

# Multi-threading modules
import asyncio # Required for WebSockets
import threading # Required for WebSockets

# Miscellaneous Modules
import time # Required for logs
import os # Required for KeyboardInterrupt (DEBUG) and loading config files
import sys # Required for KeyboardInterrupt (DEBUG)
import json # Load the list of servers to redirect to
import traceback # Error handling

# Load sensitive information
import dotenv
dotenv.load_dotenv()

# Own Modules
from SN_PyDepends import *

Log(f'[System] Configuring server...')
SRV_CFG = LoadCFG(os.path.basename(__file__).replace(".py", ".cfg"))

""" .env Variables """
SSL_Cert = os.getenv('SSL_Cert')
SSL_Key = os.getenv('SSL_Key')

""" .cfg Variables """
SRV_Name = SRV_CFG["Info"]["Name"]
SRV_Desc = SRV_CFG["Info"]["Description"]
SRV_Vers = SRV_CFG["Info"]["Version"]

Routine_Sleep = int(SRV_CFG["API"]["RoutineSleep"])
API_RawPort = int(SRV_CFG["API"]["RawPort"])
API_PacketSize = int(SRV_CFG["API"]["PacketSize"])

""" Processed Variables """
API_SocketHost = socket.gethostname()
API_RawSocket = socket.socket()

Log(f'[System] Loaded configuration for "{SRV_Name} - {SRV_Vers}", {SRV_Desc}.')


""" Service Functions """
def SirioAPI_Thread():
    Log(f'[System] INFO: Initializing SirioAPI...')

    async def Process_Request(Client_Request, Client_Address):
        return Client_Request
        
    """ Socket Handlers """
    def RawSocket_Server():
        Log(f'[System] INFO: Starting RawSockets Server...')

        async def RawSocket_Handler(Client_Socket):
            Client, Address = Client_Socket.accept()
            Client_Address = str(Address[0])+":"+str(Address[1])
            Log(f'[Connection] OK: Raw://{Client_Address}.')

            Forwarded = Client.recv(API_PacketSize).decode()
            Forwarded = Forwarded.split("¤") # Janky!
            Forwarded_Address = Forwarded[0]
            Forwarded_Request = Forwarded[1]

            Log(f'[Request] {Forwarded_Address}: "{Forwarded_Request}".')
            Server_Result = await Process_Request(Forwarded_Request, Forwarded_Address)
            Log(f'[Sending] {Forwarded_Address}: {Server_Result}')
            Client.send(Server_Result.encode())

        def RawSocket_Async(RawSocket):
            asyncio.run(RawSocket_Handler(RawSocket))

        Log(f'[System] OK: RawSockets thread started.')
        Attempt = 1
        while True:
            try:
                API_RawSocket.bind((API_SocketHost, API_RawPort))
                Log(f"[System] Success: Binded RawSocket Server in {Attempt} attempt(s).")
                break
            except:
                Log(f"[System] ERROR: Failed to bind RawSocket Server! (Attempt {Attempt})")
                Attempt+=1
                time.sleep(1)
        API_RawSocket.listen()
        Log(f'[System] OK: Now listening for RawSockets.')
        while True:
            threading.Thread(target=RawSocket_Async(API_RawSocket)).start()

    threading.Thread(target=RawSocket_Server).start()


""" Server State Functions """

def Shutdown():
    Log(f'[System] SHUTDOWN: Shutting down server...')
    try: sys.exit(130)
    except SystemExit: os._exit(130)
    
def Bootstrap():
    os.system("clear")
    Log(f"[System] Starting server...")
    threading.Thread(target=SirioAPI_Thread).start()
    Log(f'[System] Server initialized.')
    try:
        while True: 
            Log(f'[System] Awaiting next Routine Loop in {Routine_Sleep} seconds.')
            time.sleep(Routine_Sleep)
            Log(f'[System] Executing Routine.')
    except KeyboardInterrupt:
        Shutdown()

# Spark
if __name__== '__main__': 
    while True:
        try: Bootstrap()
        except Exception: Crash(traceback.format_exc(),False)
