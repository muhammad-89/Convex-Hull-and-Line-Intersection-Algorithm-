import tkinter as tk
import timeit
import time

class LineIntersectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection Checker (Gradient/Slope Method)")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack(pady=20)

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        self.check_button = tk.Button(self.menu_frame, text="Check Intersection", command=self.check_intersection, bg="lightblue", padx=10)
        self.check_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.menu_frame, text="Clear", command=self.clear_canvas, bg="lightcoral", padx=10)
        self.clear_button.pack(side=tk.LEFT)

        self.complexity_label = tk.Label(root, text="", pady=10)
        self.complexity_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="grey")

        # Draw lines if we have enough points
        if len(self.points) == 4:
            self.canvas.create_line(self.points[0], self.points[1], fill="blue")
            self.canvas.create_line(self.points[2], self.points[3], fill="green")

    def check_intersection(self):
        if len(self.points) == 4:
            start_time = timeit.default_timer()
            intersect, operations = self.do_intersect(self.points[0], self.points[1], self.points[2], self.points[3])
            end_time = timeit.default_timer()
            elapsed_time = end_time - start_time

            if intersect:
                print("The two line segments intersect.")
                self.canvas.create_text(250, 250, text="Intersect", fill="red", font=("Arial", 16))
            else:
                print("The two line segments do not intersect.")
                self.canvas.create_text(250, 250, text="No Intersection", fill="green", font=("Arial", 16))

            time_complexity = "O(1)"  # Constant time complexity
            complexity_text = f"Time Complexity: {time_complexity}\nElapsed Time: {elapsed_time:.6f} seconds\nNumber of Operations: {operations}"
            self.complexity_label.config(text=complexity_text)

    def do_intersect(self, point1, point2, point3, point4):
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3
        x4, y4 = point4

        # Calculate slopes (m) and intercepts (b) for each line segment
        slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
        slope2 = (y4 - y3) / (x4 - x3) if x4 != x3 else float('inf')

        operations = 4  # Counter for the number of operations

        # Check if the lines are parallel
        if slope1 == slope2:
            return False, operations
        
        operations += 2  # Two additional operations for the following calculations

        # Calculate intersection point using slope-intercept form (y = mx + b)
        intercept1 = y1 - slope1 * x1 if slope1 != float('inf') else x1
        intercept2 = y3 - slope2 * x3 if slope2 != float('inf') else x3

        operations += 2  # Two additional operations for the intercept calculations

        # Calculate intersection x-coordinate
        intersect_x = (intercept2 - intercept1) / (slope1 - slope2)
        operations += 3  # Three additional operations for the intersect_x calculation

        # Calculate intersection y-coordinate using either line equation
        intersect_y = slope1 * intersect_x + intercept1 if slope1 != float('inf') else slope2 * intersect_x + intercept2
        operations += 2  # Two additional operations for the intersect_y calculation

        # Check if intersection point lies within the line segments' x and y ranges
        if (min(x1, x2) <= intersect_x <= max(x1, x2)) and (min(y1, y2) <= intersect_y <= max(y1, y2)) and \
           (min(x3, x4) <= intersect_x <= max(x3, x4)) and (min(y3, y4) <= intersect_y <= max(y3, y4)):
            operations += 8  # Eight additional operations for the range checks
            return True, operations
        
        operations += 8  # Eight additional operations for the range checks
        return False, operations

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []

if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectApp(root)
    root.mainloop()
