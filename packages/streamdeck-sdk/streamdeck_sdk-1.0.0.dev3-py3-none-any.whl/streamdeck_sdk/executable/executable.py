import argparse
import logging
import os
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(Path().resolve())
ASSETS_DIR = Path(__file__).parent / "assets"
BASE_PROJECT_DIR = ASSETS_DIR / "base_project"

now = datetime.now()
dt = now.strftime("%Y_%m_%d_%H_%M_%S")
RELEASE_DIR = BASE_DIR / f"releases/{dt}"


def main():
    parser = argparse.ArgumentParser(description='StreamDeckSDR')
    parser.add_argument('command')
    parser.add_argument('-i', default=None, required=False, type=str)
    args = parser.parse_args()
    logger.info(args)
    command = args.command
    if command == "startproject":
        shutil.copytree(BASE_PROJECT_DIR, BASE_DIR, symlinks=False, dirs_exist_ok=True)
        os.chmod(
            'DistributionTool',
            755,
        )
        os.chmod(
            'DistributionTool.exe',
            755,
        )
    elif command == "build":
        input_file = Path(args.i).resolve()
        os_name = platform.system()
        logger.info(os_name)
        RELEASE_DIR.mkdir(exist_ok=True, parents=True)
        if os_name == "Darwin":
            subprocess.run(
                [str(BASE_DIR / "DistributionTool"), "-b", "-i", input_file, "-o", str(RELEASE_DIR)],
            )
        elif os_name == "Windows":
            subprocess.run(
                [str(BASE_DIR / "DistributionTool.exe"), "-b", "-i", input_file, "-o", str(RELEASE_DIR)],
            )
