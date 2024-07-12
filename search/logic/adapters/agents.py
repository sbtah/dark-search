from random import choice
from typing import Any

from django.db.models import QuerySet
from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.agents import NoUserAgentsError
from parameters.models import UserAgent


class UserAgentAdapter(BaseAdapter):
    """Adapter for creating and fetching user agents from database."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.agent = UserAgent
        super().__init__(*args, **kwargs)

    def sync_get_or_create_user_agent(self, user_agent: str) -> UserAgent:
        """
        Create new UserAgent object or return existing one.
        - :arg user_agent: String representing browser User Agent.
        """
        try:
            existing_agent: UserAgent = self.agent.objects.get(value=user_agent)
            self.logger.debug(
                f'UserAgent Adapter, found existing User Agent: user_agent_id="{existing_agent.id}", '
                f'value="{user_agent}"'
            )
            return existing_agent
        except UserAgent.DoesNotExist:
            new_agent: UserAgent = self.agent.objects.create(value=user_agent)
            self.logger.debug(
                f'UserAgent Adapter, created new User Agent: user_agent_id="{new_agent.id}", '
                f'value="{user_agent}"'
            )
            return new_agent

    def get_random_user_agent(self) -> UserAgent:
        """
        Retrieve random UserAgent object from database.
        """
        agents: QuerySet[UserAgent | None] = self.agent.objects.all()
        if not agents:
            raise NoUserAgentsError()
        return choice(agents)
