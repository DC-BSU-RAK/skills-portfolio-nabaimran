# Student Manager Application with Extended Features
# This application allows users to manage student records,
# including viewing, adding, deleting, and updating student information.    
# Some parts of the code are inspired by ChatGPT. such as the GUI layout and basic structure. and then i added more features and functionalities to it.

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os

 # define the main application class
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("950x600")
        self.root.config(bg="#F4F5FB")

        self.students = []
        self.load_students()

        # Header
        header = tk.Frame(root, bg="#1F3A93", height=60)
        header.pack(side="top", fill="x")
        tk.Label(
            header,
            text="University Student Manager",
            bg="#1F3A93",
            fg="white",
            font=("Georgia", 22, "bold")
        ).pack(padx=20, pady=12)

        # Left side menu frame
        self.menu_frame = tk.Frame(root, bg="#2C3E50", width=240)
        self.menu_frame.pack(side="left", fill="y")

        # Content frame
        self.content_frame = tk.Frame(root, bg="#F4F5FB")
        self.content_frame.pack(side="right", expand=True, fill="both")

        self.create_menu_buttons()

        # Text area for output
        self.text_area = ScrolledText(
            self.content_frame,
            bg="white",
            fg="#2C3E50",
            font=("Georgia", 12),
            bd=0,
            highlightthickness=1,
            highlightbackground="#D0D3D4",
            relief="flat"
        )
        self.text_area.pack(padx=20, pady=20, fill="both", expand=True)


 # section to load student data from file
    def load_students(self):
        file_path = r"Assessment 1 - Skills Portfolio\Exercise3\studentMarks.txt"
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        self.students.clear()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 6:
                continue
            try:
                code = int(parts[0])
                name = parts[1]
                c1, c2, c3 = map(int, parts[2:5])
                exam = int(parts[5])
                self.students.append({
                    "code": code,
                    "name": name,
                    "coursework": [c1, c2, c3],
                    "exam": exam
                })
            except:
                continue


    # section to save student data to file
    def save_students(self):
        file_path = r"Assessment 1 - Skills Portfolio\Exercise3\studentMarks.txt"
        try:
            with open(file_path, "w") as file:
                for s in self.students:
                    line = (
                        f"{s['code']},{s['name']},"
                        f"{s['coursework'][0]},{s['coursework'][1]},{s['coursework'][2]},"
                        f"{s['exam']}\n"
                    )
                    file.write(line)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")


 # section to create menu buttons
    def create_menu_buttons(self):
        buttons = [
            ("View All Students", self.view_all_students),
            ("View Individual Student", self.view_individual_student),
            ("Show Highest Scorer", self.show_highest_scorer),
            ("Show Lowest Scorer", self.show_lowest_scorer),
            ("Sort Student Records", self.sort_student_records),
            ("Add Student Record", self.add_student_record_dialog),
            ("Delete Student Record", self.delete_student_record),
            ("Update Student Record", self.update_student_record),
        ]

        bg_color = "#2C3E50"
        fg_color = "#ECF0F1"
        hover_bg = "#3B5998"
        font_style = ("Georgia", 13)

        for text, cmd in buttons:
            btn = tk.Label(
                self.menu_frame,
                text=text,
                bg=bg_color,
                fg=fg_color,
                font=font_style,
                padx=20,
                pady=12,
                anchor="w",
                cursor="hand2"
            )
            btn.pack(fill="x", pady=3, padx=8)
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=hover_bg))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=bg_color)) # reset color on leave


 # section to calculate total marks and percentage
    def calculate_total_and_percentage(self, student):
        coursework_total = sum(student["coursework"])
        exam_mark = student["exam"]
        total_marks = coursework_total + exam_mark
        percentage = (total_marks / 160) * 100
        return coursework_total, exam_mark, percentage

 # section to calculate grade based on percentage
    def calculate_grade(self, percentage):
        if percentage >= 70:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "D"
        else:
            return "F"

 # section to format student information for display
    def format_student_info(self, student):
        coursework_total, exam_mark, percentage = self.calculate_total_and_percentage(student)
        grade = self.calculate_grade(percentage)
        lines = [
            f"Student Name: {student['name']}",
            f"Student Code: {student['code']}",
            f"Total Coursework Mark: {coursework_total}/60",
            f"Exam Mark: {exam_mark}/100",
            f"Overall Percentage: {percentage:.2f}%",
            f"Grade: {grade}",
            ""
        ]
        return "\n".join(lines) # return formatted string


