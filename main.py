import click
import chipwhisperer as cw

from subprocess import run
from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "CwCli"

data_dir = user_data_dir(APP_NAME)
os.makedirs(data_dir, exist_ok=True)

CW_REPO_PARENT = os.path.join(data_dir)
CW_REPO_PATH = CW_REPO_PARENT.join("chipwhisperer")
CW_REPO = "https://github.com/newaetech/chipwhisperer.git"

DEFAULT_FIRMWARE = 'mcu/simpleserial-base'
DEFAULT_PLATFORM = 'STM32F'

scope = cw.scope()
target = cw.target(scope, cw.targets.SimpleSerial)
scope.default_setup()


def clone_repo(repo, at=data_dir):
    if CW_REPO_PATH.exists():
        print("chipwhisperer repo already exists.")
    else:
        print("chipwhisperer repo does not exist!")
        print(f"Cloning chipwhisperer repo to f{data_dir}/chipwhisperer ...")
        r = run(f"git clone {repo}".split(), cwd=at, capture_output=True, text=True)
        if r.code == 0:
            print("Cloned repo successfully.")
        else:
            print("Cloning repo failed...")
            print(r.stdout)


def init():
    clone_repo(CW_REPO)


def build_firmware(firmware, platform):
    firmware_path = CW_REPO_PATH.join("firmware").join(firmware)
    r = run("make PLATFORM={platform} CRYPTO_TARGET=NONE", cwd=firmware_path, capture_output=True, text=True)
    print(f"Compiling for firmware {firmware} and platform {platform}", end='')

    if r.code == 0:
        print("successfully.")
        hex_path = firmware_path.join("firmware.hex")
        cw.program_target(scope, cw.programmers.STM32FProgrammer, hex_path)
    else:
        print("failed...")



@click.command()
@click.option("--firmware", "-f", default=DEFAULT_FIRMWARE, help="Name of firmware")
@click.option("--platform", "-f", default=DEFAULT_PLATFORM, help="Name of the platform")
def main(firmware, platform):
    init()
    build_firmware()


if __name__ == '__main__':
    main()
