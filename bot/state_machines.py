from os.path import exists as file_exists
from json import load as json_load, dump as json_dump


class StateMachine:
    _ENCODING = "UTF-8"
    __doc__ = """
        --------- EXAMPLE ---------
        
        states = StateMachine()
        states.add(121241, "start")
        user_current_state = states.get(121241)
        if user_current_state is not None:
            do_some_actions()
        """

    def __init__(self, filename="state_db.json"):
        self._dbname = filename

        self._states = {}
        if file_exists(filename):
            self._read_database(filename)

    def get(self, user_id):
        return self._states.get(str(user_id), None)

    def add(self, user_id, state):
        self._states[str(user_id)] = state
        self._update_database()

    def _update_database(self):
        with open(self._dbname, "w", encoding=StateMachine._ENCODING) as file:
            json_dump(self._states, file)

    def _read_database(self, filename):
        with open(filename, "r", encoding=StateMachine._ENCODING) as file:
            self._states = json_load(file)
