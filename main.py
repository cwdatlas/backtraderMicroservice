import logging
import os

from Controllers.BacktraderController import btrader

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, force=True)
    btrader.run(host=os.environ.get("FLASK_IP"))
    btrader.run(debug=True)
