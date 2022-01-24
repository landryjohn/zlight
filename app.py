import logging, requests, os

from telegram import Telegram
from utils import CITIES 

TOKEN = ""

PORT = int(os.environ.get("ZLIGHT_PORT", 5000))

# Enable logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def cuts() -> object:
    req = '/coupure EST'
    #  Verify if only one city is requested, multiple cities if for the next version of the bot
    city = [city for city in req.split() if city.upper() in CITIES.keys()]
    if any(city) and len(city) < 2 :
        try :
            resp = requests.post(url="https://alert.eneo.cm/ajaxOutage.php", data={'region':CITIES[city[0]]}).json()
            return resp
        except Exception as error :
            print("An error occured ", error) 
    else : 
        return {'status': False, 'message': "Vous devez fournir une seule ville valide"}


if __name__ == "__main__" :
    r = cuts() 
