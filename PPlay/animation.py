# Pygame and System Modules
import pygame
from . import gameimage, window

"""An Animation class for frame-control."""


class Animation(gameimage.GameImage):
    """
    Creates an Animation that is composed by N frames.
    The method set_sequence_time must be called right after.
    Must note that the nnumber of frames will be automatically
    computated: if the image has 100px width and total_frames = 10,
    each frame will have 10px width.
    """
    deltatime = 0

    def __init__(self, image_file, total_frames, loop=True):
        # Parent's constructor must be first-called
        gameimage.GameImage.__init__(self, image_file)

        # A Cast to force it to be a float division
        self.width = self.width/float(total_frames)  # The width of each frame

        # Playing Control
        self.playing = True
        self.loop = loop

        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.final_frame = total_frames

        self.image_sequence = []
        self.create_image_sequence()

        # The duration of each frame
        self.frame_duration = 0
        self.total_duration = 0

        self.set_sequence(0, self.total_frames, self.loop)
        self.set_total_duration(100)
        self.curr_time = self.frame_duration

        # -----------------------SEQUENCE SETTERS-----------------
    """
    Sets some aspects of the sequence, init/final frame, loop..
    """
    def create_image_sequence(self):
        clip_rect = pygame.Rect(0 * self.width, 0, self.width, self.height)
        for i in range(self.total_frames + 1):
            self.image_sequence.append(pygame.Surface((self.width, self.height), pygame.SRCALPHA))
            clip_rect.x = i * self.width
            self.image_sequence[i].blit(self.image, (0, 0), area=clip_rect)
            self.image_sequence[i] = pygame.transform.flip(self.image_sequence[i], self.flipped_x, self.flipped_y)

    def flip_image_sequence(self, x, y):
        for i in range(self.total_frames + 1):
            self.image_sequence[i] = pygame.transform.flip(self.image_sequence[i], x, y)

    def set_sequence(self, initial_frame, final_frame, loop=True):
        self.set_initial_frame(initial_frame)
        self.set_curr_frame(initial_frame)
        self.set_final_frame(final_frame)
        self.set_loop(loop)

    """Defines each frame duration and the sequence (time / total_frames)."""
    def set_sequence_time(self, initial_frame, final_frame,
                          total_duration, loop=True):
        self.set_sequence(initial_frame, final_frame, loop)
        time_ms = int(round(total_duration / float(final_frame - initial_frame + 1)))
        self.frame_duration = time_ms
        self.curr_time = self.frame_duration

    """Sets the time for all frames."""
    def set_total_duration(self, time_ms):
        time_frame = float(time_ms) / self.total_frames
        self.total_duration = time_frame * self.total_frames
        self.frame_duration = time_frame
        self.curr_time = self.frame_duration

    # -----------------------DRAW&UPDATE METHODS--------------------
    """Method responsible for performing the change of frames."""
    def update(self):
        if self.playing:
            self.curr_time -= Animation.deltatime
            if self.curr_time < 0:
                self.curr_frame += 1
                self.curr_time = self.frame_duration
                if self.curr_frame == self.final_frame and self.loop:
                    self.curr_frame = self.initial_frame
                else:
                    if not self.loop and self.curr_frame + 1 >= self.final_frame:
                        self.curr_frame = self.final_frame - 1
                        self.playing = False

    def draw(self, mode=0):
        if self.drawable:
            # Updates the pygame rect based on new positions values
            self.rect.x, self.rect.y = self.x + window.Window.actual_camera.x, self.y + window.Window.actual_camera.y

            # Blits the image with the rect and clip_rect clipped
            window.Window.get_screen().blit(self.image_sequence[self.curr_frame], self.rect, special_flags=mode)

    # ----------------------PLAYING CONTROL METHODS----------------------
    """Stops execution and puts the initial frame as the current frame."""
    def stop(self):
        self.curr_frame = self.initial_frame
        self.playing = False

    """Method responsible for starting the execution of the animation."""
    def play(self):
        self.playing = True

    """Method responsible fo pausing the Animation."""
    def pause(self):
        self.playing = False

    """Returns true if the Animation is being executed."""
    def is_playing(self):
        return self.playing

    """Returns if the Animation is looping."""
    def is_looping(self):
        return self.loop

    """Sets if the Animation will loop or not."""
    def set_loop(self, loop):
        self.loop = loop

    # ----------------GETTER&SETTER METHODS----------------
    """Gets the total duration - sum of all time frames."""
    def get_total_duration(self):
        return self.total_duration

    """Sets the initial frame of the sequence of frames."""
    def set_initial_frame(self, frame):
        self.initial_frame = frame

    """Returns the initial frame of the sequence."""
    def get_initial_frame(self):
        return self.initial_frame

    """Sets the final frame of the sequence of frames."""
    def set_final_frame(self, frame):
        self.final_frame = frame

    """Returns the number of final frame of the sequence."""
    def get_final_frame(self):
        return self.final_frame

    """Sets the current frame that will be drawn."""
    def set_curr_frame(self, frame):
        self.curr_frame = frame

    """Gets the current frame that will be drawn."""
    def get_curr_frame(self):
        return self.curr_frame

    """The animation version of the set_image method."""
    def set_animation(self, image, total_frames):
        if type(image) == str:
            self.image = gameimage.load_image(image)
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.width = self.rect.width/float(total_frames)
        self.height = self.rect.height
        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.final_frame = total_frames
        self.set_sequence(0, self.total_frames, self.loop)
        self.image_sequence = []
        self.curr_time = self.frame_duration
        self.create_image_sequence()

    """Only works if the new image is the same size and has the same number of frames."""
    def set_image(self, image):
        if type(image) == str:
            self.image = gameimage.load_image(image)
        else:
            self.image = image
        self.create_image_sequence()

    def get_image(self):
        return self.image_sequence[self.curr_frame]

    """Flips the animation both horizontally and vertically at will."""
    """The whole sheet is inverted so that the image doesn't need to be flipped in every draw call."""
    def flip_image(self, x=True, y=False):
        if x:
            self.flipped_x = not self.flipped_x

        if y:
            self.flipped_y = not self.flipped_y
        self.flip_image_sequence(x, y)

    def get_image_sequence(self):
        return self.image_sequence
    
