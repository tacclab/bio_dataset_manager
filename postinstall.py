import subprocess
import sys


def install_torch():
    print("Installing torch")
    # Use subprocess to run the pip install command
    # "pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 -f https://download.pyt
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.3.1+cu121", "torchvision==0.18.1+cu121",
                           "torchaudio==2.3.1+cu121", "-f", "https://download.pytorch.org/whl/cu121/torch_stable.html"])

    print("Finished installing torch")


if __name__ == "__main__":
    install_torch()
