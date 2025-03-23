import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Figure size setting - adjusted to match original aspect ratio
fig, ax = plt.subplots(figsize=(8, 12))

# Set background color for the entire figure
fig.patch.set_facecolor('#333333')

# Add title and bottom bars
title_bar = patches.Rectangle((0, 1000), 800, 60, facecolor='#333333', alpha=1.0)
ax.add_patch(title_bar)
bottom_bar = patches.Rectangle((0, -60), 800, 60, facecolor='#333333', alpha=1.0)
ax.add_patch(bottom_bar)

# Main gray rectangle background (1000mm height)
main_table = patches.Rectangle((0, 260), 800, 740, facecolor='gray', alpha=0.7)
ax.add_patch(main_table)

# White bottom section (260mm height)
bottom_section = patches.Rectangle((0, 0), 800, 260, facecolor='white', edgecolor='gray', alpha=0.7)
ax.add_patch(bottom_section)

# Middle dividing line
ax.plot([400, 400], [0, 1000], color='black', alpha=0.3, linewidth=1)

# θ axis (rotation) circle
theta_circle = plt.Circle((400, 260), 50, color='orange', alpha=0.7)
ax.add_patch(theta_circle)
# Inner circles for θ axis
for i in range(6):
    angle = i * 2 * np.pi / 6
    r = 30
    x = 400 + r * np.cos(angle)
    y = 260 + r * np.sin(angle)
    inner_circle = plt.Circle((x, y), 10, color='red', alpha=0.7, fill=False)
    ax.add_patch(inner_circle)

# Yellow dots - updated to 50mm diameter (25mm radius) with numbers
yellow_dots = [(600, 800), (500, 650), (600, 500), (500, 350), (400, 650), (300, 650), (200, 500)]
for i, (x, y) in enumerate(yellow_dots):
    yellow_circle = plt.Circle((x, y), 25, color='orange', alpha=0.7)
    ax.add_patch(yellow_circle)
    yellow_inner = plt.Circle((x, y), 20, color='yellow', alpha=0.7)
    ax.add_patch(yellow_inner)
    # Add target numbers
    ax.text(x, y, f'{i+1}', color='black', ha='center', va='center', fontsize=14, fontweight='bold')

# Rotation axes - updated to 200mm diameter (100mm radius)
# Define rod length
rod_length = 200

# α axis
alpha_circle = plt.Circle((600, 500), 50, color='orange', alpha=0.7)
ax.add_patch(alpha_circle)
ax.plot([600-rod_length/2, 600+rod_length/2], [500, 500], color='orange', linewidth=10)
ax.text(600, 435, 'α axis (rotation)', color='white', ha='center', va='center', fontsize=10)

# β axis
beta_circle = plt.Circle((400, 500), 50, color='orange', alpha=0.7)
ax.add_patch(beta_circle)
ax.plot([400-rod_length/2, 400+rod_length/2], [500, 500], color='orange', linewidth=10)
ax.text(400, 435, 'β axis (rotation)', color='white', ha='center', va='center', fontsize=10)

# γ axis
gamma_circle = plt.Circle((400, 800), 50, color='orange', alpha=0.7)
ax.add_patch(gamma_circle)
ax.plot([400-rod_length/2, 400+rod_length/2], [800, 800], color='orange', linewidth=10)
ax.text(400, 735, 'γ axis (rotation)', color='white', ha='center', va='center', fontsize=10)

# δ axis
delta_circle = plt.Circle((200, 800), 50, color='orange', alpha=0.7)
ax.add_patch(delta_circle)
ax.plot([200-rod_length/2, 200+rod_length/2], [800, 800], color='orange', linewidth=10)
ax.text(200, 735, 'δ axis (rotation)', color='white', ha='center', va='center', fontsize=10)

# L, R, C axes
l_axis = plt.Circle((0, 1000), 25, color='black', alpha=0.9)
ax.add_patch(l_axis)
ax.add_patch(plt.Circle((0, 1000), 10, color='gray', alpha=0.7))

r_axis = plt.Circle((800, 1000), 25, color='black', alpha=0.9)
ax.add_patch(r_axis)
ax.add_patch(plt.Circle((800, 1000), 10, color='gray', alpha=0.7))

c_axis = plt.Circle((400, 0), 25, color='black', alpha=0.9)
ax.add_patch(c_axis)
ax.add_patch(plt.Circle((400, 0), 10, color='gray', alpha=0.7))

# Table origin label
ax.text(500, 400, 'Table (0,0)', color='white', ha='left', va='center', fontsize=10)
ax.arrow(500, 390, -100, -40, head_width=15, head_length=15, fc='white', ec='white')

# Axis labels
ax.text(-40, 1000, 'L axis (up/down)', fontsize=10, ha='center')
ax.text(840, 1000, 'R axis (up/down)', fontsize=10, ha='center')
ax.text(400, -40, 'C axis (up/down)', fontsize=10, ha='center')

# θ axis label
ax.text(400, 190, 'θ axis (rotation)', color='white', ha='center', va='center', fontsize=10)

# Border for the entire diagram
ax.plot([0, 800, 800, 0, 0], [0, 0, 1000, 1000, 0], color='gray', linewidth=1)

# Graph settings
ax.set_xlim(-100, 900)
ax.set_ylim(-100, 1100)
ax.set_aspect('equal')
ax.axis('off')

# Title at bottom
ax.text(400, -40, 'Figure A (Top View)', fontsize=12, ha='center', color='white')

plt.tight_layout()
plt.show()