import pygame
from . import gameimage, window, animation


def file_path(path):
    found_extension = False
    for i in range(len(path) - 1, 0, -1):
        if path[i] == "." and not found_extension:
            extension = ''.join(path[k] for k in range(i, len(path)))
            format_start = i - 1
            break

    number_length = 0
    while '0' < path[format_start] < '9':
        number_length += 1
        format_start -= 1

    path = ''.join(path[k] for k in range(0, format_start))

    print(path, number_length, extension)

    return path, number_length, extension


class ImageSequence(animation.Animation):
    def __init__(self, image_file, total_frames, loop=True):
        gameimage.GameImage.__init__(self)
        # Playing Control
        self.playing = True
        self.loop = loop

        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.final_frame = total_frames

        if type(image_file) == list:
            self.image_sequence = image_file
        else:
            self.create_image_sequence(image_file)

        # The duration of each frame
        self.frame_duration = 0
        self.total_duration = 0

        self.set_sequence(0, self.total_frames, self.loop)
        self.set_total_duration(33.3*total_frames)
        self.curr_time = self.frame_duration

    def create_image_sequence(self, image_file):
        path, number_length, extension = file_path(image_file)
        self.image_sequence = [gameimage.load_image(path + str(i).zfill(number_length) + extension) for i in range(self.total_frames)]
        self.rect = self.image_sequence[0].get_rect()

    def draw(self, mode=0):
        if self.drawable:
            if self.attached_to_camera:
                self.attach.x = self.x + window.Window.actual_camera.x
                self.attach.y = self.y + window.Window.actual_camera.y
                self.rect.x, self.rect.y = self.attach.x, self.attach.y
                window.Window.get_screen().blit(self.image_sequence[self.curr_frame], (self.x, self.y), special_flags=self.blend_mode)
            else:
                self.rect.x, self.rect.y = self.x + window.Window.actual_camera.x, self.y + window.Window.actual_camera.y
                window.Window.get_screen().blit(self.image_sequence[self.curr_frame], self.rect, special_flags=mode)

    def update(self):
        if self.playing:
            self.curr_time -= window.Window.animation_deltatime
            if self.curr_time < 0:
                self.curr_frame += 1
                self.curr_time = self.frame_duration
                if self.curr_frame == self.final_frame and self.loop:
                    self.curr_frame = self.initial_frame
                else:
                    if not self.loop and self.curr_frame + 1 >= self.final_frame:
                        self.curr_frame = self.final_frame - 1
                        self.playing = False

    """Only works if the new image is the same size and has the same number of frames."""

    def set_image(self, image):
        if type(image) == str:
            self.image = gameimage.load_image(image)
        else:
            self.image = image
        self.create_image_sequence()

    """Flips the animation both horizontally and vertically at will."""
    """The whole sheet is inverted so that the image doesn't need to be flipped in every draw call."""

    def flip_image(self, x=True, y=False):
        if x:
            self.flipped_x = not self.flipped_x

        if y:
            self.flipped_y = not self.flipped_y
        self.flip_image_sequence(x, y)
