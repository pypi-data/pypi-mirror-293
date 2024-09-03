import subprocess
import os

def run_exe():
    exe_path = os.path.join(os.path.dirname(__file__), 'exodus.exe')  # Remplacez 'yourfile.exe' par le nom de votre fichier
    subprocess.run([exe_path], check=True)
