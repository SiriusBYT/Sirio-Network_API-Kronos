# Modules
import time # Required for sleep functions and time related shenanigans
import discord_webhook # I'm not fucking logging into SSH every nano second but I'm a chronically online Flashcord user so.. Discord for emergency notifications!!!
import configparser # Required for loading config files
import sys # For Crash() Function

# Load sensitive information
import dotenv, os
dotenv.load_dotenv()

SRV_Name = os.getenv('SRV_Name')
SRV_Desc = os.getenv('SRV_Desc')
SRV_Vers = os.getenv('SRV_Vers')

""" Logging Functions """
# Get current time string in the example format "22:10:10" - "31-07-2024"
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date

def Log(Log):
    Log = str(Log) # Failsafe if this function is wrongly called, especially when debugging
    Time,Date = GetTime()
    TLog = f"[{Time}] {Log}"
    with open(f"logs/{Date}.log", "a", encoding="utf=8") as LogFile:
        LogFile.write(f"{TLog}\n")
        print(TLog)


""" int() Functions """
# Logs the server's basic information
def LoadCFG(CFG_File):
    CFG = configparser.ConfigParser()
    CFG.read(CFG_File)
    CFG.sections()
    Log(f'[System] Loaded configuration file "{CFG_File}".')
    return CFG

# Checks if a specified array number exist
# 04/10/24: This function is retarded! Just do "if [variable here]:"!!!
def doesEntryExists(Array,Number):
    try:
        Dummy = Array[Number]
        return True
    except:
        return False

""" void() Functions """

def Crash(Error, AllowRestart):
    Log(f"[CRASH] The server has crashed!")
    print(Error)
    if AllowRestart == True:
        for cycle in range (10):
            Log(f"Restarting server in {10-cycle}...")
            time.sleep(1)
    else:
        try: sys.exit(130)
        except SystemExit: os._exit(130)

def DoNothing(): return