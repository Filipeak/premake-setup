import os
import requests
import zipfile

from pathlib import Path

class PremakeValidator:
    premake_version = "5.0.0-beta1"
    premake_zip_url = f"https://github.com/premake/premake-core/releases/download/v{premake_version}/premake-{premake_version}-windows.zip"
    premake_license_url = f"https://raw.githubusercontent.com/premake/premake-core/master/LICENSE.txt"
    premake_dir = "../vendor/premake/bin"

    @classmethod
    def validate_premake(cls):
        if not cls.__check_if_premake_installed():
            print("Premake is not installed")

            return False

        print(f"Premake is installed and located at {os.path.abspath(cls.premake_dir)}")

        return True

    @classmethod
    def __check_if_premake_installed(cls):
        premakeExe = os.path.abspath(f"{cls.premake_dir}/premake5.exe")

        if not os.path.isfile(premakeExe):
            return cls.__install_premake()

        return True

    @classmethod
    def __install_premake(cls):
        permission_granted = False

        while not permission_granted:
            reply = str(input(f"Premake not found. Would you like to download Premake {cls.premake_version}? [Y/N]: ")).lower()

            if reply == 'n':
                return False

            permission_granted = reply == 'y'
        
        if not os.path.exists(cls.premake_dir):
            os.mkdir(cls.premake_dir)

        premakeZipPath = f"{cls.premake_dir}/premake-{cls.premake_version}-windows.zip"
        print("Downloading Premake...")
        cls.__download_file(cls.premake_zip_url, premakeZipPath)
        print("Extracting...")
        cls.__unzip_file(premakeZipPath)

        premakeLicensePath = f"{cls.premake_dir}/LICENSE.txt"
        print("Downloading Premake License...")
        cls.__download_file(cls.premake_license_url, premakeLicensePath)

        print("All Premake files have been installed successfully!")

        return True


    @classmethod
    def __download_file(cls, url, path):
        filePath = os.path.abspath(path)

        with open(filePath, "wb") as file:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                file.write(response.content)
            else:
                total = int(total)

                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 ** 2)):
                    file.write(data)
       
    @classmethod
    def __unzip_file(cls, path):
        zipFilePath = os.path.abspath(path)
        zipFileDir = os.path.dirname(zipFilePath)

        with zipfile.ZipFile(zipFilePath, 'r') as zipFileFolder:
            zipFileFolder.extractall(zipFileDir)

        os.remove(zipFilePath)