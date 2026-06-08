import pygame
import random
import math


class ParticleEntity:
    def __init__(self, owner, type: str):
        self.x = owner.x
        self.y = owner.y
        self.type = type

        if self.type == "explosion":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.lifetime = random.randint(30, 50)
            self.max_lifetime = self.lifetime
            self.size = random.uniform(6, 12)
            self.color = random.choice([
                (255, 60, 20),   # red-orange
                (255, 120, 0),   # orange
                (255, 200, 0),   # yellow
                (255, 40, 0),    # deep red
            ])

        elif self.type == "smoke":
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-1.5, -0.6)  # rises upward
            self.lifetime = random.randint(60, 90)
            self.max_lifetime = self.lifetime
            self.size = random.uniform(8, 14)
            self.color = random.choice([
                (80, 80, 80),
                (100, 100, 100),
                (60, 60, 60),
            ])

        self.alive = True

    def update(self):
        if not self.alive:
            return

        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

        if self.type == "explosion":
            # Slow down over time (drag)
            self.vx *= 0.92
            self.vy *= 0.92
            self.size = max(0, self.size - 0.25)

        elif self.type == "smoke":
            # Slight horizontal drift over time
            self.vx += random.uniform(-0.05, 0.05)
            self.size = max(0, self.size - 0.08)

        if self.lifetime <= 0 or self.size <= 0:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        if not self.alive or self.size <= 0:
            return

        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))
        size_int = max(1, int(self.size))

        # Draw on a temp surface to support alpha
        temp = pygame.Surface((size_int * 2, size_int * 2), pygame.SRCALPHA)
        r, g, b = self.color
        pygame.draw.circle(temp, (r, g, b, alpha), (size_int, size_int), size_int)
        surface.blit(temp, (int(self.x) - size_int, int(self.y) - size_int))


def explode(owner):
    for i in range(17):  # explosion
        world.particles.append(ParticleEntity(owner, "explosion"))
    for i in range(14):  # smoke
        world.particles.append(ParticleEntity(owner, "smoke"))
