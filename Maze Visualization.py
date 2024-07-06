import tkinter as tk
import socket
import threading

sensor_data = []

def start_server(server_ip='0.0.0.0', port=51973, buffer_size=1024):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, port))
    server_socket.listen(1)
    print("Server is listening on {}:{}".format(server_ip, port))

    while True:
        client_socket, addr = server_socket.accept()
        while True:
            data = client_socket.recv(buffer_size)
            if not data:
                client_socket.close()
                break
            message = data.decode().strip()
            if len(message) == 4 and message.isdigit():
                sensor_data.append([int(digit) for digit in message])

def process_sensor_data(root, app):
    if sensor_data:
        data = sensor_data.pop(0)
        app.update_maze(data)
    root.after(100, process_sensor_data, root, app)  

class MazeApp:
    def _init_(self, root):
        self.root = root
        root.title("Maze Drawing")
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()
        self.robot_x, self.robot_y = 300, 300
        self.orientation = 0
        self.cell_size = 40
        self.draw_robot()

    def draw_robot(self):
        robot_size = 10
        self.canvas.delete("robot")
        self.canvas.create_oval(
            self.robot_x - robot_size, self.robot_y - robot_size,
            self.robot_x + robot_size, self.robot_y + robot_size,
            fill="blue", tags="robot")

    def update_robot_position(self):
        movement = self.cell_size
        if self.orientation == 0:   
            self.robot_y -= movement
        elif self.orientation == 1: 
            self.robot_x += movement
        elif self.orientation == 2: 
            self.robot_y += movement
        elif self.orientation == 3: 
            self.robot_x -= movement

        self.draw_robot()

    def update_maze(self, sensor_data):
        wall_front, wall_right, wall_left, direction = sensor_data

        if direction == 1:
            self.orientation = (self.orientation + 1) % 4
        elif direction == 2:  
            self.orientation = (self.orientation - 1) % 4
        elif direction == 3:  
            self.orientation = (self.orientation + 2) % 4

       
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
            if self.orientation == 0:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)
            elif self.orientation == 1:
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 2:  
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 3:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)

        elif position == 'right':
            if self.orientation == 0:  
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 1:  
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 2:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)
            elif self.orientation == 3:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)

        elif position == 'left':
            if self.orientation == 0:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x - half_wall, y + half_wall)
            elif self.orientation == 1:  
                self.canvas.create_line(x - half_wall, y - half_wall,
                                        x + half_wall, y - half_wall)
            elif self.orientation == 2:  
                self.canvas.create_line(x + half_wall, y - half_wall,
                                        x + half_wall, y + half_wall)
            elif self.orientation == 3:
                self.canvas.create_line(x - half_wall, y + half_wall,
                                        x + half_wall, y + half_wall)


server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

root = tk.Tk()
app = MazeApp(root)
root.after(100, process_sensor_data, root, app) 
root.mainloop()