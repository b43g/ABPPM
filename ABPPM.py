import sys
import asyncio
import os
import time
import platform
import importlib
import inspect
import pkg_resources
import subprocess
import datetime
import http.client
import json
import pip

from roaming_Data.shortcuts import *

if sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def Startup() -> str:
    return "\033[4m\033[1m{}\033[0m".format(startup())
print(Startup())

class ABPPM_STARTUP:

    async def Client_Startup(self=None) -> any:

        CLI_INPUT = input("\033[34m\n{}\033[0m > ".format("Python {}".format(platform.python_version()))).split()

        CLI_FINAL_INPUT = " ".join(CLI_INPUT)
        try:
            if CLI_INPUT.__contains__("src"):
                try:
                    module = importlib.import_module(CLI_INPUT[1])
                    source_code_path = inspect.getsourcefile(module)
                    module_dir = os.path.dirname(source_code_path)
                    files = os.listdir(module_dir)
                    for file in files:
                        print("{}- {} {}".format("\033[32m",file,"\033[0m"))
                except:
                    print("\033[31m Could not find module {}!\033[0m".format(module))
            elif CLI_INPUT.__contains__("pkg_check") or CLI_INPUT.__contains__("package_check") or CLI_INPUT.__contains__("packages"):
                try:
                    installed_packages = [package.key for package in pkg_resources.working_set]
                    for package in installed_packages:
                        print("{}- {} {}".format("\033[32m", package, "\033[0m"))
                except:
                    print("\033[31m Fatal Error! \033[0m")
            elif CLI_INPUT.__contains__("package_install") or CLI_INPUT.__contains__("pck_install"):
                os.system("pip install {}".format(CLI_INPUT[1]))
            elif CLI_FINAL_INPUT.__contains__("package_about"):
                package_name = CLI_INPUT[1]
                try:
                    package = pkg_resources.get_distribution(package_name)
                    print("\033[32mPackage Information:")
                    print("Name:", package.project_name)
                    print("Version:", package.version)
                    print("Location:", package.location)
                    requirements = package.requires()
                    if not requirements:
                        print("Dependencies: None")
                    else:
                        print("Dependencies:")
                        for req in requirements:
                            print("  -", req)
                    print("Egg Name:", package.egg_name())
                    print("Summary:", package.summary, "\033[0m")
                except pkg_resources.DistributionNotFound:
                    print("\033[31mThe package '{}' was not found.\033[0m".format(package_name))
            elif CLI_INPUT.__contains__("package_search"):
                try:
                    pkg_resources.get_distribution(CLI_INPUT[1])
                    print("\033[32mThe package '{}' is installed.\033[0m".format(CLI_INPUT[1]))
                except pkg_resources.DistributionNotFound:
                    print("\033[31mThe package '{}' is not installed.\033[0m".format(CLI_INPUT[1]))
            elif CLI_INPUT.__contains__("egg/startup_file"):
                project_name = CLI_INPUT[1]
                os.makedirs(project_name)
                os.chdir(project_name)
                open("__init__.py", "a").close()
                open("setup.py", "w").write("from setuptools import setup, find_packages\n\nsetup(\n    name='{}',\n    version='0.1',\n    packages=find_packages(),\n)".format(project_name))
                time.sleep(1)
                print("\033[32mYour project has been created in the '{}' directory.".format(project_name))
                time.sleep(0.8)
                print("You can create an egg file by running the following command in your terminal:")
                time.sleep(0.8)
                print("python {}/setup.py bdist_egg".format(project_name))
                time.sleep(0.8)
                print("You can change the __init__.py file, or format the project however you wish.\nBut this is only making the startup.py/egg file you need for your project, you may also edit the startup file\033[0m")
                os.chdir("..")
            elif CLI_INPUT.__contains__("package_remove"):
                module_name = CLI_INPUT[1]
                try:
                    os.system("pip uninstall {}".format(module_name))
                except:
                    print("\033[31mPackage {} is not installed.\033[0m".format(module_name))
                os.chdir("..")
            elif CLI_INPUT.__contains__("PRFF") or CLI_INPUT.__contains__("py_run_from_File"):
                subprocess.call("python", CLI_INPUT[1])
            elif CLI_INPUT.__contains__("PRFC") or CLI_INPUT.__contains__("py_run_from_Code"):
                os.system("python -c {}".format(CLI_INPUT[1]))
            elif CLI_INPUT.__contains__("package_checker"):
                try:
                    __import__(CLI_INPUT[1])
                    print(f"\033[32m{CLI_INPUT[1]} is working\033[0m")
                except ImportError as e:
                    print(f"\033[33m{CLI_INPUT[1]} is not working. Error: \033[31m{e}\033[0m")
            elif CLI_INPUT.__contains__("up") or CLI_INPUT.__contains__("update_pip"):
                os.system("python -m pip install --upgrade pip")
            elif CLI_INPUT.__contains__("CFI") or CLI_INPUT.__contains__("check_file_imports"):
                file_path = CLI_INPUT[1]
                missing_packages = []
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.startswith("import"):
                            package_name = line.strip().split(" ")[1]
                            try:
                                importlib.import_module(package_name)
                            except ImportError:
                                missing_packages.append(package_name)

                if missing_packages:
                    print("\033[33mThe following packages are missing:", ", ".join(missing_packages))
                    install = input("Do you want to install the missing packages? [Y/n] \033[0m").strip().lower()
                    if install == 'y' or install == 'yes':
                        for package in missing_packages:
                            pip.main(['install', package])
                    else:
                        print("Skipping installation of missing packages.\033[0m")
                else:
                    print("\033[32mAll dependencies are already installed.\033[0m")
            elif CLI_INPUT.__contains__("ABPPM"):
                print("\033[32m\t- src <package>")
                print("\t- pkg_check <package>")
                print("\t- package_install <package>")
                print("\t- package_search <package>")
                print("\t- egg/startup_file <package name>")
                print("\t- package_search <package>")
                print("\t- CFI <python_directory>")
                print("\t- up/upgrade_pip")
                print("\t- PRFF")
                print("\t- PRFC <code>")
                print("\t- package_remove <package>")
                print("\t- pkg_check <package>")
                print("\t- CFI_R <python_directory>")
                print("\t- package_about <package>\033[0m")
            elif CLI_INPUT.__contains__("CFI_R") or CLI_INPUT.__contains__("check_file_imports_run"):
                file_path = CLI_INPUT[1]
                missing_packages = []
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.startswith("import"):
                            package_name = line.strip().split(" ")[1]
                            try:
                                importlib.import_module(package_name)
                            except ImportError:
                                missing_packages.append(package_name)

                if missing_packages:
                    print("\033[33mThe following packages are missing:", ", ".join(missing_packages))
                    install = input("Do you want to install the missing packages? [Y/n] \033[0m").strip().lower()
                    if install == 'y' or install == 'yes':
                        for package in missing_packages:
                            pip.main(['install', package])
                    else:
                        print("Skipping installation of missing packages.\033[0m")
                else:
                    print("\033[32mAll dependencies are already installed.\033[0m")

                time.sleep(4)
                os.system("python {}".format(file_path))
            else:
                os.system(CLI_FINAL_INPUT)
        except:
            pass

while(True):
    asyncio.run(ABPPM_STARTUP.Client_Startup())