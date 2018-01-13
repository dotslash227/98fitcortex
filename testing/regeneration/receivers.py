from django.dispatch import receiver

from .signals import diet_regeneration , workout_regeneration
from .utils import get_window_tuples , create_diet_regeneration_node , create_workout_regeneration_node

import epilogue.constants

import logging

@receiver(diet_regeneration)
def diet_regenerator(sender , *args , **kwargs):
	user = kwargs.pop('user')
	logger = logging.getLogger(__name__)
	logger.debug("Received Diet Regeneration")
	eligible_window = get_window_tuples()

	return [
		create_diet_regeneration_node(user,*t) for t in eligible_window
	]


@receiver(workout_regeneration)
def workout_regenerator(sender , *args, **kwargs):
	user = kwargs.pop('user')
	eligible_window = get_window_tuples()

	logger = logging.getLogger(__name__)
	logger.debug("Received Workout Regeneration")

	return [
		create_workout_regeneration_node(user,*t) for t in eligible_window
	]