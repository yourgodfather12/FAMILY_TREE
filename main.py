import tkinter as tk
from tkinter import messagebox


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#2D2D2D", foreground="white", relief="solid",
                         borderwidth=1)
        label.pack(ipadx=5)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()


class FamilyTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Family Tree")
        self.root.config(bg="#1E1E1E")

        # Initialize family tree data
        self.family_tree = {
            'John': {'spouse': 'Jane', 'children': ['Mary', 'Tom'], 'birthdate': '1970-01-01', 'gender': 'Male'},
            'Mary': {'spouse': '', 'children': ['Peter', 'Alice'], 'birthdate': '1975-03-15', 'gender': 'Female'},
            'Tom': {'spouse': '', 'children': ['Jack', 'Jill'], 'birthdate': '1978-11-20', 'gender': 'Male'}
        }

        # Create main frame
        self.main_frame = tk.Frame(root, bg="#1E1E1E")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create canvas for drawing the tree
        self.canvas = tk.Canvas(self.main_frame, bg="#1E1E1E", width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create details frame
        self.details_frame = tk.Frame(self.main_frame, bg="#2D2D2D", width=200, height=600)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Add controls for editing the tree
        self.add_controls()

        # Draw family tree
        self.draw_tree()

    def draw_tree(self):
        # Clear canvas
        self.canvas.delete("all")

        # Draw nodes and edges
        for parent, info in self.family_tree.items():
            parent_coords = (200, 100)
            self.canvas.create_oval(parent_coords[0] - 20, parent_coords[1] - 20, parent_coords[0] + 20,
                                    parent_coords[1] + 20, fill='#3F3F3F')
            self.canvas.create_text(parent_coords[0], parent_coords[1], text=parent, fill="white")

            # Display detailed information
            detail_text = f"Spouse: {info['spouse']}\nChildren: {', '.join(info['children'])}\nBirthdate: {info['birthdate']}\nGender: {info['gender']}"
            self.canvas.create_text(parent_coords[0], parent_coords[1] + 40, text=detail_text, fill="white")

            for child in info['children']:
                child_coords = (200 + 100 * (info['children'].index(child) - 0.5), 250)
                self.canvas.create_oval(child_coords[0] - 20, child_coords[1] - 20, child_coords[0] + 20,
                                        child_coords[1] + 20, fill='#3F3F3F')
                self.canvas.create_text(child_coords[0], child_coords[1], text=child, fill="white")

                # Draw edge
                self.canvas.create_line(parent_coords[0], parent_coords[1] + 20, child_coords[0], child_coords[1] - 20,
                                        fill="white")

    def add_controls(self):
        # Add entry fields for adding/editing family members
        self.parent_label = tk.Label(self.details_frame, text="Parent:", bg="#2D2D2D", fg="white")
        self.parent_label.pack()
        self.parent_entry = tk.Entry(self.details_frame)
        self.parent_entry.pack()

        self.child_label = tk.Label(self.details_frame, text="Child:", bg="#2D2D2D", fg="white")
        self.child_label.pack()
        self.child_entry = tk.Entry(self.details_frame)
        self.child_entry.pack()

        self.spouse_label = tk.Label(self.details_frame, text="Spouse:", bg="#2D2D2D", fg="white")
        self.spouse_label.pack()
        self.spouse_entry = tk.Entry(self.details_frame)
        self.spouse_entry.pack()

        self.birthdate_label = tk.Label(self.details_frame, text="Birthdate:", bg="#2D2D2D", fg="white")
        self.birthdate_label.pack()
        self.birthdate_entry = tk.Entry(self.details_frame, placeholder="YYYY-MM-DD")
        self.birthdate_entry.pack()

        self.gender_label = tk.Label(self.details_frame, text="Gender:", bg="#2D2D2D", fg="white")
        self.gender_label.pack()
        self.gender_entry = tk.Entry(self.details_frame)
        self.gender_entry.pack()

        # Add buttons for adding/editing/removing family members
        self.add_button = tk.Button(self.details_frame, text="Add Member", bg="#4CAF50", fg="white",
                                    command=self.add_member)
        self.add_button.pack(pady=5, padx=10, fill=tk.X)
        self.remove_button = tk.Button(self.details_frame, text="Remove Member", bg="#F44336", fg="white",
                                       command=self.remove_member)
        self.remove_button.pack(pady=5, padx=10, fill=tk.X)

        # Add tooltips
        self.add_tooltips()

    def add_tooltips(self):
        ToolTip(self.parent_label, "Enter parent's name")
        ToolTip(self.child_label, "Enter child's name")
        ToolTip(self.spouse_label, "Enter spouse's name")
        ToolTip(self.birthdate_label, "Enter birthdate (YYYY-MM-DD)")
        ToolTip(self.gender_label, "Enter gender (Male/Female)")

    def add_member(self):
        parent = self.parent_entry.get()
        child = self.child_entry.get()
        spouse = self.spouse_entry.get()
        birthdate = self.birthdate_entry.get()
        gender = self.gender_entry.get()

        if parent and child:
            if parent not in self.family_tree:
                self.family_tree[parent] = {'spouse': spouse, 'children': [], 'birthdate': birthdate, 'gender': gender}
            self.family_tree[parent]['children'].append(child)
            self.draw_tree()
            self.show_message("Member added successfully.")
        else:
            self.show_message("Please enter both parent and child names.")

    def remove_member(self):
            parent = self.parent_entry.get()
            child = self.child_entry.get()

            if parent and child:
                if parent in self.family_tree and child in self.family_tree[parent]['children']:
                    self.family_tree[parent]['children'].remove(child)
                    self.draw_tree()
                    self.show_message("Member removed successfully.")
                else:
                    self.show_message("Parent-child relationship not found.")
            else:
                self.show_message("Please enter both parent and child names.")

    def show_message(self, message):
            messagebox.showinfo("Message", message)

    root = tk.Tk()
    app = FamilyTreeApp(root)
    root.mainloop()

