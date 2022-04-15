from os.path import exists as file_exists
from json import load as json_load, dumps as json_dumps


class StateMachine:
    ENCODING = "UTF-8"

    def __init__(self, filename="state_db.json"):
        self.dbname = filename

        self.states = {}
        if file_exists(filename):
            self.read_database(filename)

    def get(self, user_id):
        return self.states.get(str(user_id), None)

    def change(self, user_id, state):
        self.states[str(user_id)] = state
        self.update_database()

    def update_database(self):
        with open(self.dbname, "w", encoding=StateMachine.ENCODING) as file:
            json_dumps(file)

    def read_database(self, filename):
        with open(filename, "r", encoding=StateMachine.ENCODING) as file:
            self.states = json_load(file)
