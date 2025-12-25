"""
DEPRECATED: This module is no longer used in the project after v1.0.0.
This module contains the InstallationManager class, which is used to manage
the installation of dependencies.
"""

import os
import platform
import subprocess
from pathlib import Path
import urllib.request


class InstallationManager:
    """Class to manage the installation of dependencies"""

    def __init__(self):
        self.root_dir = Path.cwd()
        self.conda_dir = self.root_dir / "conda"
        self.env_name = "open_llm_vtuber"
        self.python_version = "3.10"

        # Platform specific settings
        self.platform = platform.system().lower()
        if self.platform == "windows":
            self.conda_executable = self.conda_dir / "Scripts" / "conda.exe"
            self.activate_script = self.conda_dir / "Scripts" / "activate.bat"
        else:
            self.conda_executable = self.conda_dir / "bin" / "conda"
            self.activate_script = self.conda_dir / "bin" / "activate"

    def download_miniconda(self):
        """Download appropriate Miniconda installer"""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "windows":
            url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
            installer = self.root_dir / "miniconda_installer.exe"
        elif system == "darwin":
            if machine == "arm64":
                url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
            else:
                url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
            installer = self.root_dir / "miniconda_installer.sh"
        else:  # Linux
            if machine == "aarch64":
                url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
            else:
                url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
            installer = self.root_dir / "miniconda_installer.sh"

        print(f"Downloading Miniconda from {url}")
        urllib.request.urlretrieve(url, installer)
        return installer

    def install_miniconda(self, installer):
        """Install Miniconda to local directory"""
        if platform.system().lower() == "windows":
            subprocess.run(
                [str(installer), "/S", "/D=" + str(self.conda_dir)], check=True
            )
        else:
            os.chmod(installer, 0o755)
            subprocess.run(
                ["bash", str(installer), "-b", "-p", str(self.conda_dir)], check=True
            )

        # Clean up installer
        installer.unlink()

    def create_environment(self):
        """Create isolated conda environment with specified Python version.
        This environment will contain all project dependencies and avoid system conflicts.
        """
        subprocess.run(
            [
                str(self.conda_executable),
                "create",
                "-y",
                "-n",
                self.env_name,
                f"python={self.python_version}",
            ],
            check=True,
        )

    def install_conda_dependencies(self):
        """Install system-level dependencies via conda package manager.
        Installs ffmpeg (audio/video processing) and git (version control).
        """
        subprocess.run(
            [
                str(self.conda_executable),
                "install",
                "-y",
                "-n",
                self.env_name,
                "ffmpeg",
                "git",
            ],
            check=True,
        )

    def install_pip_dependencies(self):
        """Install Python dependencies from requirements.txt within the conda environment.
        Also installs ML frameworks: PyTorch, TorchAudio, and model serving libraries.
        """
        # Determine how to activate the environment based on operating system
        if platform.system().lower() == "windows":
            activate_cmd = f"call {self.activate_script} {self.env_name}"
        else:
            activate_cmd = f"source {self.activate_script} {self.env_name}"

        # Build pip install command with project requirements and additional ML packages
        pip_install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
        pip_install_cmd += (
            " && pip install torch torchaudio funasr modelscope huggingface_hub onnx"
        )

        if platform.system().lower() == "windows":
            subprocess.run(pip_install_cmd, shell=True, check=True)
        else:
            subprocess.run(["bash", "-c", pip_install_cmd], check=True)

    def check_environment(self):
        """Verify that the conda environment exists, create and provision it if missing.
        Handles initial setup of isolated Python environment with all required packages.
        """
        result = subprocess.run(
            [str(self.conda_executable), "env", "list"],
            capture_output=True,
            text=True,
            check=True,
        )
        if self.env_name not in result.stdout:
            self.create_environment()
            self.install_conda_dependencies()
            self.install_pip_dependencies()

    def setup(self):
        """Execute complete environment setup process from scratch.
        Includes Miniconda installation, environment creation, and dependency provisioning.
        """
        if not self.conda_dir.exists():
            installer = self.download_miniconda()
            self.install_miniconda(installer)

        # Verify or create the isolated Python environment with all dependencies
        self.check_environment()
