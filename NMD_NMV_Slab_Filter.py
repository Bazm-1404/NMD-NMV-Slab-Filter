
# ============================================================
# GUI NMD NMV Slab Filtering Application
# ============================================================

# Importing Libraries

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

from datetime import datetime


# ============================================================
# Creating Main Window
# ============================================================

root = tk.Tk()

root.title("GUI NMD NMV Slab Filtering Application")

root.geometry("800x800")

root.minsize(800, 800)

root.resizable(True, True)


# ============================================================
# Variables
# ============================================================

input_file_var = tk.StringVar()

output_file_var = tk.StringVar()

field_index_var = tk.StringVar(value="0")

logic_var = tk.StringVar(value="Less Than")

min_value_var = tk.StringVar()

max_value_var = tk.StringVar()

output_format_var = tk.StringVar(
    value="Selected Index + Header"
)


processed_rows = 0

saved_rows = 0


# ============================================================
# Generate Output Filename
# ============================================================

def generate_output_filename():

    input_file = input_file_var.get().strip()

    if not input_file:

        return

    directory = os.path.dirname(input_file)

    base_name = os.path.splitext(
        os.path.basename(input_file)
    )[0]

    current_date = datetime.now().strftime("%b_%d")

    logic = logic_var.get()


    # Less Than Logic

    if logic == "Less Than":

        max_value = max_value_var.get().strip()

        if not max_value:

            return

        output_name = (
            f"{base_name}_LT_{max_value}_{current_date}.txt"
        )


    # Between Logic

    elif logic == "Between":

        min_value = min_value_var.get().strip()

        max_value = max_value_var.get().strip()

        if not min_value or not max_value:

            return

        output_name = (
            f"{base_name}_{min_value}_{max_value}_{current_date}.txt"
        )


    else:

        return


    # Setting Output File Path

    output_file_var.set(
        os.path.join(directory, output_name)
    )


# ============================================================
# Browse Input File
# ============================================================

