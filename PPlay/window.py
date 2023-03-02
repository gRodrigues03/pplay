# Pygame and system modules
import sys
import pygame
from pygame.locals import *
from . import keyboard, mouse, point

"""A simple Window class, it's the primary Surface(from pygame).
All the other game's renderable objects will be drawn on it. """


class Window:
	# A class attribute in Python, this case is similar to Java statics
	screen = None
	fake_screen = None
	screen_distance = point.Point(0, 0)  # The distance between the game screen and real window borders
	mouse_pos = [0, 0]
	camera = None
	actual_camera = None
	keyboard = keyboard.Keyboard()
	mouse = mouse.Mouse()
	deltatime = 0
	animation_deltatime = 0
	"""Initialize a Window (width x height)"""

	def __init__(self, width, height):
		# Size
		info = pygame.display.Info()  # Gets the monitor resolution
		pygame.event.set_allowed([QUIT, VIDEORESIZE])
		self.screen_width = info.current_w  # Saves it, duh
		self.screen_height = info.current_h

		self.width = width  # Normal, same as before
		self.height = height
		# Gets both aspect ratios (maybe there is a better way to do it, but this is the way I found)
		self.aspect_ratio = self.height / self.width

		# Window size flags
		self.fullscreen = False
		self.resizable = True

		# Pattern Title
		self.title = "Title"

		# Time Control
		self.curr_time = 0  # current frame time
		self.last_time = 0  # last frame time
		self.total_time = 0  # += curr-last(delta_time), update()

		# Creates the screen (pygame.Surface)
		# There are some useful flags (look pygame's docs)
		# It's like a static attribute in Java

		# Now it has 2 screens. one for the game and another for the window
		# The game screen fits the window maintaining the original self.width and self.height
		Window.screen = pygame.display.set_mode((self.width, self.height))  # Real window
		Window.fake_screen = Window.screen.copy()  # Game screen
		Window.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)  # Re-declaration of the real window
		# Whenever both aspect ratios are different, the game screen is drawn in the middle of the window
		# In short, it doesn't get wacky coordinates from the resized window and only applies to the game screen.

		Window.camera = point.Point(0, 0)
		Window.actual_camera = point.Point(0, 0)

		# Sets pattern starting conditions
		self.set_background_color((255, 255, 255))
		self.set_title(self.title)

		# Updates the entire screen if no arguments are passed
		# Can be used to update portions of the screen (Rect list)
		pygame.display.update()

	# ------------------------VIDEO RESIZE METHODS----------------------
	"""Not implemented yet - Sets the Window to Fullscreen"""

	# Unfortunately, it must save the old screen (buffer) and
	# blit (transfer, see pygame doc) to the new FSCREEN

	# Done!, it is a bit slower than usual, but hey, it works
	def set_fullscreen(self, value=True):
		if value:
			if not self.fullscreen:
				self.fullscreen = True
				self.update_aspect_ratio((self.screen_width, self.screen_height), FULLSCREEN)
		else:
			self.restoreScreen()

	"""Not implemented yet - Disable the full display mode"""

	# Implemented!

	# Yeah.. guess what...
	# I did it lol
	# It now restores the original size and exits fullscreen
	def restoreScreen(self):
		if self.fullscreen:
			self.fullscreen = False
			self.update_aspect_ratio((self.width, self.height))
			if not self.resizable:
				Window.screen = pygame.display.set_mode((self.width, self.height))

	"""Not implemented yet - Sets the Window resolution"""

	def is_fullscreen(self):
		return self.fullscreen

	def is_resizable(self):
		return self.resizable

	# Defines if the window is resizable
	# updates it and does stuff
	def set_resizable(self, value=True):
		if value:
			if not self.resizable:
				self.resizable = True
				if not self.fullscreen:
					Window.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
					self.update_aspect_ratio(self.width, self.height)
		else:
			self.resizable = False
			if not self.fullscreen:
				self.restoreScreen()

	# -----------------------CONTROL METHODS---------------------------
	"""Refreshes the Window - makes changes visible, AND updates the Time"""

	def update(self):
		# Draw the game screen onto the real window, takes a bit of time, but I think it is worth it...
		pygame.transform.scale(Window.fake_screen, Window.screen.get_rect().size, Window.screen)
		pygame.display.update()  # refresh
		for event in pygame.event.get():  # necessary to not get errors
			if event.type == QUIT:
				self.close()
			elif event.type == VIDEORESIZE:
				if not self.fullscreen and self.resizable:
					self.update_aspect_ratio(event.size)  # Updates the game's 'fake screen' size only when necessary
		self.update_aspect_ratio_offset()
		self.update_mouse()  # Updates the mouse cursor coordinates to fit the new game's 'fake screen' size
		self.last_time = self.curr_time  # set last frame time
		self.curr_time = pygame.time.get_ticks()  # since pygame.init()
		self.total_time += (self.curr_time - self.last_time)  # == curr_time
		Window.animation_deltatime = self.curr_time - self.last_time
		Window.deltatime = Window.animation_deltatime / 1000.0

	# Updates the game's 'fake screen' size and distance from the border
	# so that it fits the resized window a.k.a. the 'real screen'
	def update_aspect_ratio(self, size, mode=RESIZABLE):
		w, h = size
		new_as = h/w
		inverted_new_as = w/h
		if new_as > self.aspect_ratio:
			screen_new_size = (self.width, self.width * new_as)
			Window.screen_distance.x, Window.screen_distance.y = 0, (self.height - screen_new_size[1]) / -2
		else:
			screen_new_size = (self.height * inverted_new_as, self.height)
			Window.screen_distance.x, Window.screen_distance.y = (self.width - screen_new_size[0]) / -2, 0
		Window.screen = pygame.display.set_mode(screen_new_size)
		Window.fake_screen = Window.screen.copy()
		Window.screen = pygame.display.set_mode(size, mode)
		self.update_aspect_ratio_offset()

	# Updates the distance between the edge of the window and the original aspect_ratio.
	@classmethod
	def update_aspect_ratio_offset(cls):
		cls.actual_camera.x = cls.camera.x + cls.screen_distance.x
		cls.actual_camera.y = cls.camera.y + cls.screen_distance.y

	# Updates the mouse cursor coordinates to fit the new game's 'fake screen' size
	# I believe it doesn't break anything
	# The mouse class now returns window.Window.mouse_pos instead, works fine
	# It used to update this coordinate everytime the get_position() was used
	# Now it's only when the window updates
	@classmethod
	def update_mouse(cls):
		cls.mouse_pos = list(pygame.mouse.get_pos())
		fake_screen_size = cls.fake_screen.get_rect().size
		real_screen_size = cls.screen.get_rect().size
		cls.mouse_pos[0] = int((cls.mouse_pos[0] / real_screen_size[0]) * fake_screen_size[0])
		cls.mouse_pos[1] = int((cls.mouse_pos[1] / real_screen_size[1]) * fake_screen_size[1])

	# curr_time should be the REAL current time, but in Python
	# the method returns the time in seconds.
	# And we DO WANT MILLIseconds :P
	# While REAL time is not necessary, yet..

	"""Paints the screen - White - and update"""

	def clear(self):
		self.set_background_color([255, 255, 255])
		self.update()

	"""
	Closes the Window and stops the program - throws an exception
	"""
	@staticmethod
	def close():
		pygame.quit()
		sys.exit()

	# ---------------------GETTERS AND SETTERS METHODS-----------------
	"""
	Changes background color - receives a vector [R, G, B] value
	Example: set_background_color([0,0,0]) -> black
	or set_background_color([255,255,255]) -> white
	"""
	@classmethod
	def set_background_color(cls, RGB):
		# !CHANGED: now it draws onto the fake screen
		cls.fake_screen.fill(RGB)

	# !Implement later possible strings values, such as:
	# "red","green","blue"..!
	# Rodrigs: Too many ifs and elses for something that's called every frame and is not
	# used very often. Maybe values as constants tho? that would come in handy.
	# 02/09/2022: added in constants.py under the color class.

	"""Sets the title of the Window"""

	def set_title(self, title):
		self.title = title
		pygame.display.set_caption(title)

	"""Gets the title of the Window"""

	def get_title(self):
		return self.title

	"""Sets the Window icon"""
	# The icon can be a GameImage, Sprite, path to an image or a pygame surface.
	@staticmethod
	def set_icon(path):
		if type(path) == str:
			img = pygame.image.load(path)
		elif path.__class__.__name__ == 'GameImage' or path.__class__.__name__ == 'Sprite':
			img = path.image
		elif path.__class__.__name__ == 'Animation':
			print('PPlay error: Window.set_icon\nAnimation type object cannot be used as an icon.'
									'\nObjeto do tipo Animation não pode ser usado como ícone.')
			return
		else:
			img = path
		pygame.display.set_icon(img)

	# ----------------------TIME CONTROL METHODS--------------------------

	"""Pause the program for an amount of time - milliseconds"""

	# Uses the processor to make delay accurate instead of
	# pygame.time.wait that SLEEPS the proccess
	@staticmethod
	def delay(time_ms):
		pygame.time.delay(time_ms)

	"""
	Returns the time passed between
	the last and the current frame - SECONDS
	"""

	@classmethod
	def delta_time(cls):
		return cls.deltatime

	"""Returns the total time passed since the Window was created"""

	def time_elapsed(self):
		return self.total_time

	# ------------------------DRAW METHODS-------------------------------
	"""
	Draw a text on the screen at X and Y co-ords, using [R, G, B] color,
	with the specified font,[with the specified size, Bold, Italic
	"""
	@classmethod
	def draw_text(cls, text, x, y, size=12, color=(0, 0, 0), font_name="Arial", bold=False, italic=False):
		# Creates a Font from the system fonts
		# SysFont(name, size, bold=False, italic=False) -> Font
		font = pygame.font.SysFont(font_name, size, bold, italic)

		# Creates a pygame.Surface with the text rendered on it
		# render(text, antialias, color, background=None)->Surface
		font_surface = font.render(text, True, color)
		# That's because pygame does NOT provide a way
		# to directly draw text on an existing Surface.
		# So you must use Font.render() -> Surface and BLIT

		# Finally! BLIT!

		# !CHANGED: now it draws onto the fake screen
		cls.fake_screen.blit(font_surface, (x+Window.actual_camera.x, y+Window.actual_camera.y))

	# ---------------------CLASS METHODS--------------------------
	"""Returns the drawing surface"""

	@classmethod
	def get_screen(cls):
		# !CHANGED: now it returns the fake screen
		# I believe only draw functions use this...
		return cls.fake_screen

	"""Returns the camera position"""

	@classmethod
	def get_camera(cls):
		# !CHANGED: now it returns the fake screen
		# I believe only draw functions use this...
		return cls.camera

	"""Returns the keyboard input"""

	@classmethod
	def get_keyboard(cls):
		return cls.keyboard

	"""Returns the mouse input"""

	@classmethod
	def get_mouse(cls):
		return cls.mouse
