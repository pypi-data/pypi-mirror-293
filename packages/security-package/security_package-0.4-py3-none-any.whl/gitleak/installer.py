# gitleaks_installer/installer.py
import os
import subprocess
import sys

    # url = f"https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_windows_armv6.zip"
import os
import subprocess
import sys
import platform
import shutil

def download_gitleaks():
    system = platform.system().lower()
    
    if system == 'linux':
        url = "https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_linux_arm64.tar.gz"
    elif system == 'windows':
        url = "https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_windows_armv6.zip"
    else:
        raise OSError("Unsupported operating system")
    
    download_command = f"curl -LO {url}"
    subprocess.run(download_command, shell=True, check=True)

def install_gitleaks():
    system = platform.system().lower()
    
    download_gitleaks()
    
    if system == 'linux':
        tar_command = "tar -xvf gitleaks-linux-amd64.tar.gz"
        subprocess.run(tar_command, shell=True, check=True)
        binary_path = "./gitleaks"
        install_path = "/usr/local/bin/gitleaks"
        shutil.move(binary_path, install_path)
        subprocess.run(["chmod", "+x", install_path])
    elif system == 'windows':
        # Check if the file exists before trying to extract
        if not os.path.exists("gitleaks_8.18.4_windows_armv6.zip"):
            raise FileNotFoundError("The download file gitleaks_8.18.4_windows_armv6.zip does not exist.")
        
        # Extract the zip file
        zip_command = "powershell -command \"Expand-Archive -Force -Path .\\gitleaks_8.18.4_windows_armv6.zip -DestinationPath .\""
        subprocess.run(zip_command, shell=True, check=True)
        
        binary_path = "./gitleaks.exe"
        install_path = os.path.join(os.environ['ProgramFiles'], 'Gitleaks', 'gitleaks.exe')
        os.makedirs(os.path.dirname(install_path), exist_ok=True)
        shutil.move(binary_path, install_path)
        print(f"Gitleaks has been installed at {install_path}")
    else:
        raise OSError("Unsupported operating system")

def add_gitleaks_to_path():
    system = platform.system().lower()
    
    if system == 'linux':
        bashrc_path = os.path.expanduser("~/.bashrc")
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\nexport PATH=$PATH:/usr/local/bin\n")
        subprocess.run(["source", bashrc_path], shell=True)
        print("Gitleaks path has been added to your ~/.bashrc file.")
    elif system == 'windows':
        install_path = os.path.join(os.environ['ProgramFiles'], 'Gitleaks')
        subprocess.run(f'setx PATH "%PATH%;{install_path}"', shell=True)
        print("Gitleaks path has been added to your system PATH.")
    else:
        raise OSError("Unsupported operating system")
