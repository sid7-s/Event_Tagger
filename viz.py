import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd

# The team that is attacking from left to right in the first half
right_attacking_team = "Great Britain"

# Load the CSV file with the match events
first_half = 'match_events_1.csv'# Replace with your CSV file path
df1 = pd.read_csv(first_half)
df1.loc[df1['Team'] != right_attacking_team, 'X Coordinate'] = 100 - df1["X Coordinate"]
df1.loc[df1['Team'] != right_attacking_team, 'Y Coordinate'] = 60 - df1["Y Coordinate"]

second_half = 'match_events_2.csv'# Replace with your CSV file path
df2 = pd.read_csv(second_half)
df2.loc[df2['Team'] == right_attacking_team, 'X Coordinate'] = 100 - df2["X Coordinate"]
df2.loc[df2['Team'] == right_attacking_team, 'Y Coordinate'] = 60 - df2["Y Coordinate"]

events_df = pd.concat([df1,df2])



# Load the rink image
rink_image_path = '../rink_viz.jpg'  # Replace with your rink image path
rink_image = Image.open(rink_image_path)


def visualize_shots_by_outcome_with_unfilled_shapes_and_label(team_name, event):
    """
    Visualize shots for the given team with unfilled shapes for each shot outcome.
    - Unfilled circle for goals.
    - Unfilled triangle for blocked shots.
    - X for saved shots (basic X shape).
    - Unfilled square for off-target shots.
    Also add a legend for the markers in the top-left corner.
    """
    team_events = events_df[events_df['Team'] == team_name]

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Display the rink image
    ax.imshow(rink_image, extent=[0, 100, 60, 0])

    # Plot the shots with different unfilled shapes based on outcome
    for i, row in team_events.iterrows():
        if row['Event'] == 'Shot':
            x = row['X Coordinate']
            y = row['Y Coordinate']
            outcome = row['Outcome']

            # Determine marker type based on outcome
            if outcome == 'Goal':
                marker = 'o'  # Unfilled circle
                color = 'green'
                facecolor = 'none'  # No fill
                label = 'Goal'
            elif outcome == 'Blocked':
                marker = '^'  # Unfilled Triangle
                color = 'black'
                facecolor = 'none'  # No fill
                label = 'Blocked'
            elif outcome == 'Saved':
                marker = 'x'  # X (basic X shape)
                color = 'red'
                facecolor = color
                label = 'Saved'
            elif outcome == 'Off Target':
                marker = 's'  # Unfilled square
                color = 'blue'
                facecolor = 'none'  # No fill
                label = 'Off Target'

            ax.scatter(x, y, color=color, marker=marker, s=100, edgecolors=color, facecolors=facecolor, linewidth=1.5,
                       label=label)

    # Remove axes, labels, and tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set the title dynamically based on the event
    ax.set_title(f'{team_name}: {event}', pad=20)

    # Add a legend in the top-left corner
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left')

    # Show the plot
    plt.show()


def visualize_passes_leading_to_shots_with_legend(team_name, event):
    """
    Visualize passes that led to shots for the given team.
    Green arrows indicate passes that led to goals, and red arrows indicate other shots.
    Adds a legend for the colors.
    """
    team_events = events_df[events_df['Team'] == team_name]

    # Initialize lists to hold pass and shot pairs
    current_pass = None

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Display the rink image
    ax.imshow(rink_image, extent=[0, 100, 60, 0])

    # Iterate through the events in order
    for i, row in team_events.iterrows():
        event_type = row['Event']

        # If it's a pass, store it temporarily
        if event_type == 'Pass':
            current_pass = (row['X Coordinate'], row['Y Coordinate'])

        # If it's a shot after a pass, store the pass-shot pair
        if event_type == 'Shot' and current_pass:
            shot_coords = (row['X Coordinate'], row['Y Coordinate'])
            color = 'green' if row['Outcome'] == 'Goal' else 'red'
            ax.annotate('', xy=shot_coords, xytext=current_pass,
                        arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle='->', lw=2))
            current_pass = None  # Reset after shot

    # Remove axes, labels, and tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set the title dynamically based on the event
    ax.set_title(f'{team_name}: {event}', pad=20)

    # Add a legend
    green_patch = plt.Line2D([0], [0], color='green', lw=2, label='Pass leading to Goal')
    red_patch = plt.Line2D([0], [0], color='red', lw=2, label='Pass leading to Other Shots')

    # Show the legend in the top-left corner
    ax.legend(handles=[green_patch, red_patch], loc='upper left')

    # Show the plot
    plt.show()


# Example usage:
# To visualize shots by outcome for Great Britain
visualize_shots_by_outcome_with_unfilled_shapes_and_label('Austria', 'Shots')

# To visualize passes leading to shots for Great Britain
visualize_passes_leading_to_shots_with_legend('Austria', 'Passes Leading to Shots')