# section to view all students
    def view_all_students(self):
        self.text_area.delete(1.0, tk.END)
        if not self.students:
            self.text_area.insert(tk.END, "No student records loaded.\n")
            return

        total_percentage_sum = 0
        count = len(self.students)
  # to loop through all students and display their info
        for student in self.students:
            info = self.format_student_info(student)
            self.text_area.insert(tk.END, info + "\n")
            total_percentage_sum += self.calculate_total_and_percentage(student)[2]

        average_percentage = total_percentage_sum / count if count > 0 else 0
        self.text_area.insert(tk.END, f"Number of Students: {count}\n")
        self.text_area.insert(tk.END, f"Average Percentage: {average_percentage:.2f}%\n")
 

 # section to view individual student
    def view_individual_student(self):
        inp = simpledialog.askstring("Input", "Enter Student Code or Name:")
        if not inp:
            return

        found = None
        try:
            code = int(inp)
            for student in self.students:
                if student["code"] == code:
                    found = student
                    break
        except: # i added a case insensitive search so you can only type the exact name as given in the database
            for student in self.students:
                if student["name"].lower() == inp.lower(): 
                    found = student
                    break

        self.text_area.delete(1.0, tk.END)
        if found:
            info = self.format_student_info(found)
            self.text_area.insert(tk.END, info)
        else:
            self.text_area.insert(tk.END, "No student found with that code or name.\n")
  

  # section to show highest scorer
    def show_highest_scorer(self):
        if not self.students:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "No student records loaded.\n")
            return

        highest = max(self.students, key=lambda s: self.calculate_total_and_percentage(s)[2]) 
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Student with Highest Overall Mark:\n\n")
        self.text_area.insert(tk.END, self.format_student_info(highest))
# section to show lowest scorer
    def show_lowest_scorer(self):
        if not self.students:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "No student records loaded.\n")
            return

        lowest = min(self.students, key=lambda s: self.calculate_total_and_percentage(s)[2])
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Student with Lowest Overall Mark:\n\n")
        self.text_area.insert(tk.END, self.format_student_info(lowest))


# section to sort student records
    def sort_student_records(self):
        choice = simpledialog.askstring("Sort", "Sort ascending or descending? (asc/desc)")
        if choice not in ["asc", "desc"]:
            messagebox.showerror("Error", "Invalid choice. Enter 'asc' or 'desc'.")
            return

        reverse = (choice == "desc")
        self.students.sort(key=lambda s: self.calculate_total_and_percentage(s)[2], reverse=reverse)
        self.view_all_students()

