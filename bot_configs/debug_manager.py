import io
import requests


class DebugManager(io.StringIO):
    """ Менеджер для отладки ошибок. Отправляет сообщение администраторам """

    def __init__(self, config_data, admins):
        super().__init__()
        self.config_data = config_data
        self.admins = admins

    def send_debug_message(self, message):
        for admin in self.admins:
            requests.get(f"https://api.telegram.org/bot{self.config_data.BOT_TOKEN}/sendMessage",
                         data={"chat_id": admin, "text": message})

    def write(self, *args, **kwargs):
        self.send_debug_message(*args)
