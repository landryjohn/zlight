import logging, requests, os
from turtle import update

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import utils

TOKEN = ""

PORT = int(os.environ.get("ZLIGHT_PORT", 5000))

# Enable logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define commands handlers. 
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when bot receive the command /start"""
    update.message.reply_text(utils.MESSAGE)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when bot receive the command /aide"""
    update.message.reply_text(utils.HELP)

def author(update: Update, context: CallbackContext) -> None:
    """Send the author name /aide"""
    update.message.reply_text("lnjohn ;)")

def cuts() -> object:
    req = '/coupure EST'
    #  Verify if only one valid city is requested, multiple cities if for the next version of the bot
    city = [city for city in req.split() if city.upper() in utils.CITIES.keys()]
    if any(city) and len(city) < 2 :
        try :
            # Send request to the API
            resp = requests.post(url="https://alert.eneo.cm/ajaxOutage.php", data={'region':utils.CITIES[city[0]]}).json()
            formated_resp = ''
            for cut in resp['data']:
                formated_resp += '=============PROGRAMME DE COUPURE===============\n'
                formated_resp += f"REGION: {cut['region']}\n"
                formated_resp += f"VILLE: {cut['ville']}\n"
                formated_resp += f"DATE : {cut['prog_date']} | HEURE DEBUT : {cut['prog_heure_debut']} | HEURE FIN : {cut['prog_heure_fin']}\n"
                formated_resp += f"DETAILS : {cut['observations']}\n"  
                formated_resp += '================================================\n\n'
            return formated_resp if any(formated_resp) else "AUCUN PROGRAMME DE COUPURE DANS CETTE ZONE" 
        except Exception as error :
            print("An error occured ", error) 
    else : 
        return {'status': False, 'message': "Vous devez fournir une seule ville valide"}

def main() -> None:
    """Start the bot"""

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to registrer handler
    dispatcher = updater.dispatcher 

    # trigger differents command 
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('coupures', cuts))
    dispatcher.add_handler(CommandHandler('author', author))
    
    # on non command
    dispatcher.add_handler(MessageHandler(Filters.text and ~Filters.command, help_command))

    # Starting the bot 
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN
    )

    updater.bot.set_webhook("https://still-shore-89901.herokuapp.com/" + TOKEN)

    updater.idle()

if __name__ == "__main__" :
    main()