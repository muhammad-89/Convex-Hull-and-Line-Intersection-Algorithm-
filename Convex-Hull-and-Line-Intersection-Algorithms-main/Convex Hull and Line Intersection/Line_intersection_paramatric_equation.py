import tkinter as tk
import timeit

# Global variables to store points and canvas
points = []
canvas = None

# Function to handle mouse clicks to add points
def on_click(event):
    global points, canvas
    x, y = event.x, event.y
    points.append((x, y))
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='black')

    # Check for line intersection when more than 2 points are present
    if len(points) >= 4:
        start_time = timeit.default_timer()
        intersect, intersection_point = check_intersection(points[-2], points[-1], points[-3], points[-4])
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time

        if intersect:
            canvas.create_text(50, 20, text="Lines intersect!", fill='red')
            canvas.create_oval(intersection_point[0] - 2, intersection_point[1] - 2,
                               intersection_point[0] + 2, intersection_point[1] + 2, fill='red')
            canvas.create_line(points[-2][0], points[-2][1], points[-1][0], points[-1][1], fill='red')
            canvas.create_line(points[-3][0], points[-3][1], points[-4][0], points[-4][1], fill='red')
        else:
            canvas.create_text(50, 20, text="No intersection", fill='green')
            canvas.create_line(points[-2][0], points[-2][1], points[-1][0], points[-1][1])
            canvas.create_line(points[-3][0], points[-3][1], points[-4][0], points[-4][1])

        # Display elapsed time and time complexity
        time_complexity = "O(1)"  # Assuming constant time complexity
        complexity_text = f"Elapsed Time: {elapsed_time:.6f} seconds\nTime Complexity: {time_complexity}"

        # Create or update the label to display the information
        display_label = canvas.create_text(300, 20, text=complexity_text, anchor='w', fill='black')
        canvas.itemconfig(display_label, text=complexity_text)

# Function to check for line intersection using parametric equations
def check_intersection(p1, q1, p2, q2):
    x1, y1 = p1
    x2, y2 = q1
    x3, y3 = p2
    x4, y4 = q2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return False, None  # Lines are parallel or coincident

    t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = t_num / den

    u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
    u = u_num / den

    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection_point = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return True, intersection_point

    return False, None

# Create the main window
root = tk.Tk()
root.title("Line Intersection - Parametric Equations")

# Create canvas
canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.pack()

# Bind mouse click to canvas
canvas.bind("<Button-1>", on_click)

# Start the main loop
root.mainloop()
