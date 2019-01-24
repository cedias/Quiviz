from .quiviz import *
import logging
import sys
import os
import json
from pathlib import Path

#Find or create folder
if Path.exists(Path.home()/".quiviz_rc"):

    with open(Path.home()/".quiviz_rc") as config:
        config_data = json.load(config)
        base_path = Path(os.path.expanduser(config_data.get("log_base_path",".")))
else:

    base_path = Path.cwd() / "quiviz_logs"

script_name = sys.argv[0].split('.')[0]
instance_name = '_'.join(sys.argv).replace('/','_')+".qzlog"

Path.mkdir(base_path / script_name,parents=True,exist_ok=True) #creates missing files
log_file  = base_path / script_name / instance_name

print(f"Quiviz logging to {log_file}")
#Register logging
logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ],
                        level=logging.INFO)


logging.info(f"\n\n$ {'_'.join(sys.argv)}\n--> new run:\n\n")

## Auto import LoggingObs
register(LoggingObs())
set_xp_name(sys.argv)