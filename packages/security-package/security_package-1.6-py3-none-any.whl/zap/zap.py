import os
import platform
import requests
import zipfile
import tarfile
import subprocess
from pathlib import Path

def download_zap():
    system = platform.system().lower()

    if system == 'windows':
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2_15_0_windows.exe'
        zap_file = 'ZAP_Windows.exe'
    elif system == 'darwin':  # macOS
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2.15.0_aarch64.dmg'
        zap_file = 'ZAP_Mac_OS_X.dmg'
    else:  # Assuming Linux
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2_15_0_unix.sh'
        zap_file = 'ZAP_Linux.sh'

    print(f'Downloading OWASP ZAP from {zap_url}...')
    response = requests.get(zap_url, stream=True)
    with open(zap_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return zap_file

def extract_zap(zap_file):
    zap_dir = 'OWASP_ZAP'
    print(f'Extracting {zap_file}...')

    if zap_file.endswith('.zip'):
        with zipfile.ZipFile(zap_file, 'r') as zip_ref:
            zip_ref.extractall(zap_dir)
    elif zap_file.endswith('.tar.gz'):
        with tarfile.open(zap_file, 'r:gz') as tar_ref:
            tar_ref.extractall(zap_dir)

    print(f'OWASP ZAP extracted to {zap_dir}')
    return zap_dir

def install_zap(zap_file, zap_dir):
    system = platform.system().lower()

    if system == 'windows':
        print(f'Running ZAP installer {zap_file}...')
        subprocess.run([zap_file], check=True)

    elif system == 'darwin':  # macOS
        print(f'Running ZAP installer for macOS...')
        subprocess.run(['hdiutil', 'attach', zap_file], check=True)
        subprocess.run(['sudo', 'cp', '-R', f'/Volumes/ZAP/ZAP.app', '/Applications'], check=True)
        subprocess.run(['hdiutil', 'detach', '/Volumes/ZAP'], check=True)

    else:  # Linux
        print(f'Running ZAP installer for Linux...')
        subprocess.run(['chmod', '+x', zap_file], check=True)
        subprocess.run(['sh', zap_file], check=True)

    print('OWASP ZAP installation complete.')

def main():
    zap_file = download_zap()
    zap_dir = extract_zap(zap_file)
    install_zap(zap_file, zap_dir)

if __name__ == "__main__":
    main()
