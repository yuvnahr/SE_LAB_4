import pygame
from .paddle import Paddle
from .ball import Ball
import time

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.winning_score = 5  # default

        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen):
        self.ball.move(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.score_sound.play()
            self.ball.reset()


        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over(screen)


    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        # Check if someone reached the winning score
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            # Determine winner
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"

            # Display winner
            screen.fill((0, 0, 0))
            title = self.font.render(winner_text, True, (255, 255, 255))
            screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 3))

            # Display replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]

            for i, text in enumerate(options):
                line = self.font.render(text, True, (255, 255, 255))
                screen.blit(line, (self.width // 2 - line.get_width() // 2,
                                self.height // 2 + i * 40))

            pygame.display.flip()

            # Wait for player choice
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_3:
                            self.winning_score = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 7
                            waiting = False

            # Reset game for new match
            self.reset_game()

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
