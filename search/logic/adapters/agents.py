from random import choice

from logic.adapters.base import BaseAdapter
from parameters.models import UserAgent


class UserAgentAdapter(BaseAdapter):
    """Adapter for creating and fetching user agents from database."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = UserAgent

    def get_random_user_agent(self) -> UserAgent:
        """
        Retrieve random UserAgent object from database.
        """
        agents = self.agent.objects.all()
        return choice(agents)
