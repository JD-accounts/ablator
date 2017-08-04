import random
from typing import Optional

from .models import Functionality, Flavor, ClientUser, Availability


def can_i_use(client_user: ClientUser, functionality: Functionality) -> bool:
    """
    Is the specified user allowed to use the feature?

    Returns `True` if the specified ClientUser is allowed to use the functionality group,
    `False` if the user is disallowed, or the functionality group does not exist.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    functionality = which(client_user, functionality)
    if functionality:
        return functionality.is_enabled
    return False


def _availability_or_none(availability):
    if availability:
        if availability.is_enabled:
            return availability
    return None


def which(client_user: ClientUser, functionality: Functionality) -> Optional[Availability]:
    """
    Which Flavor of the given Functionality is enabled for the user, if any?

    Returns a Flavor object that corresponds to the ClientUser's enabled functionality,
    or `None` if the user does not have any Flavor in the given Functionality.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """

    # Check Roll Out Strategy
    if functionality.rollout_strategy == Functionality.RECALL_FEATURE:
        return None

    if functionality.rollout_strategy == Functionality.ENABLE_GLOBALLY:
        Availability(
            functionality_group=Functionality.flavor_set.first(),
            is_enabled=True
        )

    # Retrieve Availability and Flavor Instances
    try:
        availability = Availability.objects.select_related('flavor').get(
            flavor__in=functionality.flavor_set.all(),
            user=client_user
        )
    except Availability.DoesNotExist:
        availability = None

    # Easiest Case: Already enabled
    if availability and availability.is_enabled:
        return availability

    # Already Exists, but disabled
    if availability and not availability.is_enabled:
        if functionality.rollout_strategy == Functionality.PAUSE_ROLLOUT:
            return availability.functionality
        elif functionality.rollout_strategy == Functionality.DEFINED_BY_RELEASES:
            enabled_count = Availability.objects.filter(
                flavor__functionality=functionality,
                is_enabled=True
            ).count()
            if functionality.current_release.max_enabled_users > enabled_count:
                availability.is_enabled = True
                availability.save()
            return _availability_or_none(availability)

    # Check if Rollout is paused
    if functionality.rollout_strategy == Functionality.PAUSE_ROLLOUT:
        return None

    # Availability does not yet exist. Choose a Flavor at random
    if not functionality.current_release:
        return None

    flavors = functionality.flavor_set.all()
    if flavors:
        availability = Availability()
        availability.user = client_user
        availability.flavor = random.choice(flavors)

        enabled_count = Availability.objects.filter(
            flavor__functionality=functionality,
            is_enabled=True
        ).count()
        availability.is_enabled = (
            functionality.current_release.max_enabled_users > enabled_count
        )
        availability.save()
    return _availability_or_none(availability)
