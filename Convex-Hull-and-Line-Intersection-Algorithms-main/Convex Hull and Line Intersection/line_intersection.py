import tkinter as tk
import timeit

class LineIntersectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection Checker")

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
            elapsed_time = timeit.timeit(self.check_intersection_logic, number=1)
            if self.check_intersection_logic():
                print("The two line segments intersect.")
                self.canvas.create_text(250, 250, text="Intersect", fill="red", font=("Arial", 16))
            else:
                print("The two line segments do not intersect.")
                self.canvas.create_text(250, 250, text="No Intersection", fill="green", font=("Arial", 16))

            # Display elapsed time
            time_complexity = "O(1)"
            space_complexity = "O(1)"
            complexity_text = f"Time Complexity: {time_complexity} ({elapsed_time:.6f} seconds)\nSpace Complexity: {space_complexity}"
            self.complexity_label.config(text=complexity_text)

    def check_intersection_logic(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        o1 = orientation(self.points[0], self.points[1], self.points[2])
        o2 = orientation(self.points[0], self.points[1], self.points[3])
        o3 = orientation(self.points[2], self.points[3], self.points[0])
        o4 = orientation(self.points[2], self.points[3], self.points[1])

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        if o1 == 0 and self.on_segment(self.points[0], self.points[2], self.points[1]):
            return True
        if o2 == 0 and self.on_segment(self.points[0], self.points[3], self.points[1]):
            return True
        if o3 == 0 and self.on_segment(self.points[2], self.points[0], self.points[3]):
            return True
        if o4 == 0 and self.on_segment(self.points[2], self.points[1], self.points[3]):
            return True

        return False

    def on_segment(self, p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []

if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectApp(root)
    root.mainloop()
