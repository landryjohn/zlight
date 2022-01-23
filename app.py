import logging, requests, os
import re

from telegram import Update
from .cities import CITIES 

TOKEN = ""

PORT = int(os.environ.get("ZLIGHT_PORT", 5000))

# Enable logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def cuts() -> None :
    integrity = True 
    req = 'VILLE=CENTRE'
    if re.fullmatch('[A-Za-z]*=[A-Za-z]*', req.strip().replace(' ','')) :
        query,target = req.split('=')
        integrity = query in ['VILLE', 'REGION'] and True 
        # TODO : control the integrity of the command 


# if __name__ == "__main__" :
#     main() 
