import contextlib
import unittest.mock

with contextlib.redirect_stdout(unittest.mock.Mock()):
	import pygame