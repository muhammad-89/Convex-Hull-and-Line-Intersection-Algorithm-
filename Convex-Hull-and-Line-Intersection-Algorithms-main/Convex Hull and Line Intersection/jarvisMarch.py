import tkinter as tk
import time
import math

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull App")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        self.convex_hull_button = tk.Button(self.menu_frame, text="Compute Convex Hull", command=self.compute_convex_hull)
        self.convex_hull_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.menu_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.time_label = tk.Label(root, text="Time Complexity: ")
        self.time_label.pack()

        self.space_label = tk.Label(root, text="Space Complexity: ")
        self.space_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def compute_convex_hull(self):
        if len(self.points) < 3:
            return

        start_time = time.time()
        convex_hull_points = self.jarvis_march()
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate time complexity
        time_complexity = len(self.points) * len(self.points)  # O(n^2) in the worst case

        # Calculate space complexity
        space_complexity = len(self.points)  # O(n) for the convex hull list

        self.time_label.config(text=f"Time Complexity: O({time_complexity}) ({elapsed_time:.6f} seconds)")
        self.space_label.config(text=f"Space Complexity: O({space_complexity})")

        self.draw_convex_hull(convex_hull_points)

    def jarvis_march(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        def angle_between(p1, p2):
            return -1 * (180 + (180 / 3.1415926535) * (180 / 3.1415926535) * (180 / 3.1415926535) * (180 / 3.1415926535) * (180 / 3.1415926535) * math.atan2(p2[1] - current_point[1], p2[0] - current_point[0]) / 3.1415926535)

        bottom_point = max(self.points, key=lambda point: (point[1], point[0]))
        current_point = bottom_point
        convex_hull = []

        while True:
            convex_hull.append(current_point)
            endpoint = self.points[0]

            for next_point in self.points[1:]:
                if endpoint == current_point or orientation(current_point, endpoint, next_point) == 2:
                    endpoint = next_point

            current_point = endpoint

            # Visualize the current line being considered
            self.draw_current_line(convex_hull[-1], current_point)
            self.root.update()
            time.sleep(1)

            if current_point == bottom_point:
                break

        return convex_hull

    def draw_convex_hull(self, convex_hull_points):
        self.canvas.create_polygon(convex_hull_points, outline="red", fill="", width=2)

    def draw_current_line(self, p1, p2):
        self.canvas.create_line(p1, p2, fill="blue")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()