def browse_input_file():

    filename = filedialog.askopenfilename(
        title="Select Input File",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if filename:

        input_file_var.set(filename)

        generate_output_filename()


# ============================================================
# Browse Output File
# ============================================================

def browse_output_file():

    filename = filedialog.asksaveasfilename(
        title="Save Output File",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if filename:

        output_file_var.set(filename)


# ============================================================
# Update Filtering Fields
# ============================================================

def update_filter_fields(*args):

    logic = logic_var.get()


    if logic == "Less Than":

        min_entry.config(
            state="disabled"
        )

        min_value_var.set("")

        max_label.config(
            text="Maximum Value (Y):"
        )


    elif logic == "Between":

        min_entry.config(
            state="normal"
        )

        max_label.config(
            text="Maximum Value:"
        )


    generate_output_filename()


# ============================================================
# Automatically Update Output Filename
# ============================================================

def update_output_filename(*args):

    generate_output_filename()


# ============================================================
# Processing Function
# ============================================================

def process_file():

    try:

        # Getting Input Values

        input_file = input_file_var.get().strip()

        output_file = output_file_var.get().strip()

        field_index = int(
            field_index_var.get()
        )

        logic = logic_var.get()

        output_format = output_format_var.get()


        # Validating Input File

        if not input_file:

            messagebox.showerror(
                "Error",
                "Please select an input file."
            )

            return


        if not os.path.isfile(input_file):

            messagebox.showerror(
                "Error",
                "Input file does not exist."
            )

            return


        # Validating Output File

        if not output_file:

            messagebox.showerror(
                "Error",
                "Please specify an output file."
            )

            return


        if os.path.abspath(input_file) == os.path.abspath(output_file):

            messagebox.showerror(
                "Error",
                "Input and output files cannot be the same."
            )

            return


        # Validating Field Index

        if field_index < 0:

            messagebox.showerror(
                "Error",
                "Field index cannot be negative."
            )

            return


        # Validating Output Format

        if output_format not in [
            "Selected Index + Header",
            "Index 0 Only (No Header)"
        ]:

            messagebox.showerror(
                "Error",
                "Please select a valid output format."
            )

            return


        # Validating Filtering Values

        if logic == "Less Than":

            max_value = float(
                max_value_var.get()
            )

            min_value = None


        elif logic == "Between":

            min_value = float(
                min_value_var.get()
            )

            max_value = float(
                max_value_var.get()
            )


            if min_value > max_value:

                messagebox.showerror(
                    "Error",
                    "Minimum value cannot be greater than maximum value."
                )

                return


        # Initializing Counters

        global processed_rows, saved_rows

        processed_rows = 0

        saved_rows = 0


        # Disabling Start Button

        start_button.config(
            state="disabled"
        )


        # Resetting Progress

        progress_bar["value"] = 0

        progress_label.config(
            text="0%"
        )

        status_label.config(
            text="Starting file processing..."
        )


        # Starting Background Thread

        thread = threading.Thread(
            target=run_processing,
            args=(
                input_file,
                output_file,
                field_index,
                logic,
                min_value,
                max_value,
                output_format
            )
        )

        thread.daemon = True

        thread.start()


    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
        )


# ============================================================
# File Processing
# ============================================================

def run_processing(
    input_file,
    output_file,
    field_index,
    logic,
    min_value,
    max_value,
    output_format
):

    global processed_rows, saved_rows

    try:

        # Getting Total File Size

        total_size = os.path.getsize(
            input_file
        )

        processed_bytes = 0


        # Opening Files

        with open(
            input_file,
            "r",
            buffering=1024 * 1024
        ) as input_file:

            with open(
                output_file,
                "w",
                buffering=1024 * 1024
            ) as output_handle:


                # Reading Header

                header = input_file.readline()


                if not header:

                    raise ValueError(
                        "The input file is empty."
                    )


                header_fields = header.rstrip(
                    "\r\n"
                ).split(",")


                # Validating Field Index

                if field_index >= len(header_fields):

                    raise ValueError(
                        "Field index is outside the available columns."
                    )


                # Writing Header Based on Output Format

                if output_format == "Selected Index + Header":

                    output_header = (
                        header_fields[0]
                        + ","
                        + header_fields[field_index]
                    )

                    output_handle.write(
                        output_header + "\n"
                    )


                # Processing Data Rows

                for line in input_file:


                    # Counting Processed Rows

                    processed_rows += 1


                    processed_bytes += len(
                        line.encode("utf-8")
                    )


                    # Splitting Fields

                    fields = line.rstrip(
                        "\r\n"
                    ).split(",")


                    # Validating Row Length

                    if field_index >= len(fields):

                        continue


                    # Getting Selected Value

                    try:

                        selected_value = float(
                            fields[field_index]
                        )

                    except ValueError:

                        continue


                    # Applying Filtering Logic

                    if logic == "Less Than":

                        condition = (
                            selected_value < max_value
                        )


                    elif logic == "Between":

                        condition = (
                            min_value
                            <= selected_value
                            <= max_value
                        )


                    # Saving Matching Rows

                    if condition:


                        # Option 1: Index 0 + Selected Index

                        if output_format == "Selected Index + Header":

                            output_line = (
                                fields[0]
                                + ","
                                + fields[field_index]
                            )


                        # Option 2: Index 0 Only

                        elif output_format == "Index 0 Only (No Header)":

                            output_line = fields[0]


                        # Writing Output

                        output_handle.write(
                            output_line + "\n"
                        )


                        # Counting Saved Rows

                        saved_rows += 1


                    # Updating Progress Every 100,000 Rows

                    if processed_rows % 100000 == 0:


                        progress = (
                            processed_bytes / total_size * 100
                            if total_size > 0
                            else 0
                        )


                        root.after(
                            0,
                            update_progress,
                            progress,
                            processed_rows,
                            saved_rows
                        )


        # Processing Completed

        root.after(
            0,
            processing_completed,
            processed_rows,
            saved_rows,
            output_file
        )


    except Exception as error:


        root.after(
            0,
            processing_error,
            str(error)
        )


# ============================================================
# Update Progress
# ============================================================

def update_progress(
    progress,
    processed,
    saved
):

    progress_bar["value"] = progress

    progress_label.config(
        text=f"{progress:.2f}%"
    )

    status_label.config(
        text=(
            f"Processed: {processed:,} rows | "
            f"Saved: {saved:,} rows | "
            f"Excluded: {processed - saved:,} rows"
        )
    )


# ============================================================
# Processing Completed
# ============================================================

def processing_completed(
    processed,
    saved,
    output_file
):

    progress_bar["value"] = 100

    progress_label.config(
        text="100%"
    )


    status_label.config(
        text=(
            f"Processed: {processed:,} rows | "
            f"Saved: {saved:,} rows | "
            f"Excluded: {processed - saved:,} rows"
        )
    )


    start_button.config(
        state="normal"
    )


    messagebox.showinfo(
        "Processing Completed",
        (
            "Processing Completed Successfully!\n\n"
            f"Total Rows Processed: {processed:,}\n"
            f"Total Rows Saved: {saved:,}\n"
            f"Total Rows Excluded: {processed - saved:,}\n\n"
            f"Output File:\n{output_file}"
        )
    )


# ============================================================
# Processing Error
# ============================================================

def processing_error(error):

    start_button.config(
        state="normal"
    )


    messagebox.showerror(
        "Processing Error",
        error
    )


# ============================================================
# GUI Layout
# ============================================================

# Main Frame

main_frame = ttk.Frame(
    root,
    padding=20
)

main_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# Application Title
# ============================================================

title_label = ttk.Label(
    main_frame,
    text="NMD / NMV Slab Filtering Application",
    font=("Arial", 18, "bold")
)

title_label.pack(
    pady=(0, 20)
)


# ============================================================
# Input File
# ============================================================

input_frame = ttk.LabelFrame(
    main_frame,
    text="Input File",
    padding=10
)

input_frame.pack(
    fill="x",
    pady=5
)


input_entry = ttk.Entry(
    input_frame,
    textvariable=input_file_var,
    width=65
)

input_entry.grid(
    row=0,
    column=0,
    padx=5
)


input_button = ttk.Button(
    input_frame,
    text="Browse",
    command=browse_input_file
)

input_button.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Field Index
# ============================================================

field_frame = ttk.LabelFrame(
    main_frame,
    text="Field Selection",
    padding=10
)

field_frame.pack(
    fill="x",
    pady=5
)


ttk.Label(
    field_frame,
    text="Field Index (0-based):"
).grid(
    row=0,
    column=0,
    padx=5
)


field_entry = ttk.Entry(
    field_frame,
    textvariable=field_index_var,
    width=15
)

field_entry.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Filtering Logic
# ============================================================

filter_frame = ttk.LabelFrame(
    main_frame,
    text="Filtering Logic",
    padding=10
)

filter_frame.pack(
    fill="x",
    pady=5
)


ttk.Label(
    filter_frame,
    text="Filtering Logic:"
).grid(
    row=0,
    column=0,
    padx=5
)


logic_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=logic_var,
    values=[
        "Less Than",
        "Between"
    ],
    state="readonly",
    width=20
)

