import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc


def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def make_scatter_plot(player_data, player_id):
    sns.set(style="white", color_codes=True)

    made_df = player_data[player_data['SHOT_MADE_FLAG'] == 1]
    miss_df = player_data[player_data['SHOT_MADE_FLAG'] == 0]
    joint_shot_chart = sns.jointplot(made_df['LOC_X'], made_df['LOC_Y'], stat_func=None,
                                     kind='scatter', space=0, alpha=0.5)

    joint_shot_chart.ax_joint.scatter(miss_df['LOC_X'], miss_df['LOC_Y'], marker='x', c='coral')

    joint_shot_chart.fig.set_size_inches(12, 11)

    ax = joint_shot_chart.ax_joint
    draw_court(ax)

    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    path = f'{player_id}-scatter.png'
    plt.savefig(path)
    return path


def make_hexbin_plot(player_data, player_id):
    plt.figure(figsize=(12, 11))

    made_df = player_data[player_data['SHOT_MADE_FLAG'] == 1]

    plt.hexbin(made_df['LOC_X'], made_df['LOC_Y'], gridsize=6, C=None, bins=None, mincnt=1, cmap=plt.cm.OrRd)
    draw_court()
    plt.xlim(-250, 250)
    plt.ylim(422.5, -47.5)
    path = f'{player_id}-hexbin.png'
    plt.savefig(path)
    return path
