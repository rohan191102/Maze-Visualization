import tkinter as tk

class MazeApp:
    def __init__(self, root):
        self.root = root
        root.title("Maze Drawing")

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.robot_x, self.robot_y = 300, 300  # Robot's starting position
        self.orientation = 0  # 0: Up, 1: Right, 2: Down, 3: Left
        self.cell_size = 35  # Size of each cell in the maze (35x35)

        self.draw_robot()

    def draw_robot(self):
        robot_size = 10
        self.canvas.delete("robot")
        self.canvas.create_oval(self.robot_x - robot_size, self.robot_y - robot_size,
                                self.robot_x + robot_size, self.robot_y + robot_size,
                                fill="blue", tags="robot")

    def update_robot_position(self):
        movement = self.cell_size
        if self.orientation == 0:   # Up
            self.robot_y -= movement
        elif self.orientation == 1: # Right
            self.robot_x += movement
        elif self.orientation == 2: # Down
            self.robot_y += movement
        elif self.orientation == 3: # Left
            self.robot_x -= movement

        self.draw_robot()

    def update_maze(self, sensor_data):
        wall_front, wall_right, wall_left, direction = sensor_data

        # Update the robot's orientation based on the direction instruction
        if direction == 1:  # Right turn
            self.orientation = (self.orientation + 1) % 4
        elif direction == 2:  # Left turn
            self.orientation = (self.orientation - 1) % 4
        elif direction == 3:  # Backward
            self.orientation = (self.orientation + 2) % 4

        # Then move the robot forward and draw walls if it's not a backward instruction
        if direction != 3:  
            self.update_robot_position()
            if wall_front:
                self.draw_wall('front')
            if wall_right:
                self.draw_wall('right')
            if wall_left:
                self.draw_wall('left')

        self.draw_robot()

    def draw_wall(self, position):
        wall_length = self.cell_size
        half_wall = wall_length // 2
        x, y = self.robot_x, self.robot_y

        if position == 'front':
            if self.orientation == 0:  # Up
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)
            elif self.orientation == 1:  # Right
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 2:  # Down
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 3:  # Left
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)

        elif position == 'right':
            if self.orientation == 0:  # Up
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 1:  # Right
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 2:  # Down
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)
            elif self.orientation == 3:  # Left
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)

        elif position == 'left':
            if self.orientation == 0:  # Up
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)
            elif self.orientation == 1:  # Right
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)
            elif self.orientation == 2:  # Down
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 3:  # Left
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)

root = tk.Tk()
app = MazeApp(root)

# Example sensor data
sensor_data = [
    # Starting at the bottom of the uploaded image, facing up
    [0, 0, 1, 0], 
    [0, 1, 1, 0], 
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 1, 0, 3],
    [0, 1, 0, 0], # Walls do not matter here 
    [1, 1, 0, 2],
    [1, 0, 1, 2],
    [0, 1, 1, 1],
    [0, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 0, 1, 2],
    [1, 1, 1, 1],
    [1, 1, 1, 3], # Walls do not matter here
    [1, 1, 0, 0],
    [1, 0, 1, 2],
    [1, 1, 0, 1],
    [1, 0, 0, 2],
    [0, 0, 1, 1]
]

for data in sensor_data:
    app.update_maze(data)
    root.update()
    root.after(500)  # Delay for visualization

root.mainloop()