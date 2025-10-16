import pygame
import random

# Initialize mixer for sound (before anything else)
pygame.mixer.init()

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # 🎵 Load MP3 sound effects
        self.hit_sound = pygame.mixer.Sound("bounce-8111.mp3")
        self.wall_sound = pygame.mixer.Sound("bounce-8111.mp3")
        self.score_sound = pygame.mixer.Sound("bounce-8111.mp3")

    def move(self, player, ai):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall bounce
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_sound.play()

        # Paddle collision detection
        if self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            self.hit_sound.play()

        elif self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            self.hit_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
