import os
import platform
import requests
import zipfile
import tarfile
from pathlib import Path

def download_zap():
    system = platform.system().lower()

    if system == 'windows':
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2_15_0_windows.exe'
        zap_file = 'ZAP_Windows.zip'
    elif system == 'darwin':  # macOS
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2.15.0_aarch64.dmg'
        zap_file = 'ZAP_Mac_OS_X.zip'
    else:  # Assuming Linux
        zap_url = 'https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2_15_0_unix.sh'
        zap_file = 'ZAP_Linux.tar.gz'

    print(f'Downloading OWASP ZAP from {zap_url}...')
    response = requests.get(zap_url, stream=True)
    with open(zap_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return zap_file

def extract_zap(zap_file):
    zap_dir = 'OWASP_ZAP'  # Fixed directory name without version number
    print(f'Extracting {zap_file}...')

    if zap_file.endswith('.zip'):
        with zipfile.ZipFile(zap_file, 'r') as zip_ref:
            zip_ref.extractall(zap_dir)
    elif zap_file.endswith('.tar.gz'):
        with tarfile.open(zap_file, 'r:gz') as tar_ref:
            tar_ref.extractall(zap_dir)

    # Cleanup the downloaded file
    print(f'Cleaning up {zap_file}...')
    os.remove(zap_file)

    print(f'OWASP ZAP installed successfully in {zap_dir}')

def main():
    zap_file = download_zap()
    extract_zap(zap_file)

if __name__ == "__main__":
    main()
