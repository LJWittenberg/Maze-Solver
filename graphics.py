from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk() # This creates the main window for our application
        self.__root.title("Maze solver") # This sets the name of the window to "My Window"
        self.__canvas = Canvas(self.__root, bg="white",width=width, height=height) # Creates a canvas within the root window with specified width and height
        self.__canvas.pack(fill=BOTH, expand=1)  # This line ensures the canvas fills the window
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.running = False # Initializes the running state of the window

    def redraw(self):
        self.__root.update_idletasks() 
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()
        print("Window closed.")

    def close(self):
        self.__running = False

    def Draw_line(self, line, color="blue"):
        line.Draw(self.__canvas, color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2

    def Draw(self, canvas, color):
        canvas.create_line(self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y, fill=color, width=2)