import tkinter as tk
import numpy as np
from scipy.spatial import ConvexHull
import time

class ChanConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chan's Algorithm Convex Hull")

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

        self.complexity_label = tk.Label(root, text="", pady=10)
        self.complexity_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def compute_convex_hull(self):
        if len(self.points) < 3:
            return

        self.start_time = time.time()  # Record the start time
        
        self.root.after(10, self.compute_convex_hull_after_update)

    def compute_convex_hull_after_update(self):
        convex_hull_points = self.chan_algorithm()
        elapsed_time = time.time() - self.start_time

        self.draw_convex_hull(convex_hull_points, color="red")

        # Calculate time complexity
        n = len(self.points)
        time_complexity = n * np.log(n)  # O(n log n)

        # Calculate space complexity
        space_complexity = n  # O(n) for storing points

        complexity_text = f"Time Complexity: O({time_complexity:.2f} log n) ({elapsed_time:.6f} seconds)\nSpace Complexity: O({space_complexity})"
        self.complexity_label.config(text=complexity_text)

    def chan_algorithm(self):
        
        hull = ConvexHull(self.points)
        hull_points = np.array([self.points[i] for i in hull.vertices])
        return hull_points

    def draw_convex_hull(self, convex_hull_points, color="red"):
        for i in range(len(convex_hull_points)):
            flattened_points = [coord for point in convex_hull_points[:i+1] for coord in point]
            self.canvas.create_polygon(*flattened_points, outline=color, fill="", width=2)
            self.root.update()
            time.sleep(1)

        # Display the final convex hull in a different color
        final_color = "blue"
        final_flattened_points = [coord for point in convex_hull_points for coord in point]
        self.canvas.create_polygon(*final_flattened_points, outline=final_color, fill="", width=2)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ChanConvexHullApp(root)
    root.mainloop()
