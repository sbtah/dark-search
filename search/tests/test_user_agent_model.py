"""
Test cases for User Agents object.
"""
import pytest
from parameters.models import UserAgent


pytestmark = pytest.mark.django_db


class TestUserAgentsModel:
    """Test cases for User Agents object."""

    def test_create_user_agent(self):
        """Test creating UserAgents object is successful."""
        assert UserAgent.objects.count() == 0
        agent = UserAgent.objects.create(
            value='Mozilla/5.0 Test Agent'
        )
        assert UserAgent.objects.count() == 1
        assert isinstance(agent, UserAgent)

    def test_user_agent_str_method(self, user_agent):
        """Test that UserAgent's __str__ is generating proper output."""
        agent = user_agent
        assert str(agent) == f'{agent.type}:{agent.value}:{agent.created}'
