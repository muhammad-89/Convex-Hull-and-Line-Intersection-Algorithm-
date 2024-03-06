import tkinter as tk
import time

class QuickHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Hull App")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        self.quick_hull_button = tk.Button(self.menu_frame, text="Compute Quick Hull", command=self.compute_quick_hull)
        self.quick_hull_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.menu_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.time_label = tk.Label(root, text="Time Complexity: ")
        self.time_label.pack()

        self.space_label = tk.Label(root, text="Space Complexity: ")
        self.space_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append([x, y])
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def compute_quick_hull(self):
        if len(self.points) < 3:
            return

        start_time = time.time()
        self.hull = set()
        min_point, max_point = self.find_min_max_points(self.points)
        self.quick_hull_recursive(self.points, min_point, max_point, 1)
        self.quick_hull_recursive(self.points, min_point, max_point, -1)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate time complexity
        time_complexity = len(self.points) * len(self.points)  # O(n^2) in the worst case

        # Calculate space complexity
        space_complexity = len(self.points)  # O(n) for the convex hull list

        self.time_label.config(text=f"Time Complexity: O({time_complexity}) ({elapsed_time:.6f} seconds)")
        self.space_label.config(text=f"Space Complexity: O({space_complexity})")

        # Draw the final convex hull
        self.draw_convex_hull(self.hull, final=True)

    def find_side(self, p1, p2, p):
        val = (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])
        if val > 0:
            return 1
        if val < 0:
            return -1
        return 0

    def line_dist(self, p1, p2, p):
        return abs((p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0]))

    def draw_line(self, p1, p2, color="black", label=None):
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2, tags=label)

    def draw_point(self, p, color="black", label=None):
        self.canvas.create_oval(p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3, fill=color, tags=label)

    def find_min_max_points(self, point_set):
        min_x = 0
        max_x = 0
        for i in range(1, len(point_set)):
            if point_set[i][0] < point_set[min_x][0]:
                min_x = i
            if point_set[i][0] > point_set[max_x][0]:
                max_x = i
        return point_set[min_x], point_set[max_x]

    def quick_hull_recursive(self, point_set, p1, p2, side):
        max_dist = 0
        ind = -1

        for i in range(len(point_set)):
            temp = self.line_dist(p1, p2, point_set[i])
            if (self.find_side(p1, p2, point_set[i]) == side) and (temp > max_dist):
                ind = i
                max_dist = temp

        if ind == -1:
            self.draw_line(p1, p2, color="black", label="final_hull")
            return

        # Draw the current line being considered
        self.draw_line(p1, p2, color="blue", label="steps")
        self.root.update()
        time.sleep(1)

        # Draw the line connecting the current point to the two end points of the current line
        self.draw_line(point_set[ind], p1, color="red", label="steps")
        self.draw_line(point_set[ind], p2, color="red", label="steps")
        self.root.update()
        time.sleep(1)

        # Recur for the two parts divided by point_set[ind]
        self.quick_hull_recursive(point_set, point_set[ind], p1, -self.find_side(point_set[ind], p1, p2))
        self.quick_hull_recursive(point_set, point_set[ind], p2, -self.find_side(point_set[ind], p2, p1))

    def draw_convex_hull(self, convex_hull_points, final=False):
        if not convex_hull_points:
            return

        hull_points = [list(map(int, point.split("$"))) for point in convex_hull_points]
        if final:
            self.canvas.create_polygon(hull_points, outline="red", fill="", width=2, tags="final_hull")
        else:
            self.canvas.create_polygon(hull_points, outline="blue", fill="", width=2, tags="steps")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.hull = set()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickHullApp(root)
    root.mainloop()
