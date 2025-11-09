

from pathlib import Path
import sys
import platform
try:
    import ctypes
except Exception:
    ctypes = None
from tkinter import (
    Tk,
    Canvas,
    Entry,
    Text,
    Button,
    PhotoImage,
    Toplevel,
    StringVar,
    OptionMenu,
    Label,
    messagebox,
    Frame,
    Scrollbar,
    LEFT,
    RIGHT,
    BOTH,
    Y,
    VERTICAL,
    NW,
    Radiobutton,
)
from PIL import ImageTk, Image
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Joseph\Documents\Tkinter\Tkinter-Designer\build\build\assets\frame0")


students = []
action_buttons = []
DB_PATH = OUTPUT_PATH / "students.db"  

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def make_dpi_aware() -> None:
    """Make the process DPI aware on Windows to avoid blurry Tk windows.

    This tries several Windows APIs in preference order:
    1. SetProcessDpiAwarenessContext (per-monitor v2) if available
    2. shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    3. user32.SetProcessDPIAware (fallback)

    Only runs on Windows and will silently no-op on other platforms or if ctypes is not available.
    """
    if platform.system().lower() != "windows":
        return
    if not ctypes:
        return
    try:
        user32 = ctypes.windll.user32
        # Preferred: per-monitor v2 (Windows 10+)
        try:
            if hasattr(user32, "SetProcessDpiAwarenessContext"):
                # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
                user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
                return
        except Exception:
            pass

        # Next: shcore.SetProcessDpiAwareness (Windows 8.1+)
        try:
            shcore = ctypes.windll.shcore
            shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            return
        except Exception:
            pass

        # Fallback: system DPI aware
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass
    except Exception:
        # Any failure - don't crash the app for DPI setup
        return


make_dpi_aware()


def init_db():
    """Initialize the SQLite database and create table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            course TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

window = Tk()

window.geometry("996x627")
window.configure(bg = "#FFFFFF")
window.title("LocatR")
# Create an icon image using the PhotoImage class imported from tkinter.
# Use relative_to_assets so the path is resolved against the generated assets folder.
try:
    photo = PhotoImage(file=relative_to_assets("Logo.png"))
    window.iconphoto(False, photo)
except Exception:
    # If loading the icon fails, continue without setting it.
    photo = None


# Main canvas for the window background
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 627,
    width = 996,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Create a frame to hold the scrollable list
list_frame = Frame(window, bg="#FFFFFF")
list_frame.place(x=0, y=170, width=996, height=457)  # Start just below column headers

# Create a canvas for the scrollable content
list_canvas = Canvas(
    list_frame,
    bg="#FFFFFF",
    height=391,
    width=996,
    bd=0,
    highlightthickness=0,
)
list_canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Add a scrollbar
scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=list_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
list_canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the student rows
students_frame = Frame(list_canvas, bg="#FFFFFF")
list_canvas.create_window((0, 0), window=students_frame, anchor=NW, width=996)

# Configure scrolling
def configure_scroll_region(event):
    list_canvas.configure(scrollregion=list_canvas.bbox("all"))
students_frame.bind("<Configure>", configure_scroll_region)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_1 = canvas.create_image(
    186.5,
    64.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    font=("Inter", 14),
    highlightthickness=0
)
entry_1.place(
    x=85.0,
    y=42.5,
    width=250.0,
    height=45.0
)
# Bind search: filter students by student id or name as user types
entry_1.bind("<KeyRelease>", lambda e: render_students())

canvas.create_text(
    40.0,
    143.66665649414062,
    anchor="nw",
    text="STUDENT ID",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    278.0,
    144.0,
    anchor="nw",
    text="NAME",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    492.0,
    144.0,
    anchor="nw",
    text="COURSE",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    678.0,
    144.0,
    anchor="nw",
    text="LOCATION",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    862.0,
    143.66665649414062,
    anchor="nw",
    text="ACTION",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_rectangle(
    -1.0,
    128.0,
    996.00048828125,
    129.0,
    fill="#C2B9B9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_add_student_window(),
    relief="flat"
)
button_1.place(
    x=729.0,
    y=27.0,
    width=245.0,
    height=73.0
)

# Preload the edit icon once and keep a reference to avoid it being garbage-collected
try:
    button_image_2 = Image.open(relative_to_assets("button_edit.png"))
    button_image_2 = button_image_2.resize((80, 26))
    button_image_2 = ImageTk.PhotoImage(button_image_2)
    
    print("success")
except Exception as e:
    button_image_2 = None
    print(e)

# Background for list area
canvas.create_rectangle(
    0.0,
    170.0,
    996.0,
    627.0,
    fill="#FFFFFF",
    outline="")

# --- Student data and UI management ---

# Constants for text display
MAX_NAME_LENGTH = 25  # characters
MAX_COURSE_LENGTH = 20  # characters

def validate_student_id(student_id: str) -> tuple[bool, str]:
    """Validate student ID: must be exactly 10 digits."""
    if not student_id:
        return False, "Student ID is required."
    if not student_id.isdigit():
        return False, "Student ID must contain only numbers."
    if len(student_id) != 10:
        return False, "Student ID must be exactly 10 digits."
    return True, ""

def validate_name(name: str) -> tuple[bool, str]:
    """Validate name: cannot contain numbers."""
    if not name.strip():
        return False, "Name is required."
    if any(char.isdigit() for char in name):
        return False, "Name cannot contain numbers."
    return True, ""

def validate_course(course: str) -> tuple[bool, str]:
    """Validate course: cannot contain numbers."""
    if not course.strip():
        return False, "Course is required."
    if any(char.isdigit() for char in course):
        return False, "Course cannot contain numbers."
    return True, ""

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text and add ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def load_students_from_db():
    """Load all student records from the SQLite database."""
    students.clear()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT student_id, name, course, location FROM students")
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        students.append({
            "student_id": r[0],
            "name": r[1],
            "course": r[2],
            "location": r[3],
        })


def save_students_to_db():
    """Overwrite all student records in the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clear table
    cur.execute("DELETE FROM students")

    # Insert all in-memory student records
    for s in students:
        cur.execute(
            "INSERT INTO students (student_id, name, course, location) VALUES (?, ?, ?, ?)",
            (s.get("student_id", ""), s.get("name", ""), s.get("course", ""), s.get("location", "")),
        )

    conn.commit()
    conn.close()


