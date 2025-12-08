import logging
import sys
import traceback
from pathlib import Path

from danfe_generator.web.app import main

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.error("Fatal error in main loop")
        traceback.print_exc()
        sys.exit(1)
