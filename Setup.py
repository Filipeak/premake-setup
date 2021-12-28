import os
import subprocess
import platform

from SetupPremake import PremakeValidator
from SetupPython import PythonValidator

if PythonValidator.validate_python():
    premake_installed = PremakeValidator.validate_premake()

    if premake_installed:
        if platform.system() == "Windows":
            print("Running Premake...")            
            subprocess.call(["Win-GenerateProjects.bat", "nopause"])

        print("Setup completed!")
    else:
        print("Couldn't validate Premake, which is needed to generate project files!")
else:
    print("Couldn't validate python")