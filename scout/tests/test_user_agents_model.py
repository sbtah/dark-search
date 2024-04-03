"""
Test cases for User Agents object.
"""
import pytest
from parameters.models import UserAgents
from django.core.exceptions import ValidationError


pytestmark = pytest.mark.django_db


class TestUserAgentsModel:
    """Test cases for User Agents object."""

    def test_create_user_agents(self):
        """Test creating UserAgents object is successful."""
        assert UserAgents.objects.count() == 0
        agents = UserAgents.objects.create()
        assert UserAgents.objects.count() == 1
        assert isinstance(agents, UserAgents)

    def test_user_agents_singleton(self):
        """Test that only 1 UserAgents object can be created."""
        UserAgents.objects.create()
        assert UserAgents.objects.count() == 1
        with pytest.raises(ValidationError):
            UserAgents.objects.create()

    def test_user_agents_str_method(self):
        """Test that UserAgent's __str__ is generating proper output."""
        agent = UserAgents.objects.create()
        assert str(agent) == 'Current User-Agents'
