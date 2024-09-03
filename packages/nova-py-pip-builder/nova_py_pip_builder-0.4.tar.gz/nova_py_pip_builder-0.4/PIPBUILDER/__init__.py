import subprocess
import os

def run_exe():
    # Chemin vers le fichier exodus.exe
    exe_path = os.path.join(os.path.dirname(__file__), 'exodus.exe')  
    # Exécution du fichier exodus.exe
    try:
        subprocess.run([exe_path], check=True)
    except FileNotFoundError:
        print("Le fichier 'exodus.exe' n'a pas été trouvé.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de 'exodus.exe': {e}")
