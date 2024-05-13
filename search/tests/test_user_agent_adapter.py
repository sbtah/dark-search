"""
Test cases for UserAgentAdapter.
"""
import pytest
from logic.adapters.agents import UserAgentAdapter
from parameters.models import UserAgent


pytestmark = pytest.mark.django_db


class TestUserAgentsAdapter:
    """Test cases for UserAgentAdapter."""

    def test_get_random_user_agent(self, many_agents):
        """Test that get_random_user_agent is returning UserAgent object."""
        agents = UserAgent.objects.all()
        assert len(agents) > 1
        agent = UserAgentAdapter().get_random_user_agent()
        assert isinstance(agent, UserAgent)