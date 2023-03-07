from .settings import logger, TeleGram_info
import telegram

class TeleGram:
    def __init__(self):
        self.telegram_token = TeleGram_info['telegram_token'] 
        self.telegram_chat_id = TeleGram_info['telegram_chat_id']
        self.bot = telegram.Bot(token = self.telegram_token)
    
    def send_photo(self, photo_name, template):
        try:
            self.bot.sendPhoto(chat_id = self.telegram_chat_id, photo = open(photo_name, 'rb'), caption = template)
        except Exception as e:
            logger(e)
    
    def send_message(self, message):
        try:
            self.bot.sendMessage(chat_id = self.telegram_chat_id, text = message)
        except Exception as e:
            logger(e)   