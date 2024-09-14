# !pip install opencv-python

import numpy as np
import cv2

# Simulation parameters
arena_size = 100  # Size of the square arena in cm
outer_area_size = 20  # Width of the outer area near the walls in cm
center_area_size = 60  # Size of the center area in cm
box_size = 5  # Size of the box representing the mouse in cm (5x5 cm)
half_box_size = box_size / 2  # Half of the box size, used for boundary calculations
mean_step_length = 5.56  # Mean step length of C57BL/6J mice in cm
sem_step_length = 0.019  # Standard error of the mean (SEM) of step length in cm
mean_speed = 25.5  # Mean speed of C57BL/6J mice in cm/s
sem_speed = 0.69  # Standard error of the mean (SEM) of speed in cm/s
rate_of_direction_change = 0.7 # probability that the mouse won't move

# Frame size (scaling up the arena for better visualization)
scale_factor = 10  # Scale up the arena to 1000x1000 pixels
frame_size = int(arena_size * scale_factor) # Size of the frame in pixels

# Initialize the position of the mouse at the center of the arena
position = np.array([arena_size/2, arena_size/2])

# Number of steps in the simulation (can be adjusted for longer/shorter simulation)
num_steps = 1_000 # Number of simulation steps (underscore used for readability)

# Initialize video writer to save the simulation as a video file 
# N.B. You have to first create a "videos" folder in the folder where you saved the notebook.
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec
# LP: This fails unless you have a "videos" folder in the same directory as this script. 
# Would recommend having a configurable path for the output video file:
from pathlib import Path
video_folder = Path()
out = cv2.VideoWriter(str(video_folder / 'random_walk_box.avi'), fourcc, 20.0, (frame_size, frame_size)) # Creates a video as an output that is stored in the "videos" folder you just created

# Creation of a dictionary to store various statistics such as movements, distances, speeds, and positions
statistics = {
    "movements": [],
    "distances": [],
    "speeds": [],
    "positions": [],
}

# Function to compute the total time spent in the center and outer areas of the arena
def compute_total_time_in_center_and_outer_area(positions):
    """Computes total time the mouse spends in the center and in the outer parts of the arena""" 
    total_time_in_outer_area, total_time_in_the_center = 0, 0

    # LP: This loop could have been easily vectorized! Can you spot how?
    for position in positions:
        x, y = position
        if x + half_box_size < outer_area_size or x - half_box_size > arena_size - outer_area_size or y + half_box_size < outer_area_size or y - half_box_size > arena_size - outer_area_size:
            total_time_in_outer_area += 1
        else:
            total_time_in_the_center += 1

    return total_time_in_the_center, total_time_in_outer_area

# Function to compute and print various statistics from the simulation
def compute_statistics(statistics):
    """Computes and prints the mean distance, mean speed, the total time spent in the center and in the outer parts of the arena, 
    the total distance and the number of movements of the mouse""" 
    mean_distance = np.mean(statistics["distances"])
    mean_speed = np.mean(statistics["speeds"])

    total_time_in_the_center, total_time_in_outer_area = compute_total_time_in_center_and_outer_area(statistics["positions"])

    total_distance = sum(statistics["distances"])
    num_movements = sum(statistics["movements"])
    
    print("Statistics:")
    print(f"Total distance: {total_distance:.2f} cm")
    print(f"Mean distance: {mean_distance:.2f} cm")
    print(f"Mean speed: {mean_speed:.2f} cm/s")
    print(f"Total time spent in the center area: {total_time_in_the_center} steps")
    print(f"Total time spent in the outer area: {total_time_in_outer_area} steps")
    print(f"Number of movements: {num_movements}")
    print(f"Percentage of time spent in the center area: {total_time_in_the_center / num_steps * 100:.2f}%")
    print(f"Percentage of time spent in the outer area: {total_time_in_outer_area / num_steps * 100:.2f}%")
    print(f"Percentage of movements: {num_movements / num_steps * 100:.2f}%")
    print(f"Percentage of no movements: {(1 - num_movements / num_steps) * 100:.2f}%")
    print(f"Total steps: {len(statistics['positions'])}")

# Simulation loop
for _ in range(num_steps): # Loop over the number of steps in the simulation
    # Create a blank frame
    # frame is a numpy ndarray of shape (frame_size x frame_size x 3) bc 3 are the RGB color channels (and this is why dtype is np.uint8, bc color channel values range from 0 to 255)
    frame = np.zeros((frame_size, frame_size, 3), dtype=np.uint8)

    # Sample the step length and speed from normal distributions based on mean and SEM
    step_length = np.random.normal(mean_step_length, sem_step_length)
    speed = np.random.normal(mean_speed, sem_speed)

    # Calculate the duration of each step based on speed and step length
    step_duration = step_length / speed

    # Randomly determine the direction of movement (angle in radians)
    angle = np.random.uniform(0, 2 * np.pi)

    # number between 0 and 1 sampled from uniform distribution, which tells us if the mouse moves or not at this step
    has_moved = np.random.random()

    # Calculate the potential position variation
    displacement = step_length

    # Check if the mouse moves based on the probability 
    if has_moved < rate_of_direction_change: # no movement
        new_position = position
        statistics["movements"].append(0)
        statistics["distances"].append(0)
        statistics["speeds"].append(0)
    else: # movement
        new_position = position + np.array([displacement * np.cos(angle), displacement * np.sin(angle)])
        statistics["movements"].append(1)
        statistics["distances"].append(displacement)
        statistics["speeds"].append(speed)

    # Check for boundary conditions considering the box size: Ensure the rat stays within the arena
    if new_position[0] - half_box_size < 0 or new_position[0] + half_box_size > arena_size:
        angle = np.pi - angle  # Reflect the angle horizontally
        new_position = position + np.array([displacement * np.cos(angle), displacement * np.sin(angle)])

    if new_position[1] - half_box_size < 0 or new_position[1] + half_box_size > arena_size:
        angle = -angle  # Reflect the angle vertically
        new_position = position + np.array([displacement * np.cos(angle), displacement * np.sin(angle)])

    # Update the position of the mouse
    position = new_position
    statistics["positions"].append(position)

    # Draw the box representing the mouse in the frame
    top_left = (int((position[0] - half_box_size) * scale_factor), int((position[1] - half_box_size) * scale_factor))
    bottom_right = (int((position[0] + half_box_size) * scale_factor), int((position[1] + half_box_size) * scale_factor))
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), -1)  # Draw the box in green

    # Draw the arena border
    cv2.rectangle(frame, (0, 0), (frame_size-1, frame_size-1), (255, 255, 255), 2)

    # LP very small, but to avoid having any kind of hard coding color tuples could have also been variables

    # Write the frame to the video
    out.write(frame)

    # Display the frame (optional)
    # cv2.imshow('Random Walk', frame)
    #imshow(frame)
    #if cv2.waitKey(20) & 0xFF == ord('q'):
    #    break

# Release the video writer and close the display window
out.release()
cv2.destroyAllWindows()

# Compute and print final statistics after the simulation is complete
compute_statistics(statistics)