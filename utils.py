import random

def random_delay(lower_lim, upper_lim):
	return random.random() * (upper_lim - lower_lim) + lower_lim