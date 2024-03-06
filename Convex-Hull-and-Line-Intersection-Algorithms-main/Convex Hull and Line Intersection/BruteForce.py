import tkinter as tk
import time

# Global variables
points = []

def whichSideOfLine(ptI, ptJ, ptK):
    # Function to determine which side of the line point ptK lies
    # Returns > 0 if ptK is on the left side, < 0 if on the right side, 0 if on the line
    return ((ptJ[1] - ptI[1]) * (ptK[0] - ptI[0])) - ((ptJ[0] - ptI[0]) * (ptK[1] - ptI[1]))

def drawLineSegment(canvas, ptA, ptB):
    # Function to draw a line segment between two points on the canvas
    canvas.create_line(ptA[0], ptA[1], ptB[0], ptB[1])

def computeConvexHull():
    global points

    start_time = time.time()

    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue

            ptI = points[i]
            ptJ = points[j]

            allPointsOnTheRight = True
            for k in range(len(points)):
                if k == i or k == j:
                    continue

                d = whichSideOfLine(ptI, ptJ, points[k])
                if d < 0:
                    allPointsOnTheRight = False
                    break

            if allPointsOnTheRight:
                drawLineSegment(canvas, ptI, ptJ)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate time complexity
    time_complexity = len(points) * len(points) * len(points)  # O(n^3) in the worst case

    # Calculate space complexity
    space_complexity = 1  # O(1) for global variables

    complexity_text.set(f"Time Complexity: O({time_complexity}) ({elapsed_time:.6f} seconds)\nSpace Complexity: O({space_complexity})")

def onClick(event):
    x, y = event.x, event.y
    points.append((x, y))
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")  # Display clicked points

# Create tkinter window
root = tk.Tk()
root.title("Convex Hull Brute Force Algorithm")

# Create canvas for drawing
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Bind click event to canvas
canvas.bind("<Button-1>", onClick)

# Create a button to compute convex hull
compute_button = tk.Button(root, text="Compute Convex Hull (Brute Force)", command=computeConvexHull)
compute_button.pack()

# Label to display time and space complexity
complexity_text = tk.StringVar()
complexity_label = tk.Label(root, textvariable=complexity_text, justify="left")
complexity_label.pack()

# Run the tkinter main loop
root.mainloop()
