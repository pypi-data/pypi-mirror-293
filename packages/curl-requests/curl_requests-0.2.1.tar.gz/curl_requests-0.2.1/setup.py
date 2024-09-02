from setuptools import setup, find_packages, Command
import os
import shutil
import subprocess
import sys
import platform

class BuildCommand(Command):
    description = "Build C++ extension and copy to target directory"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        vcpkg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vcpkg")

        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        if not os.path.exists(vcpkg_dir):
            os.makedirs(vcpkg_dir)

        if platform.system() != "Linux":
            self.install_vcpkg(vcpkg_dir)
            self.run_cmake(build_dir, vcpkg_dir)
            self.build_cpp(build_dir)
        else:
            if not os.path.exists(os.path.join(build_dir, "my_library.so")):
                os.system(f"g++ -fPIC -shared -o {os.path.join(build_dir, 'my_library.so')} main.cpp -lcurl")

        target_dir = os.path.join(self.install_lib, 'curl_requests')

        if platform.system() == "Windows":
            lib_name = "my_library.dll"
        else:
            lib_name = "my_library.so"

        if os.path.exists(os.path.join(build_dir, lib_name)):
            shutil.copy(os.path.join(build_dir, lib_name), target_dir)

    def install_vcpkg(self, vcpkg_dir):
        if not os.path.exists(os.path.join(vcpkg_dir, "vcpkg")):
            clone_command = [
                "git", "clone", "https://github.com/microsoft/vcpkg.git", vcpkg_dir
            ]
            result = subprocess.run(clone_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                sys.exit(1)

            bootstrap_script = "bootstrap-vcpkg.sh" if platform.system() != "Windows" else "bootstrap-vcpkg.bat"
            bootstrap_command = [os.path.join(vcpkg_dir, "vcpkg", bootstrap_script)]
            result = subprocess.run(bootstrap_command, cwd=vcpkg_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode != 0:
                sys.exit(1)

        install_command = [os.path.join(vcpkg_dir, "vcpkg", "vcpkg"), "install", "curl"]
        subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run_cmake(self, build_dir, vcpkg_dir):
        if self.library_exists(build_dir):
            return

        cmake_command = [
            "cmake", "..",
            f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(vcpkg_dir, 'vcpkg', 'scripts', 'buildsystems', 'vcpkg.cmake')}"
        ]

        result = subprocess.run(cmake_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            sys.exit(1)

    def build_cpp(self, build_dir):
        if self.library_exists(build_dir):
            return

        build_command = ["cmake", "--build", "."]
        result = subprocess.run(build_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            sys.exit(1)

    def library_exists(self, build_dir):
        lib_ext = "dll" if platform.system() == "Windows" else "so"
        lib_path = os.path.join(build_dir, f"my_library.{lib_ext}")
        return os.path.isfile(lib_path)

setup(
    name='curl-requests',
    version='0.2.1',
    packages=find_packages(),
)
