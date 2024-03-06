import tkinter as tk
import time
import math
from functools import cmp_to_key

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
        convex_hull_points = self.graham_scan()
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate time complexity
        time_complexity = len(self.points) * math.log2(len(self.points))  # O(n log n) for sorting

        # Calculate space complexity
        space_complexity = len(self.points)  # O(n) for the stack

        self.time_label.config(text=f"Time Complexity: O({time_complexity:.6f}) ({elapsed_time:.6f} seconds)")
        self.space_label.config(text=f"Space Complexity: O({space_complexity})")

        self.draw_convex_hull(convex_hull_points)

    def graham_scan(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        bottom_point = min(self.points, key=lambda point: (point[1], point[0]))
        self.points.remove(bottom_point)

        def compare(p1, p2):
            angle1 = math.atan2(p1[1] - bottom_point[1], p1[0] - bottom_point[0])
            angle2 = math.atan2(p2[1] - bottom_point[1], p2[0] - bottom_point[0])

            if angle1 < angle2:
               return -1
            elif angle1 > angle2:
               return 1
            else:
                dist1 = (p1[0] - bottom_point[0])**2 + (p1[1] - bottom_point[1])**2
                dist2 = (p2[0] - bottom_point[0])**2 + (p2[1] - bottom_point[1])**2
                return -1 if dist1 < dist2 else 1

        self.points.sort(key=cmp_to_key(compare))

        stack = [bottom_point, self.points[0]]
        for i in range(1, len(self.points)):
            while len(stack) > 1 and orientation(stack[-2], stack[-1], self.points[i]) != 2:
                stack.pop()
            stack.append(self.points[i])

            # Visualize the current line being considered
            self.draw_current_line(stack[-2], stack[-1])
            self.root.update()
            time.sleep(1)

        return stack

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
