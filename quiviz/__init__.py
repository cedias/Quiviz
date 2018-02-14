from .quiviz import *
import logging
import sys
import os

logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=f"/home/dias/xp_log/{'_'.join(sys.argv).replace('/','_')}.qvzlog",
                        level=logging.INFO)

## Auto import LoggingObs
register(LoggingObs())