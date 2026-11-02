import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  

PROJECT_ROOT = Path(__file__).resolve().parents[2]   

DATA_DIR = PROJECT_ROOT / os.environ.get("DATA_DIR", "data")

INTERVALS = (1, 2, 7, 14, 30)
