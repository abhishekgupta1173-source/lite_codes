import pygame
import numpy as np
import random

# Configuration

WIDTH = 800
HEIGHT = 800

BOWL_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
BOWL_RADIUS = 300

# Start with 1 ball, then 2. Many at once is the bonus.
NUM_PARTICLES = 100

PARTICLE_RADIUS = 12
PARTICLE_SPEED = 150.0

# Pixels per second squared, not m/s^2. Note that +y points DOWN on screen.
GRAVITY = 900.0

# How much speed survives a bounce. 1.0 loses nothing, below 1.0 is weaker.
WALL_RESTITUTION = 1.0
RESTITUTION = 1.0

FPS = 60

positions = []
velocities = []

for i in range(NUM_PARTICLES):

    # A random spot inside the bowl, with the whole ball fitting.
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0, BOWL_RADIUS - PARTICLE_RADIUS)

    positions.append(BOWL_CENTER + distance * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

    # A random direction, at roughly PARTICLE_SPEED.
    # Swap for np.array([0.0, 0.0]) to drop the ball from rest.
    angle = random.uniform(0, 2 * np.pi)

    velocities.append(PARTICLE_SPEED * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

# Pygame setup

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

clock = pygame.time.Clock()

running = True

# Main loop

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Seconds since the last frame. This is your timestep.
    dt = clock.tick(FPS) / 1000.0

    ###########################################################################
    # TODO: Make every ball fall, and bounce it off the wall of the bowl.     #
    #                                                                         #
    # Two things happen here, in an order that matters.                       #
    #                                                                         #
    # First, it falls. Gravity is an acceleration, so ask yourself what it    #
    # changes directly: the position, or the velocity? And once that has      #
    # changed, what does the ball's new position depend on?                   #
    #                                                                         #
    # Second, it has to stay in the bowl. Work out how you would even         #
    # tell that it has escaped, given that you know where the centre of       #
    # the bowl is, how wide the bowl is, and how wide the ball is.            #
    # Careful: the ball is drawn with a radius of its own, so its edge        #
    # reaches the wall before its centre would.                               #
    #                                                                         #
    # Once you know it has escaped, two things need fixing. Where should      #
    # the ball actually be, and what should its velocity become? For the      #
    # velocity, only the part heading into the wall should change. The        #
    # part sliding along the wall carries on untouched. WALL_RESTITUTION      #
    # decides how much of the incoming speed comes back out.                  #
    ###########################################################################
    
    # CODE STARTS HERE.
    # The Physics behind the simulation is newtons laws of motion which we will be simulating.
    for i in range(len(positions)):
        # Apply gravity to the velocity (y-axis only) ( [1] shows y component)
        velocities[i][1] = velocities[i][1] + GRAVITY * dt
        # Updating position using new velocity , Newtons equations 
        positions[i] = positions[i] + velocities[i] * dt

         #velocities[i][1] = velocities[i][1] + GRAVITY * dt  # writing velocity after position increses the speed of the ball as time passes 

        # Checkfor wall collision
        offset = positions[i] - BOWL_CENTER
        distance = np.linalg.norm(offset)

        # The maximum allowed distance 
        max_distance = BOWL_RADIUS - PARTICLE_RADIUS

        if distance > max_distance:
            
            normal_outward_direction = offset / distance
            positions[i] = BOWL_CENTER + normal_outward_direction * max_distance
            normal_inward_direction = -normal_outward_direction #This might not needed but i used to track the vector direction

            # Reflect the velocity (as told in Readme file)
            new_velocity = np.dot(velocities[i], normal_inward_direction)
            velocities[i] = velocities[i] - (1 + WALL_RESTITUTION) * new_velocity* normal_inward_direction

    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    ###########################################################################
    # TODO: Make the balls bounce off each other.                             #
    #                                                                         #
    # Start with the condition. Given two balls, what has to be true          #
    # about where they are for them to be touching? Every ball has the        #
    # same radius, which makes this simpler than it sounds.                   #
    #                                                                         #
    # Then the response. A collision changes velocities, not positions.       #
    # Which direction does the change act along, and how would you get        #
    # that direction from the two positions you have? Only the motion         #
    # along that direction matters, the rest is unaffected.                   #
    #                                                                         #
    # One trap worth thinking about: two balls that are overlapping but       #
    # already moving apart should be left alone. If you bounce them again     #
    # they will get stuck together. How would you tell "approaching"          #
    # from "separating"?                                                      #
    #                                                                         #
    # Finally, this has to happen for every pair of balls, not just one.      #
    ###########################################################################

    # CODE STARTS HERE.
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            # finding normal vector between the balls
            normal = positions[i] - positions[j]
            distance = np.linalg.norm(normal)
            normal_direction = normal / distance

            # Finding relative velocity between balls
            relative_velocity = velocities[i] - velocities[j]
            velocity_along_normal = np.dot(relative_velocity , normal_direction)

            # The component if velocity that do not change ( its perpendicular to the line joining the two balls)
            tangent_direction = np.array([-normal_direction[1] , normal_direction[0]])

            if distance <= 2 * PARTICLE_RADIUS and velocity_along_normal < 0:
             #print("Collision detected")  #This can be used to detect that is the 'if' statmenet is working and colllision occuring or not 
                # writing final velocities after collision for each ball -- final velocity in x and in y 

                velocities [i] = ( (((RESTITUTION - 1) * np.dot(velocities[i] ,normal_direction) * normal_direction + (1+RESTITUTION) * np.dot(velocities[j] , normal_direction) * normal_direction)/2) + np.dot(velocities[i] , tangent_direction) * tangent_direction )
                velocities[j] = ( (((RESTITUTION - 1) * np.dot(velocities[j] , normal_direction) * normal_direction + (1+RESTITUTION) * np.dot(velocities[i] , normal_direction) * normal_direction) / 2) + np.dot(velocities[j] , tangent_direction) * tangent_direction )

    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    # Render

    screen.fill((20, 20, 25))

    pygame.draw.circle(
        screen,
        (180, 180, 180),
        BOWL_CENTER.astype(int),
        BOWL_RADIUS,
        width=3
    )

    for position in positions:
        pygame.draw.circle(
            screen,
            (220, 220, 220),
            position.astype(int),
            PARTICLE_RADIUS
        )

    pygame.display.flip()

pygame.quit()