def render_students() -> None:
    # Clear previous content
    for widget in students_frame.winfo_children():
        widget.destroy()
    action_buttons.clear()

    # Determine which students match the search query (student id or name)
    query = ""
    try:
        query = entry_1.get().strip().lower()
    except Exception:
        query = ""

    visible = []
    if query:
        for i, s in enumerate(students):
            if query in str(s.get("student_id", "")).lower() or query in str(s.get("name", "")).lower():
                visible.append((i, s))
    else:
        visible = list(enumerate(students))

    row_height = 46
    for row_pos, (idx, s) in enumerate(visible):
        # Create a frame for this row
        row_frame = Frame(students_frame, bg="#FFFFFF", height=row_height)
        row_frame.pack(fill="x", pady=4)
        row_frame.pack_propagate(False)  # Maintain fixed height

        # Calculate y position for consistent spacing
        y = row_height/2  # Center text vertically in row
        
        # Student ID (fixed width, no truncation needed)
        Label(row_frame, 
              text=s.get("student_id", ""),
              font=("Inter", 13),
              bg="#FFFFFF",
              anchor="w").place(x=40, y=y-10, width=150)
        
        # Name (truncated if too long)
        Label(row_frame,
              text=truncate_text(s.get("name", ""), MAX_NAME_LENGTH),
              font=("Inter", 13),
              bg="#FFFFFF",
              anchor="w").place(x=230, y=y-10, width=200)
        
        # Course (truncated if too long)
        Label(row_frame,
              text=truncate_text(s.get("course", ""), MAX_COURSE_LENGTH),
              font=("Inter", 13),
              bg="#FFFFFF",
              anchor="w").place(x=450, y=y-10, width=200)
        
        # Location (usually short, no truncation needed)
        Label(row_frame,
              text=s.get("location", ""),
              font=("Inter", 13),
              bg="#FFFFFF",
              anchor="w").place(x=695, y=y-10, width=100)

        # Create an Edit button for each row (opens edit dialog with delete)
        if button_image_2:
            btn = Button(row_frame, 
                         image=button_image_2, 
                         borderwidth=0, 
                         highlightthickness=0, 
                         command=lambda i=idx: open_edit_student_window(i),  
                         relief="flat",
                         bg="#FFFFFF"
            ) # keep reference on the widget
            btn.image = button_image_2
        else:
            btn = Button(row_frame, text="Edit", command=lambda i=idx: open_edit_student_window(i))
        # Place button near the ACTION column
        btn_width = 80
        btn_height = 26
        # Place within the row frame
        btn.place(x=855, y=btn_height/2, width=btn_width, height=btn_height)
        action_buttons.append(btn)


