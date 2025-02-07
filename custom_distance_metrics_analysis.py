import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, messagebox
from tkinter import ttk

# Define distance functions with step-by-step calculation breakdowns
def euclidean_distance(point1, point2):
    diff = point1 - point2
    squared_diff = diff ** 2
    sum_squared_diff = np.sum(squared_diff)
    return np.sqrt(sum_squared_diff), diff, squared_diff, sum_squared_diff

def manhattan_distance(point1, point2):
    abs_diff = np.abs(point1 - point2)
    sum_abs_diff = np.sum(abs_diff)
    return sum_abs_diff, abs_diff

def chebyshev_distance(point1, point2):
    abs_diff = np.abs(point1 - point2)
    max_abs_diff = np.max(abs_diff)
    return max_abs_diff, abs_diff

# Function to load dataset
def load_dataset(file_path):
    return pd.read_csv(file_path)

# Class for the Tkinter GUI application
class DistanceCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distance Calculator")

        # Variable declarations
        self.file_path = StringVar()
        self.row1 = StringVar()
        self.row2 = StringVar()
        self.data = None

        # GUI layout
        Label(root, text="Step 1: Load Dataset").grid(row=0, column=0, padx=10, pady=10)
        Button(root, text="Browse CSV", command=self.load_file).grid(row=0, column=1, padx=10, pady=10)

        Label(root, text="Step 2: Select Row 1").grid(row=1, column=0, padx=10, pady=10)
        Entry(root, textvariable=self.row1).grid(row=1, column=1, padx=10, pady=10)

        Label(root, text="Step 3: Select Row 2").grid(row=2, column=0, padx=10, pady=10)
        Entry(root, textvariable=self.row2).grid(row=2, column=1, padx=10, pady=10)

        Button(root, text="Calculate Distances", command=self.calculate_distances).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_text = Label(root, text="")
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Add separate buttons for visualizing each distance metric
        Button(root, text="Visualize Euclidean", command=lambda: self.visualize_data("euclidean")).grid(row=5, column=0, padx=10, pady=10)
        Button(root, text="Visualize Manhattan", command=lambda: self.visualize_data("manhattan")).grid(row=5, column=1, padx=10, pady=10)
        Button(root, text="Visualize Chebyshev", command=lambda: self.visualize_data("chebyshev")).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Load the dataset using a file dialog
    def load_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            self.file_path.set(file_path)
            self.data = load_dataset(file_path)
            messagebox.showinfo("Success", "Dataset loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")

    # Calculate distances between selected rows with steps
    def calculate_distances(self):
        try:
            row1 = int(self.row1.get())
            row2 = int(self.row2.get())
            point1 = self.data.iloc[row1, :-1].values
            point2 = self.data.iloc[row2, :-1].values

            # Calculate Euclidean distance with steps
            euclidean_dist, diff, squared_diff, sum_squared_diff = euclidean_distance(point1, point2)
            euclidean_steps = (f"Euclidean Distance Calculation:\n"
                               f"1. Difference (point1 - point2): {diff}\n"
                               f"2. Squared differences: {squared_diff}\n"
                               f"3. Sum of squared differences: {sum_squared_diff}\n"
                               f"4. Square root of sum: {euclidean_dist}\n")

            # Calculate Manhattan distance with steps
            manhattan_dist, abs_diff_manhattan = manhattan_distance(point1, point2)
            manhattan_steps = (f"Manhattan Distance Calculation:\n"
                               f"1. Absolute differences: {abs_diff_manhattan}\n"
                               f"2. Sum of absolute differences: {manhattan_dist}\n")

            # Calculate Chebyshev distance with steps
            chebyshev_dist, abs_diff_chebyshev = chebyshev_distance(point1, point2)
            chebyshev_steps = (f"Chebyshev Distance Calculation:\n"
                               f"1. Absolute differences: {abs_diff_chebyshev}\n"
                               f"2. Maximum absolute difference: {chebyshev_dist}\n")

            result = (f"{euclidean_steps}\n"
                      f"{manhattan_steps}\n"
                      f"{chebyshev_steps}")

            self.result_text.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating distances: {e}")

    # Visualize data with lines connecting selected points
    def visualize_data(self, distance_type):
        try:
            if self.data is None:
                messagebox.showerror("Error", "Load a dataset first.")
                return

            row1 = int(self.row1.get())
            row2 = int(self.row2.get())
            point1 = self.data.iloc[row1, :-1].values
            point2 = self.data.iloc[row2, :-1].values

            if point1.shape[0] == 2:
                plt.figure(figsize=(10, 6))
                plt.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1], label='Data Points')
                plt.scatter(point1[0], point1[1], color='red', s=100, label='Point 1')
                plt.scatter(point2[0], point2[1], color='blue', s=100, label='Point 2')

                # Draw line between points based on the distance type
                if distance_type == "euclidean":
                    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], 'g-', label='Euclidean Distance')
                elif distance_type == "manhattan":
                    plt.plot([point1[0], point1[0]], [point1[1], point2[1]], 'y--', label='Manhattan Distance')
                    plt.plot([point1[0], point2[0]], [point2[1], point2[1]], 'y--')
                elif distance_type == "chebyshev":
                    plt.plot([point1[0], point2[0]], [point1[1], point1[1]], 'm--', label='Chebyshev Distance')
                    plt.plot([point2[0], point2[0]], [point1[1], point2[1]], 'm--')

                plt.title(f'Dataset Visualization ({distance_type.capitalize()} Distance)')
                plt.xlabel(self.data.columns[0])
                plt.ylabel(self.data.columns[1])
                plt.legend()
                plt.grid()
                plt.show()
            else:
                messagebox.showinfo("Info", "Visualization is only available for 2D datasets.")
        except Exception as e:
            messagebox.showerror("Error", f"Error in visualization: {e}")

# Initialize and run the application
if __name__ == "__main__":
    root = Tk()
    app = DistanceCalculatorApp(root)
    root.mainloop()
