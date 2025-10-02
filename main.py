# SIMPLE PROJECT TO STUDY PYTHON AND PYGAME
# SEE "README.md" FOR MORE INFORMATION

import math
import pygame
import sys
import os

# Verify if running in an executable, if not, use relative path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

audio_src = resource_path("endtimes.mp3")

# pygame setup
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Outer Wilds Solar System Simulation")
clock = pygame.time.Clock()

G = 6.67430e-11  # Gravitational constant
DATETIME = 86400  # Seconds in a day
SCALE = 0.4e-9
ZOOM_SCALE = 1e-9

zoomed = False
labed = True

class Body:
    def __init__(self, x, y, vx, vy, mass, color, radius, name):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
        self.radius = radius
        self.name = name
        self.trail = []
        
    def update_position(self, bodies):
        fx = fy = 0
        for other in bodies:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx ** 2 + dy ** 2)
                if r > 0:
                    # F = G * (m1 * m2) / r^2
                    f = G * self.mass * other.mass / (r ** 2)
                    fx += f * (dx / r)
                    fy += f * (dy / r)
        
        #F = ma -> a = F / m
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DATETIME
        self.vy += ay * DATETIME
        self.x += self.vx * DATETIME
        self.y += self.vy * DATETIME
        
        current_scale = ZOOM_SCALE if zoomed else SCALE
        
        self.trail.append((int(self.x * current_scale + WIDTH // 2), int(self.y * current_scale + HEIGHT // 2)))
        if len(self.trail) > 200:
            self.trail.pop(0)
        
    def draw_text(text, font, text_color, x, y):
        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (x, y))


    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)

        current_scale = ZOOM_SCALE if zoomed else SCALE

        screen_x = float(self.x * current_scale + WIDTH // 2)
        screen_y = float(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

        # Draw the name of the planet
        font = pygame.font.SysFont("Arial", 15) if zoomed else pygame.font.SysFont("Arial", 10)
        text_surface = font.render(self.name, True, (255, 255, 255)) if labed else font.render("", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_x, screen_y + self.radius + 12))
        screen.blit(text_surface, text_rect)

def draw_timer(screen, time):
    font = pygame.font.SysFont("Arial", 24)
    minutes = time // 60
    seconds = time % 60
    timer_text = f"Time: {minutes:02d}:{seconds:02d}"
    text_surface = font.render(timer_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


bodies = [
    Body(0,0,0,0, 1.989e30, (255,255,0), 15, "Sun"),
    
    Body(5.79e10, 1e9, -2e3, 4.74e4, 4.302e23, (255,75,8), 5, "Ash Twin"),
    
    Body(5.81e10, -1e9, 2e3, 4.74e4, 4.302e23, (250,75,8), 5, "Ember Twin"),

    Body(1.5e11,0,0,2.98e4,5.972e24,(0,150,0),7, "Timber Hearth"),
    
    Body(2.28e11,0,0,2.41e4,6.39e23,(25,0,150),8, "Brittle Hollow"),
    
    Body(3.78e11,0,0,1.91e4,7.898e23,(0,200,100),11, "Giant’s Deep"),
    
    Body(4.43e11,0,0,1.81e4,8.683e23,(85,68,50),10, "Dark Bramble"),
    
    Body(5.50e11,0,0,3.48e3,4.024e23,(50,100,255),6, "Interloper"),
]

change_time = 0
running = True
while running:
    time = int(pygame.time.get_ticks() / 1000) + change_time # Get time in seconds

    #Sun stages
    if (time >= 254) and (time <= 527):
        bodies[0].color = (255,205,0)
        bodies[0].radius = 15.5
    if (time >= 528) and (time <= 781):
        bodies[0].color = (255,155,0)
        bodies[0].radius = 16
    if (time >= 782) and (time <= 1035):
        bodies[0].color = (255,105,0)
        bodies[0].radius = 16.5
    if (time >= 1036) and (time <= 1199):
        bodies[0].color = (255,55,0)
        bodies[0].radius = 17
    if (time >= 1200) and (time <= 1289):
        bodies[0].color = (255,20,0)
        bodies[0].radius = 17.5

    # Time ends
    if time == 1203:
        pygame.mixer.music.load(audio_src)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
    if time == 1290:
        radius = 1
        bodies = [Body(0, 0, 0, 0, 1.989e31, (0,200,255), radius, "Supernova")]
    if time >= 1291:
        bodies[0].radius += 0.33
    if time >= 1320:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Keybinds
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_time += 30
                if time >= 1190:
                    change_time = 1190

            if event.key == pygame.K_DOWN:
                change_time -= 30
                if time <= 30:
                    change_time = 0
                if time >= 1190:
                    change_time = 1190

            if event.key == pygame.K_z:
                zoomed = not zoomed
                
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_x:
                labed = not labed
                
            for body in bodies:
                body.trail = []  # Clear trails on zoom toggle

    screen.fill((0, 0, 0))  # Clear screen

    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    draw_timer(screen, time)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit to 60 FPS
        
pygame.quit()  # Clean up and close the window
