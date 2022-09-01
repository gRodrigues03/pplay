# coding= utf-8

# Pygame and system modules
import sys
import pygame
from pygame.locals import *
from . import keyboard, mouse, point

# Initializes pygame's modules
pygame.init()

"""A simple Window class, it's the primary Surface(from pygame).
All the other game's renderable objects will be drawn on it. """


class Window:
	# A class attribute in Python, this case is similar to Java statics
	screen = None

	"""Initialize a Window (width x height)"""

	def __init__(self, width, height):
		# Input controllers
		Window.keyboard = keyboard.Keyboard()
		Window.mouse = mouse.Mouse()

		# Size
		info = pygame.display.Info()  # Gets the monitor resolution
		self.screen_width = info.current_w  # Saves it, duh
		self.screen_height = info.current_h
		self.width = width  # Normal, same as before
		self.height = height
		# Gets both aspect ratios (maybe there is a better way to do it, but this is the way I found)
		self.aspect_ratio = self.height / self.width
		self.inevrted_aspect_ratio = self.width / self.height

		# Window size flags
		self.fullscreen = False
		self.resizable = True

		# Pattern color
		self.color = [0, 0, 0]  # Black

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
		Window.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)  # Real window
		Window.fake_screen = Window.screen.copy()  # Game screen
		Window.screen_new_size = (self.width, self.height)  # Sent to pygame transform when resizing the fake screen
		Window.screen_distance = 0, 0  # The distance between the game screen and real window borders
		# Whenever both aspect ratios are different, the game screen is drawn in the middle of the window
		Window.mouse_pos = [0, 0]
		# Reinterpreted mouse position.
		# In short, it doesn't get wacky coordinates from the resized window and only applies to the game screen.

		Window.camera = point.Point(0, 0)
		# Sets pattern starting conditions
		self.set_background_color(self.color)
		self.set_title(self.title)

		# Updates the entire screen if no arguments are passed
		# Can be used to update portions of the screen (Rect list)
		pygame.display.update()

	# ------------------------TODO - VIDEO RESIZE METHODS----------------------
	"""Not implemented yet - Sets the Window to Fullscreen"""

	# Unfortunately, it must save the old screen (buffer) and
	# blit (transfer, see pygame doc) to the new FSCREEN

	# Done!, it is a bit slower than usual, but hey, it works
	# And I've made so it doesn't stretch the aspect ratio
	# instead, it fits the window size while maintaining the aspect ratio
	def set_fullscreen(self, value=True):
		if value:
			if not self.fullscreen:
				self.fullscreen = True
				Window.screen = pygame.display.set_mode((self.screen_width, self.screen_height), FULLSCREEN)
				self.update_aspect_ratio()
		else:
			self.restoreScreen()

	"""Not implemented yet - Disable the full display mode"""

	# Implemented!

	# Yeah.. guess what..
	# I did it lol
	# It now restores the original size and exits fullscreen
	def restoreScreen(self):
		if self.fullscreen:
			self.fullscreen = False
			if self.resizable:
				Window.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
			else:
				Window.screen = pygame.display.set_mode((self.width, self.height))
			self.update_aspect_ratio()

	"""Not implemented yet - Sets the Window resolution"""

	def is_fullscreen(self):
		return self.fullscreen

	def is_resizable(self):
		return self.resizable

	# The same problem as fullscreen
	def set_resolution(self, width, height):
		pass

	# I don't think that altering the game resolution makes sense, but maybe the altering the upscaled screen does

	# TODO

	# Defines if the window is resizable
	# updates it and does stuff
	def set_resizable(self, value=True):
		if value:
			if not self.resizable:
				self.resizable = True
				if not self.fullscreen:
					Window.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
					self.update_aspect_ratio()
		else:
			self.resizable = False
			if not self.fullscreen:
				self.restoreScreen()

	# -----------------------CONTROL METHODS---------------------------
	"""Refreshes the Window - makes changes visible, AND updates the Time"""

	def update(self):
		# Draw the game screen onto the real window, takes a bit of time, but I think it is worth it...
		Window.screen.blit(pygame.transform.scale(Window.fake_screen, Window.screen_new_size), Window.screen_distance)
		pygame.display.update()  # refresh
		for event in pygame.event.get():  # necessary to not get errors
			if event.type == QUIT:
				self.close()
			elif event.type == VIDEORESIZE:
				if not self.fullscreen and self.resizable:
					Window.screen = pygame.display.set_mode(event.size, RESIZABLE)
					self.update_aspect_ratio()  # Updates the game's 'fake screen' size only when necessary
		self.update_mouse()  # Updates the mouse cursor coordinates to fit the new game's 'fake screen' size
		self.last_time = self.curr_time  # set last frame time
		self.curr_time = pygame.time.get_ticks()  # since pygame.init()
		self.total_time += (self.curr_time - self.last_time)  # == curr_time

	# Updates the game's 'fake screen' size and distance from the border
	# so that it fits the resized window a.k.a. the 'real screen'
	def update_aspect_ratio(self):
		w, h = Window.screen.get_rect().size
		if h / w > self.aspect_ratio:
			Window.screen_new_size = (w, w * self.aspect_ratio)
		else:
			Window.screen_new_size = (h * self.inevrted_aspect_ratio, h)
		Window.screen_distance = (Window.screen_new_size[0] - w) / -2, (Window.screen_new_size[1] - h) / -2

	# Updates the mouse cursor coordinates to fit the new game's 'fake screen' size
	# I believe it doesn't break anything
	# The mouse class now returns window.Window.mouse_pos instead, works fine
	# It used to update this coordinate everytime the get_position() was used
	# Now it's only when the window updates
	def update_mouse(self):
		Window.mouse_pos = list(pygame.mouse.get_pos())
		fake_screen_size = Window.fake_screen.get_rect().size
		real_screen_size = Window.screen.get_rect().size
		rmax = real_screen_size[0] - Window.screen_distance[0]
		Window.mouse_pos[0] = ((Window.mouse_pos[0] - Window.screen_distance[0]) / (rmax - Window.screen_distance[0])) * fake_screen_size[0]
		rmax = real_screen_size[1] - Window.screen_distance[1]
		Window.mouse_pos[1] = ((Window.mouse_pos[1] - Window.screen_distance[1]) / (rmax - Window.screen_distance[1])) * fake_screen_size[1]

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

	def close(self):
		pygame.quit()
		sys.exit()

	# ---------------------GETTERS AND SETTERS METHODS-----------------
	"""
	Changes background color - receives a vector [R, G, B] value
	Example: set_background_color([0,0,0]) -> black
	or set_background_color([255,255,255]) -> white
	"""

	def set_background_color(self, RGB):
		self.color = RGB
		# !CHANGED: now it draws onto the fake screen
		Window.fake_screen.fill(self.color)

	# !Implement later possible strings values, such as:
	# "red","green","blue"..!
	# Rodrigs: Too many ifs and elses for something that's called every frame and is not
	# used very often. Maybe values as constants tho? that would come in handy.

	"""Gets the color attribute (background)"""

	def get_background_color(self):
		return self.color

	"""Sets the title of the Window"""

	def set_title(self, title):
		self.title = title
		pygame.display.set_caption(title)

	"""Gets the title of the Window"""

	def get_title(self):
		return self.title

	"""Sets the Window icon"""
	# The icon can be a GameImage, Sprite, path to an image or a pygame surface.
	def set_icon(self, path):
		if type(path) == str:
			img = pygame.image.load(path)
		elif path.__class__.__name__ == 'GameImage' or path.__class__.__name__ == 'Sprite':
			img = path.image
		elif path.__class__.__name__ == 'Animation':
			print('PPlay error: Window.set_icon\nAnimation type object cannot be used as an icon.\nObjeto do tipo Animation não pode ser usado como ícone.')
			return
		else:
			img = path
		pygame.display.set_icon(img)


	# ----------------------TIME CONTROL METHODS--------------------------

	"""Pause the program for an amount of time - milliseconds"""

	# Uses the processor to make delay accurate instead of
	# pygame.time.wait that SLEEPS the proccess
	def delay(self, time_ms):
		pygame.time.delay(time_ms)

	"""
	Returns the time passed between
	the last and the current frame - SECONDS
	"""

	def delta_time(self):
		return (self.curr_time - self.last_time) / 1000.0

	"""Returns the total time passed since the Window was created"""

	def time_elapsed(self):
		return self.total_time

	# ------------------------DRAW METHODS-------------------------------
	"""
	Draw a text on the screen at X and Y co-ords, using [R, G, B] color
	[with the specified font,
		   [with the specified size,
				   [Bold,
						 [Italic]]]]
	"""

	def draw_text(self, text, x, y, size=12, color=(0, 0, 0),
				  font_name="Arial", bold=False, italic=False):
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
		Window.fake_screen.blit(font_surface, [x, y])

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
