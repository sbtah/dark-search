"""
Test cases for User Agents object.
"""
import pytest
from parameters.models import UserAgent
from django.core.exceptions import ValidationError


pytestmark = pytest.mark.django_db


class TestUserAgentsModel:
    """Test cases for User Agents object."""

    def test_create_user_agents(self):
        """Test creating UserAgents object is successful."""
        assert UserAgent.objects.count() == 0
        agents = UserAgent.objects.create(
            value='Mozilla/5.0 Test Agent'
        )
        assert UserAgent.objects.count() == 1
        assert isinstance(agents, UserAgent)

    def test_user_agents_str_method(self):
        """Test that UserAgent's __str__ is generating proper output."""
        agent = UserAgent.objects.create(
            value='Mozilla/5.0 Test Agent'
        )
        assert str(agent) == f'{agent.type}:{agent.value}:{agent.created}'