logic_dropdown.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Minimum Value
# ============================================================

ttk.Label(
    filter_frame,
    text="Minimum Value (X):"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=10
)


min_entry = ttk.Entry(
    filter_frame,
    textvariable=min_value_var,
    width=20
)

min_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=10
)


# ============================================================
# Maximum Value
# ============================================================

max_label = ttk.Label(
    filter_frame,
    text="Maximum Value (Y):"
)

max_label.grid(
    row=2,
    column=0,
    padx=5
)


max_entry = ttk.Entry(
    filter_frame,
    textvariable=max_value_var,
    width=20
)

max_entry.grid(
    row=2,
    column=1,
    padx=5
)


# ============================================================
# Output Format
# ============================================================

format_frame = ttk.LabelFrame(
    main_frame,
    text="Output Format",
    padding=10
)

format_frame.pack(
    fill="x",
    pady=5
)


ttk.Label(
    format_frame,
    text="Select Output Format:"
).grid(
    row=0,
    column=0,
    padx=5
)


format_dropdown = ttk.Combobox(
    format_frame,
    textvariable=output_format_var,
    values=[
        "Selected Index + Header",
        "Index 0 Only (No Header)"
    ],
    state="readonly",
    width=30
)

format_dropdown.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Output File
# ============================================================

output_frame = ttk.LabelFrame(
    main_frame,
    text="Output File",
    padding=10
)

output_frame.pack(
    fill="x",
    pady=5
)


output_entry = ttk.Entry(
    output_frame,
    textvariable=output_file_var,
    width=65
)

output_entry.grid(
    row=0,
    column=0,
    padx=5
)


output_button = ttk.Button(
    output_frame,
    text="Browse",
    command=browse_output_file
)

output_button.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Progress Bar
# ============================================================

progress_frame = ttk.LabelFrame(
    main_frame,
    text="Processing Progress",
    padding=10
)

progress_frame.pack(
    fill="x",
    pady=10
)


progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=650,
    mode="determinate"
)

progress_bar.pack(
    pady=5
)


progress_label = ttk.Label(
    progress_frame,
    text="0%",
    font=("Arial", 10, "bold")
)

progress_label.pack()


# ============================================================
# Status Label
# ============================================================

status_label = ttk.Label(
    main_frame,
    text="Ready to process.",
    font=("Arial", 10)
)

status_label.pack(
    pady=5
)


# ============================================================
# Start Processing Button
# ============================================================

start_button = tk.Button(
    main_frame,
    text="▶  START PROCESSING",
    command=process_file,
    font=("Arial", 14, "bold"),
    bg="#198754",
    fg="white",
    activebackground="#146c43",
    activeforeground="white",
    width=30,
    height=2,
    cursor="hand2"
)

start_button.pack(
    pady=15
)


# ============================================================
# Connecting Variables to Output Filename
# ============================================================

logic_var.trace_add(
    "write",
    update_filter_fields
)


min_value_var.trace_add(
    "write",
    update_output_filename
)


max_value_var.trace_add(
    "write",
    update_output_filename
)


# ============================================================
# Initial GUI Configuration
# ============================================================

update_filter_fields()


# ============================================================
# Running Application
# ============================================================

root.mainloop()

