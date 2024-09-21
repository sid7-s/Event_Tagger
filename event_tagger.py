import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pandas as pd

teams = ["Team A", "Team B"]
players = 5
players_team_a = ['A' + str(i) for i in range(1, players + 1)]
players_team_b = ['B' + str(i) for i in range(1, players + 1)]
event_data = [] # To store the match events


# Function to handle coordinate click on the canvas
def display_cordinate(event):
    # Scale the coordinates to match a 100x60 grid
    scaled_x = int(event.x * (100 / 500))  # 500px canvas width to 100 units
    scaled_y = int(event.y * (60 / 300))  # 300px canvas height to 60 units

    # Set the scaled coordinates in the entries
    x_coord_entry.delete(0, 'end')
    x_coord_entry.insert(0, str(scaled_x))
    y_coord_entry.delete(0, 'end')
    y_coord_entry.insert(0, str(scaled_y))


# Insert team and player names (already existing)
def insert_row():
    teams[0] = team_a.get()
    teams[1] = team_b.get()
    players_team_a[0] = a1.get()
    players_team_b[0] = b1.get()
    players_team_a[1] = a2.get()
    players_team_b[1] = b2.get()
    players_team_a[2] = a3.get()
    players_team_b[2] = b3.get()
    players_team_a[3] = a4.get()
    players_team_b[3] = b4.get()
    players_team_a[4] = a5.get()
    players_team_b[4] = b5.get()

    # Clear the values
    team_a.delete(0, "end")
    team_a.insert(0, teams[0])
    team_b.delete(0, "end")
    team_b.insert(0, teams[1])

    a1.delete(0, "end")
    a1.insert(0, players_team_a[0])
    b1.delete(0, "end")
    b1.insert(0, players_team_b[0])

    a2.delete(0, "end")
    a2.insert(0, players_team_a[1])
    b2.delete(0, "end")
    b2.insert(0, players_team_b[1])

    a3.delete(0, "end")
    a3.insert(0, players_team_a[2])
    b3.delete(0, "end")
    b3.insert(0, players_team_b[2])

    a4.delete(0, "end")
    a4.insert(0, players_team_a[3])
    b4.delete(0, "end")
    b4.insert(0, players_team_b[3])

    a5.delete(0, "end")
    a5.insert(0, players_team_a[4])
    b5.delete(0, "end")
    b5.insert(0, players_team_b[4])

    # Update team and player dropdowns in the event section
    team_dropdown['values'] = teams
    update_player_dropdown(None)  # Update player list when teams are updated


# Function to dynamically update the player list based on selected team
def update_player_dropdown(event):
    selected_team = team_dropdown.get()
    if selected_team == teams[0]:
        player_dropdown['values'] = players_team_a
    elif selected_team == teams[1]:
        player_dropdown['values'] = players_team_b


# Function to update outcome dropdown based on selected event
def update_outcome(event):
    selected_event = event_dropdown.get()
    if selected_event == 'Pass':
        outcome_dropdown['values'] = ["Successful", "Unsuccessful"]
    elif selected_event == 'Shot':
        outcome_dropdown['values'] = ["Off Target", "Saved","Blocked", "Goal"]


# Function to store event data and reset the form, and update the treeview
def store_event_data():
    event_details = {
        'Team': team_dropdown.get(),
        'Player': player_dropdown.get(),
        'Event': event_dropdown.get(),
        'X Coordinate': x_coord_entry.get(),
        'Y Coordinate': y_coord_entry.get(),
        'Outcome': outcome_dropdown.get()
    }
    event_data.append(event_details)

    # Add the new event to the treeview
    treeview.insert('', tk.END, values=(
        event_details['Team'], event_details['Player'], event_details['Event'],
        event_details['X Coordinate'], event_details['Y Coordinate'], event_details['Outcome']
    ))

    # Clear the selected values
    team_dropdown.set('')
    player_dropdown.set('')
    event_dropdown.set('')
    x_coord_entry.delete(0, 'end')
    x_coord_entry.insert(0, '0')
    y_coord_entry.delete(0, 'end')
    y_coord_entry.insert(0, '0')
    outcome_dropdown.set('')


# Function to export data to CSV and show the result in the Tkinter app
def export_to_csv():
    if event_data:
        df = pd.DataFrame(event_data)
        df.to_csv('match_events.csv', index=False)
        export_message["text"] = "Data exported to match_events.csv"  # Show success message
    else:
        export_message["text"] = "No data to export"  # Show error message


# Function to delete a selected entry from the treeview and event_data
def delete_selected_entry():
    selected_item = treeview.selection()  # Get selected item in treeview
    if selected_item:
        # Find the index of the selected item and remove it from event_data
        item_index = treeview.index(selected_item[0])
        del event_data[item_index]

        # Remove the selected item from the treeview
        treeview.delete(selected_item[0])
        export_message["text"] = "Entry deleted."
    else:
        export_message["text"] = "No entry selected."


