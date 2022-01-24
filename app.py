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
    #  Verify if only one valid city is requested, multiple cities if for the next version of the bot
    city = [city for city in req.split() if city.upper() in CITIES.keys()]
    if any(city) and len(city) < 2 :
        try :
            # Send request to the API
            resp = requests.post(url="https://alert.eneo.cm/ajaxOutage.php", data={'region':CITIES[city[0]]}).json()
            formated_resp = ''
            for cut in resp['data']:
                formated_resp += '=============PROGRAMME DE COUPURE===============\n'
                formated_resp += f"REGION: {cut['region']}\n"
                formated_resp += f"VILLE: {cut['ville']}\n"
                formated_resp += f"DATE : {cut['prog_date']} | HEURE DEBUT : {cut['prog_heure_debut']} | HEURE FIN : {cut['prog_heure_fin']}\n"
                formated_resp += f"DETAILS : {cut['observations']}\n"  
                formated_resp += '================================================\n\n'
            return formated_resp
        except Exception as error :
            print("An error occured ", error) 
    else : 
        return {'status': False, 'message': "Vous devez fournir une seule ville valide"}

if __name__ == "__main__" :
    resp = cuts()
    if any(resp) :   
        print(resp)
    else :
        print("AUCUN PROGRAMME DE COUPURE DANS CETTE ZONE") 

