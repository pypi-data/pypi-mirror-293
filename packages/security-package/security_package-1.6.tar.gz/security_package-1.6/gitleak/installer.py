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
        url = "https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_windows_x64.zip"
    else:
        raise OSError("Unsupported operating system")
    
    download_command = f"curl -LO {url}"
    subprocess.run(download_command, shell=True, check=True)

def install_gitleaks():
    system = platform.system().lower()
    
    download_gitleaks()

    if system == 'linux':
        # Extract the tar.gz file
        tar_command = "tar -xvf gitleaks-linux-amd64.tar.gz"
        subprocess.run(tar_command, shell=True, check=True)
        
        binary_path = "./gitleaks"
        # Get the parent directory of the tar.gz file
        parent_dir = os.path.dirname(os.path.abspath("gitleaks-linux-amd64.tar.gz"))
        install_path = os.path.join(parent_dir, "gitleaks")
        
        # Move the binary
        shutil.move(binary_path, install_path)
        subprocess.run(["chmod", "+x", install_path])
        print(f"Gitleaks has been installed at {install_path}")

    elif system == 'windows':
        # Check if the ZIP file exists
        zip_file = "gitleaks_8.18.4_windows_x64.zip"
        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"The download file {zip_file} does not exist.")
        
        # Extract the ZIP file using PowerShell
        extraction_dir = os.path.join(os.path.dirname(zip_file), "gitleaks")
        zip_command = f'powershell -command "Expand-Archive -Force -Path {zip_file} -DestinationPath {extraction_dir}"'
        subprocess.run(zip_command, shell=True, check=True)
        
        binary_path = os.path.join(extraction_dir, "gitleaks.exe")
        install_path = os.path.join(os.path.dirname(zip_file), "gitleaks.exe")
        
        # Move the binary
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
