import pygame
import time
import multiprocessing
import sys

# Function to count and send progress updates
def count_progress(pipe, close_flag):
    for i in range(1001):
        if close_flag.value:  # Check if close flag is set
            break
        pipe.send(i)  # Send progress through the pipe
        time.sleep(0.01)  # Simulate some work

    pipe.send('done')  # Send 'done' signal when counting is finished
    pipe.close()

# Function to create a Pygame window and display the progress bar
def display_progress(pipe, close_flag):
    pygame.init()
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Loading Screen')

    running = True
    font = pygame.font.Font(None, 36)
    progress = 0

    while running:
        screen.fill((0, 0, 0))  # Set background color to black

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                close_flag.value = 1  # Set the close flag when the close button is pressed
                break

        if pipe.poll():  # Check if there's data in the pipe
            data = pipe.recv()  # Receive progress update from the pipe
            if data == 'done':
                running = False
                break

            progress = data

        # Draw the green progress bar at the center
        bar_width = 400
        bar_height = 50
        bar_x = (width - bar_width) // 2
        bar_y = (height - bar_height) // 2

        pygame.draw.rect(screen, (0, 128, 0), (bar_x, bar_y, bar_width * (progress / 1000), bar_height))
        text = font.render(f"Progress: {progress} / 1000", True, (255, 255, 255))
        screen.blit(text, (width // 2 - 100, height // 2 - 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    # Create a Pipe to communicate between processes
    parent_conn, child_conn = multiprocessing.Pipe()
    close_flag = multiprocessing.Value('i', 0)  # Shared value to indicate whether to close the application

    # Create two processes for counting and displaying progress
    count_process = multiprocessing.Process(target=count_progress, args=(child_conn, close_flag))
    display_process = multiprocessing.Process(target=display_progress, args=(parent_conn, close_flag))

    # Start the processes
    count_process.start()
    display_process.start()

    # Wait for the processes to finish
    count_process.join()
    display_process.join()

    # Exit the application when the Pygame GUI is closed
    sys.exit()
