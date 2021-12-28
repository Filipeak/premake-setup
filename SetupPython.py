import sys
import subprocess
import importlib.util

class PythonValidator:
    required_packages = ["requests"]
    min_version_major = 3
    min_version_minor = 3
    min_version_micro = 0


    @classmethod
    def validate_python(cls):
        if not cls.__validate_python_version() or not cls.__validate_python_packages():
            return False

        return True


    @classmethod
    def __validate_python_version(cls):
        if sys.version is not None:
            major = sys.version_info.major
            minor = sys.version_info.minor
            micro = sys.version_info.micro

            print(f"Detected Python {major}.{minor}.{micro}")

            if major < cls.min_version_minor or (minor < cls.min_version_minor and major <= cls.min_version_major) or (micro < cls.min_version_micro and minor < cls.min_version_minor and major <= cls.min_version_major):
                print(f"Python version is too low, minimum version is: Python {cls.min_version_major}.{cls.min_version_minor}.{cls.min_version_micro}")

                return False

            print("Python version OK")

            return True

        return False
    

    @classmethod
    def __validate_python_packages(cls):
        for package in cls.required_packages:
            if not cls.__validate_package(package):
                return False

        return True

    
    @classmethod
    def __validate_package(cls, package_name):
        if importlib.util.find_spec(package_name) is None:
            return cls.__install_package()

        return True

    @classmethod
    def __install_package(cls, package_name):
        permission_granted = False

        while not permission_granted:
            reply = str(input("Would you like to install following Python package [Y/N]: " + package_name)).lower()

            if reply == 'n':
                return False

            permission_granted = reply == 'y'

        print(f"Installing {package_name} module...")

        subprocess.check_call(["python", "-m", "pip", "install", package_name])

        return cls.__validate_package(package_name)