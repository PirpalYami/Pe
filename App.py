import tkinter as tk
from tkinter import ttk
import pandas as pd
import ttkbootstrap as tb
import csv
import os
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


class mainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Project")

        frame = tk.Frame(self.root)
        frame.pack()

        box = tk.LabelFrame(frame)
        box.grid(row=0, column=0, padx=20, pady=10)

        tk.Label(box, text="Lesson:").grid(row=0, column=0, padx=10, pady=10)
        self.lesson_entry = ttk.Combobox(box, width=10, values=["Math", "English","Science","Biology","Physics","Sosiology","Geography","History"])
        self.lesson_entry.grid(row=0, column=1)

        tk.Label(box, text="Score:").grid(row=1, column=0, padx=10, pady=10)
        self.score_entry = tk.Spinbox(box, from_=0, to=100)
        self.score_entry.grid(row=1, column=1)

        save_button = tk.Button(box, text="Save", command=self.save_to_csv)
        save_button.grid(row=2, column=0, padx=10, pady=10)

        self.tree = ttk.Treeview(box, columns=("Lesson", "Score"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col)
        self.tree.grid(row=3, column=0, columnspan=2)

        for widget in box.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        self.load_csv()
        self.embed_graph()  # Automatically embed the graph on startup

    def load_csv(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            if os.path.exists('data.csv'):
                with open('data.csv', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.tree.insert("", tk.END, values=(row["Lesson"], row["Score"]))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV: {e}")

    def save_to_csv(self):
        lesson = self.lesson_entry.get()
        score = self.score_entry.get()

        if lesson and score:
            data = {"Lesson": lesson, "Score": score}
            file_exists = os.path.exists("data.csv")

            try:
                with open('data.csv', mode='a', newline='') as file:
                    fieldnames = ["Lesson", "Score"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(data)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save to CSV: {e}")

            finally:
                self.load_csv()
                self.embed_graph()  # Refresh the graph after saving

    def embed_graph(self):
        if not os.path.exists("data.csv"):
            return

        df = pd.read_csv("data.csv")
        df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
        df = df.dropna(subset=["Lesson", "Score"])
        df["Test Number"] = range(1, len(df) + 1)

        fig, ax = plt.subplots(figsize=(5, 4))

        sns.lineplot(data=df, x="Test Number", y="Score", hue="Lesson", marker="o", ax=ax)

        for _, row in df.iterrows():
            ax.text(row["Test Number"], row["Score"] + 2, f"{row['Score']}", ha='center', fontsize=9)

        ax.set_title("Test Scores by Lesson")
        ax.set_xlabel("Number of Tests Completed")
        ax.set_ylabel("Test Score")
        ax.set_xticks(df["Test Number"])
        ax.grid(True)
        plt.tight_layout()

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)


root = tb.Window()
mainApp(root)
root.mainloop()
