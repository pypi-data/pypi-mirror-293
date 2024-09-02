from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform
import subprocess
import sys

class CustomInstallCommand(install):
    def run(self):
        super().run()
        
        if platform.system() != "Linux":
            install_vcpkg()
            run_cmake()
            build_cpp()
        else:
            if not os.path.exists("my_library.so"):
                os.system("g++ -fPIC -shared -o my_library.so main.cpp -lcurl")

def install_vcpkg():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vcpkg_path = os.path.join(current_dir, "vcpkg")

    if not os.path.exists(vcpkg_path):
        clone_command = [
            "git", "clone", "https://github.com/microsoft/vcpkg.git", vcpkg_path
        ]
        result = subprocess.run(clone_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            sys.exit(1)

        bootstrap_script = "bootstrap-vcpkg.sh" if platform.system() != "Windows" else "bootstrap-vcpkg.bat"
        bootstrap_command = [os.path.join(vcpkg_path, bootstrap_script)]
        result = subprocess.run(bootstrap_command, cwd=vcpkg_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode != 0:
            sys.exit(1)

    install_command = [os.path.join(vcpkg_path, "vcpkg"), "install", "curl"]
    subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_cmake():
    if library_exists():
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    vcpkg_path = os.path.join(current_dir, "vcpkg")
    build_dir = os.path.join(current_dir, "build")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    cmake_command = [
        "cmake", "..",
        f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(vcpkg_path, 'scripts', 'buildsystems', 'vcpkg.cmake')}"
    ]

    result = subprocess.run(cmake_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        sys.exit(1)

def build_cpp():
    if library_exists():
        return

    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

    build_command = ["cmake", "--build", "."]
    result = subprocess.run(build_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        sys.exit(1)

def library_exists():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lib_ext = "dll" if platform.system() == "Windows" else "so"
    lib_path = os.path.join(current_dir, "build", "Debug", f"my_library.{lib_ext}")
    return os.path.isfile(lib_path)

setup(
    name='curl_requests',               # Название пакета
    version='0.1.1',
    packages=find_packages(),           # Автоматически найдет папку curl_requests
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        'tqdm'
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