# section to add student record dialog
    def add_student_record_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("420x360")
        dialog.config(bg="#F4F5FB")
        dialog.grab_set()
  
        tk.Label(
            dialog,
            text="Add New Student",
            bg="#F4F5FB",
            fg="#2C3E50",
            font=("Georgia", 16, "bold")
        ).pack(pady=10)

        form_frame = tk.Frame(dialog, bg="#F4F5FB")
        form_frame.pack(padx=20, pady=10, fill="x")

        labels = [
            "Student Code (1000-9999):",
            "Name:",
            "Coursework Mark 1 (0-20):",
            "Coursework Mark 2 (0-20):",
            "Coursework Mark 3 (0-20):",
            "Exam Mark (0-100):"
        ]

        self.entry_vars = [] # to hold entry variables
         # create labels and entry fields
        font_label = ("Georgia", 12)
        font_entry = ("Georgia", 12)

        for i, text in enumerate(labels):
            tk.Label(
                form_frame,
                text=text,
                bg="#F4F5FB",
                fg="#2C3E50",
                font=font_label,
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=4)
            var = tk.StringVar()
            entry = tk.Entry(
                form_frame,
                textvariable=var,
                font=font_entry,
                bg="white",
                fg="#2C3E50",
                relief="solid",
                bd=1
            )
            entry.grid(row=i, column=1, sticky="ew", pady=4, padx=8)
            form_frame.grid_columnconfigure(1, weight=1)
            self.entry_vars.append(var)

        btn_frame = tk.Frame(dialog, bg="#F4F5FB")
        btn_frame.pack(pady=15)
  # section to handle save action

        def on_save():
            try:
                code = int(self.entry_vars[0].get())
                if any(s["code"] == code for s in self.students):
                    messagebox.showerror("Error", "Student code already exists!", parent=dialog)
                    return
                name = self.entry_vars[1].get().strip()
                c1 = int(self.entry_vars[2].get())
                c2 = int(self.entry_vars[3].get())
                c3 = int(self.entry_vars[4].get())
                exam = int(self.entry_vars[5].get())

                if not name:
                    messagebox.showerror("Error", "Name cannot be empty.", parent=dialog)
                    return
                for c in [c1, c2, c3]:
                    if c < 0 or c > 20:
                        messagebox.showerror("Error", "Coursework marks must be 0-20.", parent=dialog)
                        return
                if exam < 0 or exam > 100:
                    messagebox.showerror("Error", "Exam mark must be 0-100.", parent=dialog)
                    return

                new_student = {
                    "code": code,
                    "name": name,
                    "coursework": [c1, c2, c3],
                    "exam": exam
                }
                self.students.append(new_student) # add new student to list
                self.save_students()
                messagebox.showinfo("Success", "Student added successfully!", parent=dialog)
                dialog.destroy()
                self.view_all_students()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input or error: {e}", parent=dialog)
  # section to handle cancel action
        def on_cancel():
            dialog.destroy()

        save_btn = tk.Button(
            btn_frame,
            text="Save",
            command=on_save,
            bg="#1F3A93",
            fg="white",
            font=("Georgia", 12),
            relief="flat",
            padx=15,
            pady=6
        )
        save_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=on_cancel,
            bg="#7F8C8D",
            fg="white",
            font=("Georgia", 12),
            relief="flat",
            padx=15,
            pady=6
        )
        cancel_btn.pack(side="left", padx=10)
  # section to delete student record
    def delete_student_record(self):
        inp = simpledialog.askstring("Input", "Enter student code or name to delete:")
        if not inp:
            return

        found = None
        try:
            code = int(inp)
            for s in self.students:
                if s["code"] == code:
                    found = s
                    break
        except:
            for s in self.students:
                if s["name"].lower() == inp.lower():
                    found = s
                    break

        if found:
            self.students.remove(found)
            self.save_students()
            messagebox.showinfo("Success", "Student record deleted.")
            self.view_all_students()
        else:
            messagebox.showerror("Error", "Student not found.")
  
  # section to update student record
    def update_student_record(self):
        inp = simpledialog.askstring("Input", "Enter student code or name to update:")
        if not inp:
            return

        found = None
        try:
            code = int(inp)
            for s in self.students:
                if s["code"] == code:
                    found = s
                    break
        except:
            for s in self.students:
                if s["name"].lower() == inp.lower():
                    found = s
                    break

        if not found:
            messagebox.showerror("Error", "Student not found.")
            return
   # specify which field to update
        field = simpledialog.askstring("Update", "Enter field to update: (code, name, c1, c2, c3, exam)") 
        if not field or field not in ["code", "name", "c1", "c2", "c3", "exam"]:
            messagebox.showerror("Error", "Invalid field.")
            return

        try:
            if field == "code":
                new_value = int(simpledialog.askstring("Update", "Enter new student code:"))
                if any(s["code"] == new_value for s in self.students if s != found):
                    messagebox.showerror("Error", "Student code already exists!")
                    return
                found["code"] = new_value
            elif field == "name":
                new_value = simpledialog.askstring("Update", "Enter new student name:")
                found["name"] = new_value
            elif field in ["c1", "c2", "c3"]:
                idx = int(field[-1]) - 1
                new_value = int(simpledialog.askstring("Update", f"Enter new coursework mark {idx+1}:"))
                if new_value < 0 or new_value > 20:
                    messagebox.showerror("Error", "Mark must be between 0 and 20.")
                    return
                found["coursework"][idx] = new_value
            elif field == "exam":
                new_value = int(simpledialog.askstring("Update", "Enter new exam mark (0-100):"))
                if new_value < 0 or new_value > 100:
                    messagebox.showerror("Error", "Mark must be between 0 and 100.")
                    return
                found["exam"] = new_value
 
 # save changes
            self.save_students()
            messagebox.showinfo("Success", "Student record updated.")
            self.view_all_students()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or error: {e}")

# main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
