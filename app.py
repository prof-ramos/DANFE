import sys
from pathlib import Path

# Adiciona src ao path para que os imports funcionem corretamente
# quando executado da raiz (como faz o Hugging Face Spaces)
sys.path.append(str(Path(__file__).parent / "src"))

from danfe_generator.web.app import main

if __name__ == "__main__":
    main()
