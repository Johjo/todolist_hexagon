from collections import OrderedDict

from todolist_hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from todolist_hexagon.shared.type import UserKey


class ResetFvpSession:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions : FvpSessionSetPort = set_of_fvp_sessions

    def execute(self, user_key: UserKey):
        self.set_of_fvp_sessions.save(user_key=user_key, snapshot=FvpSnapshot(OrderedDict()))