root = tk.Tk()

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack(fill='both', expand=True)

# Allow the main frame to expand with the window size
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure frame to expand with the window
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Team and player renaming section
widgets_frame = ttk.LabelFrame(frame, text="Team and Players")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

team_a = ttk.Entry(widgets_frame)
team_a.insert(0, teams[0])
team_a.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

team_b = ttk.Entry(widgets_frame)
team_b.insert(0, teams[1])
team_b.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

a1 = ttk.Entry(widgets_frame)
a1.insert(0, players_team_a[0])
a1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

b1 = ttk.Entry(widgets_frame)
b1.insert(0, players_team_b[0])
b1.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

a2 = ttk.Entry(widgets_frame)
a2.insert(0, players_team_a[1])
a2.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

b2 = ttk.Entry(widgets_frame)
b2.insert(0, players_team_b[1])
b2.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

a3 = ttk.Entry(widgets_frame)
a3.insert(0, players_team_a[2])
a3.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

b3 = ttk.Entry(widgets_frame)
b3.insert(0, players_team_b[2])
b3.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

a4 = ttk.Entry(widgets_frame)
a4.insert(0, players_team_a[3])
a4.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

b4 = ttk.Entry(widgets_frame)
b4.insert(0, players_team_b[3])
b4.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

a5 = ttk.Entry(widgets_frame)
a5.insert(0, players_team_a[4])
a5.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

b5 = ttk.Entry(widgets_frame)
b5.insert(0, players_team_b[4])
b5.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

update_button = ttk.Button(widgets_frame, text="Update Teams/Players", command=insert_row)
update_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

# Match event section
event_frame = ttk.LabelFrame(frame, text="Event Details")
event_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# Team Dropdown
ttk.Label(event_frame, text="Team").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
team_dropdown = ttk.Combobox(event_frame, values=teams, state="readonly")
team_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
team_dropdown.bind("<<ComboboxSelected>>", update_player_dropdown)

# Player Dropdown (updates dynamically)
ttk.Label(event_frame, text="Player").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
player_dropdown = ttk.Combobox(event_frame, state="readonly")
player_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Event Dropdown
ttk.Label(event_frame, text="Event").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
event_dropdown = ttk.Combobox(event_frame, values=["Shot", "Pass"], state="readonly")
event_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
event_dropdown.bind("<<ComboboxSelected>>", update_outcome)

# X Coordinate Entry (defaults to zero)
ttk.Label(event_frame, text="X Coordinate").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
x_coord_entry = ttk.Entry(event_frame)
x_coord_entry.insert(0, '0')
x_coord_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Y Coordinate Entry (defaults to zero)
ttk.Label(event_frame, text="Y Coordinate").grid(row=4, column=0, padx=5, pady=5, sticky="ew")
y_coord_entry = ttk.Entry(event_frame)
y_coord_entry.insert(0, '0')
y_coord_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

# Outcome Dropdown (updates dynamically)
ttk.Label(event_frame, text="Outcome").grid(row=5, column=0, padx=5, pady=5, sticky="ew")
outcome_dropdown = ttk.Combobox(event_frame, state="readonly")
outcome_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

# Button to store event data
store_button = ttk.Button(event_frame, text="Store Event", command=store_event_data)
store_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

# Treeview to display stored event data
treeFrame = ttk.LabelFrame(frame, text="Event Data")
treeFrame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

# Define the columns for the treeview
cols = ("Team", "Player", "Event", "X Coordinate", "Y Coordinate", "Outcome")
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)
for col in cols:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)
treeview.pack(fill="both", expand=True)
treeScroll.config(command=treeview.yview)

# Add Export and Delete buttons below the Treeview
button_frame = ttk.Frame(treeFrame)
button_frame.pack(fill="x", padx=5, pady=5)

export_button = ttk.Button(button_frame, text="Export to CSV", command=export_to_csv)
export_button.pack(side="left", padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete Selected Entry", command=delete_selected_entry)
delete_button.pack(side="left", padx=5, pady=5)

# Label to display export status message
export_message = ttk.Label(button_frame, text="")
export_message.pack(side="left", padx=5)

# Canvas for image and coordinate click handling
canvas_frame = ttk.LabelFrame(frame, text="Event Position")
canvas_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

canvas = tk.Canvas(canvas_frame, background="white", width=500, height=300)
canvas.grid(row=0, column=0, padx=5, pady=5)
image = Image.open("../rink.jpg")
resized_image = image.resize((505, 303))  # Slightly larger to cover canvas
img = ImageTk.PhotoImage(resized_image)

canvas.image = img  # Prevent garbage collection
canvas.create_image(0, 0, image=img, anchor='nw')

canvas.bind("<Button-1>", display_cordinate)
root.mainloop()
