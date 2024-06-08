from random import choice

from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.agents import NoUserAgentsError
from parameters.models import UserAgent


class UserAgentAdapter(BaseAdapter):
    """Adapter for creating and fetching user agents from database."""

    def __init__(self, *args, **kwargs):
        self.agent = UserAgent
        super().__init__(*args, **kwargs)

    def get_random_user_agent(self) -> UserAgent:
        """
        Retrieve random UserAgent object from database.
        """
        agents = self.agent.objects.all()
        if not agents:
            raise NoUserAgentsError()
        return choice(agents)
