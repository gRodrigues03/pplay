# Pygame and System Modules
import time
import pygame
from . import gameimage, window

# Initializes pygame's modules
pygame.init()

"""An Animation class for frame-control."""
class Animation(gameimage.GameImage):
    """
    Creates an Animation that is composed by N frames.
    The method set_sequence_time must be called right after.
    Must note that the nnumber of frames will be automatically
    computated: if the image has 100px width and total_frames = 10,
    each frame will have 10px width.
    """
    def __init__(self, image_file, total_frames, loop=True, ease=False):
        # Parent's constructor must be first-called
        gameimage.GameImage.__init__(self, image_file)

        # A Cast to force it to be a float division
        self.width = self.width/float(total_frames)  # The width of each frame

        # Playing Control
        self.playing = True
        self.loop = loop
        self.ease = ease

        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.actual_curr_frame = 0
        self.final_frame = total_frames

        # The duration of each frame
        self.frame_duration = []
        self.total_duration = 0

        # The actual time in ms
        self.last_time = int(round(time.time() * 1000))

        self.set_sequence(0, self.total_frames, self.loop)
        self.set_total_duration(100)

        
    # -----------------------SEQUENCE SETTERS-----------------
    """
    Sets some aspects of the sequence, init/final frame, loop..
    """
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
        if self.ease:
            self.frame_duration = [time_ms * ((i+1)*self.ease) for i in range(0, self.total_frames + 1)]
        else:
            self.frame_duration = [time_ms for _ in range(0, self.total_frames + 1)]

    """Sets the time for all frames."""
    def set_total_duration(self, time_ms):
        time_frame = float(time_ms) / self.total_frames
        self.total_duration = time_frame * self.total_frames
        if self.ease:
            self.frame_duration = [time_frame*((i+1)*self.ease) for i in range(0, self.total_frames + 1)]
        else:
            self.frame_duration = [time_frame for _ in range(0, self.total_frames + 1)]

    # -----------------------DRAW&UPDATE METHODS--------------------
    """Method responsible for performing the change of frames."""
    def update(self):
        if self.playing:
            time_ms = int(round(time.time() * 1000))  # gets the curr time in ms
            if((time_ms - self.last_time > self.frame_duration[self.curr_frame])
               and (self.final_frame != 0)):
                self.curr_frame += 1
                self.last_time = time_ms
            if self.curr_frame == self.final_frame and self.loop:
                self.curr_frame = self.initial_frame
            else:
                if not self.loop and self.curr_frame + 1 >= self.final_frame:
                    self.curr_frame = self.final_frame - 1
                    self.playing = False
            if self.flipped_x:
                self.actual_curr_frame = (self.total_frames - self.curr_frame) - 1
            else:
                self.actual_curr_frame = self.curr_frame
            
    """Draws the current frame on the screen."""
    def draw(self):
        if self.drawable:
            # Clips the frame (rect on the image)
            clip_rect = pygame.Rect(self.actual_curr_frame*self.width, 0, self.width, self.height)

            # Updates the pygame rect based on new positions values
            self.rect.x, self.rect.y = self.x+window.Window.camera.x, self.y+window.Window.camera.y

            # Blits the image with the rect and clip_rect clipped
            window.Window.get_screen().blit(self.image, self.rect, area=clip_rect)
        
    
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
        if self.flipped_x:
            self.actual_curr_frame = (self.total_frames - frame) - 1
        else:
            self.actual_curr_frame = frame

    """Gets the current frame that will be drawn."""
    def get_curr_frame(self):
        return self.curr_frame

    """The animation version of the set_image method."""
    def set_animation(self, image, total_frames):
        if type(image) == str:
            self.image = pygame.transform.flip(gameimage.load_image(image), self.flipped_x, self.flipped_y)
        else:
            self.image = pygame.transform.flip(image, self.flipped_x, self.flipped_y)

        if self.flipped_x:
            self.actual_curr_frame = (self.total_frames - self.curr_frame) - 1
        else:
            self.actual_curr_frame = self.curr_frame

        self.rect = self.image.get_rect()
        self.width = self.rect.width/float(total_frames)
        self.height = self.rect.height
        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.final_frame = total_frames
        self.last_time = int(round(time.time() * 1000))
        self.set_sequence(0, self.total_frames, self.loop)

    """Only works if the new image is the same size and has the same number of frames."""
    def set_image(self, image):
        if type(image) == str:
            self.image = pygame.transform.flip(gameimage.load_image(image), self.flipped_x, self.flipped_y)
        else:
            self.image = pygame.transform.flip(image, self.flipped_x, self.flipped_y)

    """Flips the animation both horizontally and vertically at will."""
    """The whole sheet is inverted so that the image doesn't need to be flipped in every draw call."""
    """self.actual_frame is used so that the frame order stays the same."""
    def flip_image(self, x=True, y=False):
        if x:
            self.flipped_x = not self.flipped_x
        if self.flipped_x:
            self.actual_curr_frame = (self.total_frames - self.curr_frame) - 1
        else:
            self.actual_curr_frame = self.curr_frame

        if y:
            self.flipped_y = not self.flipped_y
        self.image = pygame.transform.flip(self.image, x, y)
    