def delete_student(index: int) -> None:
    try:
        students.pop(index)
        save_students_to_db()
        render_students()
    except Exception:
        pass

def open_add_student_window() -> None:

    # --- WINDOW SETUP ---
    win = Toplevel(window)
    win.title("Add Student")
    win.geometry("420x290")
    win.configure(bg="#FFFFFF")
    win.resizable(False, False)
    try:
        logo = PhotoImage(file=relative_to_assets("Logo.png"))
        win.iconphoto(False, logo)
        win.logo = logo  # keep a reference to prevent garbage collection
    except Exception as e:
        print("Logo not loaded:", e)

    # --- CANVAS DESIGN ---
    canvas = Canvas(
        win,
        bg="#FFFFFF",
        height=290,
        width=420,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # --- LABELS (drawn text) ---
    canvas.create_text(
        20.0, 44.0,
        anchor="nw",
        text="Student ID:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        62.0, 92.0,
        anchor="nw",
        text="Name:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        50.0, 139.0,
        anchor="nw",
        text="Course:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        38.0, 187.0,
        anchor="nw",
        text="Location:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    # --- TEXTBOXES / ENTRY FIELDS ---
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(262.38, 52.8, image=entry_image_1)
    id_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    id_entry.place(x=138, y=38.0, width=250.23, height=30.6)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(262.38, 107.37, image=entry_image_2)
    name_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    name_entry.place(x=138, y=85, width=250.23, height=30.6)

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(262.38, 149.62, image=entry_image_3)
    course_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    course_entry.place(x=138, y=135, width=250.23, height=30.6)

    # --- LOCATION RADIO BUTTONS ---
    loc_var = StringVar(value="UP")

    radio_up = Radiobutton(
        win,
        text="UP",
        variable=loc_var,
        value="UP",
        bg="#FFFFFF",
        font=("Inter", 12)
    )
    radio_up.place(x=140, y=185)

    radio_down = Radiobutton(
        win,
        text="DOWN",
        variable=loc_var,
        value="DOWN",
        bg="#FFFFFF",
        font=("Inter", 12)
    )
    radio_down.place(x=200, y=185)

    # --- FUNCTIONALITY (SAVE + CANCEL) ---
    def on_save() -> None:
        sid = id_entry.get().strip()
        name = name_entry.get().strip()
        course = course_entry.get().strip()
        location = loc_var.get().strip()
        
        # Validate each field
        valid_id, id_error = validate_student_id(sid)
        if not valid_id:
            messagebox.showerror("Validation Error", id_error)
            id_entry.focus()
            return

        valid_name, name_error = validate_name(name)
        if not valid_name:
            messagebox.showerror("Validation Error", name_error)
            name_entry.focus()
            return

        valid_course, course_error = validate_course(course)
        if not valid_course:
            messagebox.showerror("Validation Error", course_error)
            course_entry.focus()
            return

        # All validations passed, save the data
        students.append({"student_id": sid, "name": name, "course": course, "location": location})
        save_students_to_db()
        render_students()
        messagebox.showinfo("Success", "Student added successfully!")
        try:
            win.destroy()
        except Exception:
            pass


    # --- BUTTONS (DESIGNED IMAGES) ---
    button_image_1 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_1.png"))

    # Place buttons directly in window, not over canvas drawings
    save_button = Button(
        win,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=on_save,     # will now trigger properly
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        cursor="hand2"
    )
    save_button.place(x=214.28, y=245.99, width=76.19, height=22.00)

    cancel_button = Button(
        win,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=win.destroy,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        cursor="hand2"
    )
    cancel_button.place(x=120.0, y=245.99, width=76.19, height=22.00)

    # Keep references so images aren’t garbage collected
    win.entry_images = [
        entry_image_1, entry_image_2, entry_image_3,
        button_image_1, button_image_2
    ]

    # Raise buttons above canvas (important!)
    save_button.lift()
    cancel_button.lift()



def open_edit_student_window(index: int) -> None:
    # Edit an existing student; the Delete action is available here
    try:
        s = students[index]
    except Exception:
        return

    # --- WINDOW SETUP ---
    win = Toplevel(window)
    win.title("Edit Student")
    win.geometry("420x290")
    win.configure(bg="#FFFFFF")
    win.resizable(False, False)
    try:
        logo = PhotoImage(file=relative_to_assets("Logo.png"))
        win.iconphoto(False, logo)
        win.logo = logo  # keep a reference to prevent garbage collection
    except Exception as e:
        print("Logo not loaded:", e)

    # --- CANVAS DESIGN ---
    canvas = Canvas(
        win,
        bg="#FFFFFF",
        height=290,
        width=420,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # --- LABELS (drawn text) ---
    canvas.create_text(
        20.0, 44.0,
        anchor="nw",
        text="Student ID:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        62.0, 92.0,
        anchor="nw",
        text="Name:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        50.0, 139.0,
        anchor="nw",
        text="Course:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    canvas.create_text(
        38.0, 187.0,
        anchor="nw",
        text="Location:",
        fill="#000000",
        font=("Inter", 18 * -1)
    )

    # --- TEXTBOXES / ENTRY FIELDS ---
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(262.38, 52.8, image=entry_image_1)
    id_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    id_entry.place(x=138, y=38.0, width=250.23, height=30.6)
    id_entry.insert(0, s.get("student_id", ""))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(262.38, 107.37, image=entry_image_2)
    name_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    name_entry.place(x=138, y=85, width=250.23, height=30.6)
    name_entry.insert(0, s.get("name", ""))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(262.38, 149.62, image=entry_image_3)
    course_entry = Entry(
        win,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    course_entry.place(x=138, y=135, width=250.23, height=30.6)
    course_entry.insert(0, s.get("course", ""))

    # --- LOCATION RADIO BUTTONS ---
    loc_var = StringVar(value=s.get("location", "UP"))

    radio_up = Radiobutton(
        win,
        text="UP",
        variable=loc_var,
        value="UP",
        bg="#FFFFFF",
        font=("Inter", 12)
    )
    radio_up.place(x=140, y=185)

    radio_down = Radiobutton(
        win,
        text="DOWN",
        variable=loc_var,
        value="DOWN",
        bg="#FFFFFF",
        font=("Inter", 12)
    )
    radio_down.place(x=200, y=185)

    def on_save() -> None:
        sid = id_entry.get().strip()
        name = name_entry.get().strip()
        course = course_entry.get().strip()
        location = loc_var.get().strip()
        
        # Validate each field
        valid_id, id_error = validate_student_id(sid)
        if not valid_id:
            messagebox.showerror("Validation Error", id_error)
            id_entry.focus()
            return

        valid_name, name_error = validate_name(name)
        if not valid_name:
            messagebox.showerror("Validation Error", name_error)
            name_entry.focus()
            return

        valid_course, course_error = validate_course(course)
        if not valid_course:
            messagebox.showerror("Validation Error", course_error)
            course_entry.focus()
            return

        # All validations passed, update the data
        students[index] = {"student_id": sid, "name": name, "course": course, "location": location}
        save_students_to_db()
        render_students()
        messagebox.showinfo("Success", "Student updated successfully!")
        try:
            win.destroy()
        except Exception:
            pass

    def on_delete() -> None:
        if messagebox.askyesno("Confirm", "Delete this student?"):
            try:
                students.pop(index)
                save_students_to_db()
                render_students()
            except Exception:
                pass
            try:
                win.destroy()
            except Exception:
                pass

    # --- BUTTONS ---
    # Create styled buttons without images first
    save = PhotoImage(file=relative_to_assets("button_2.png"))
    cancel = PhotoImage(file=relative_to_assets("button_1.png"))
    delete = PhotoImage(file=relative_to_assets("button_3.png"))
    
    save_button = Button(
        win,
        image=save,
        text="Save",
        borderwidth=0,
        highlightthickness=0,
        command=on_save,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        cursor="hand2"
    )
    save_button.place(x=255, y=245, width=80, height=26)


    delete_button = Button(
        win,
        image=delete,
        borderwidth=0,
        highlightthickness=0,
        command=on_delete,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        cursor="hand2"
    )
    delete_button.place(x=170, y=245, width=80, height=26)

    cancel_button = Button(
        win,
        image=cancel,
        borderwidth=0,
        highlightthickness=0,
        command=win.destroy,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        cursor="hand2"
    )
    cancel_button.place(x=85, y=245, width=80, height=26)

    # Keep entry image references
    win.entry_images = [
        entry_image_1, entry_image_2, entry_image_3, save, cancel, delete
    ]

    # Ensure buttons are visible
    save_button.lift()
    delete_button.lift()
    cancel_button.lift()


# Load any existing students and render them
init_db()
load_students_from_db()
render_students()
window.resizable(False, False)
window.mainloop()
