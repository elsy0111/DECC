import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

def simulate_ball_motion(H, W, x_target, y_target, r, l, c, v0, dt=0.01, max_time=10):
    # Determine the equation of the inclined plane z = ax + by + d
    d = r
    b = (l - r) / H
    a = (c - r - b * (H / 2)) / W
    
    # Gravitational acceleration (standard value)
    g = 9.81
    
    # Calculate the acceleration components along the inclined plane
    normal_vector = np.array([-a, -b, 1]) / np.sqrt(a**2 + b**2 + 1)
    gravity = np.array([0, 0, -g])
    parallel_gravity = gravity - np.dot(gravity, normal_vector) * normal_vector
    
    # Acceleration in the x and y directions
    ax, ay = parallel_gravity[0], parallel_gravity[1]
    
    def simulate_trajectory(theta_value):
        """
        Simulate the trajectory for a given launch angle.
        """
        # Retrieve as a scalar value
        if hasattr(theta_value, "__len__"):
            theta = theta_value[0]
        else:
            theta = theta_value
            
        x0, y0 = 0, H / 2
        vx0 = v0 * np.cos(theta)
        vy0 = v0 * np.sin(theta)
        
        times = np.arange(0, max_time, dt)
        x_positions = []
        y_positions = []
        z_positions = []
        
        x, y = x0, y0
        vx, vy = vx0, vy0
        
        for _ in times:
            x_positions.append(x)
            y_positions.append(y)
            # Calculate the z-coordinate corresponding to the point on the plane
            z = a * x + b * y + d
            z_positions.append(z)
            
            # Update velocity
            vx += ax * dt
            vy += ay * dt
            
            # Update position
            x += vx * dt
            y += vy * dt
            
            # Terminate if the ball goes out of the plane's boundaries
            if x < 0 or x > W or y < 0 or y > H:
                break
        
        return np.array(x_positions), np.array(y_positions), np.array(z_positions)
    
    def objective_function(theta):
        """
        Objective function to minimize the distance to the target point.
        """
        x_pos, y_pos, _ = simulate_trajectory(theta)
        if len(x_pos) == 0:
            return float('inf')
        
        # Calculate the distance between each position and the target point
        distances = np.sqrt((x_pos - x_target)**2 + (y_pos - y_target)**2)
        
        # Return the minimum distance
        return np.min(distances)
    
    # Initial estimate (solution for a horizontal case)
    initial_theta = np.arctan2(y_target - H/2, x_target)
    
    # Optimization (restrict angle range: -pi/4 to +pi/4)
    bounds = [(-np.pi/4, np.pi/4)]
    result = minimize(objective_function, [initial_theta], bounds=bounds, method='L-BFGS-B')
    optimal_theta = result.x[0]
    
    # Calculate the optimal trajectory
    x_traj, y_traj, z_traj = simulate_trajectory(optimal_theta)
    trajectory = (x_traj, y_traj, z_traj)
    
    return optimal_theta, trajectory

def plot_results(H, W, x_target, y_target, r, l, c, optimal_theta, trajectory, hole):
    """
    Plot the results.
    """
    x_traj, y_traj, z_traj = trajectory
    
    # 2D plot (top view)
    plt.figure(figsize=(10, 8))
    
    # Add grid to 2D plot
    grid_size = 10  # Grid spacing
    for i in range(0, int(W) + 1, grid_size):
        plt.plot([i, i], [0, H], 'k:', alpha=0.3)
    for j in range(0, int(H) + 1, grid_size):
        plt.plot([0, W], [j, j], 'k:', alpha=0.3)
        
    for hole_x, hole_y in hole:
        plt.plot(hole_x, hole_y, 'ro', markersize=10, label=f'Hole ({hole_x}, {hole_y})')
    
    plt.plot(x_traj, y_traj, 'r-', linewidth=2)
    plt.plot(0, H/2, 'go', markersize=10, label='Start Point (0, H/2)')
    plt.plot(x_target, y_target, 'bo', markersize=10, label='Target Point')
    plt.plot([0, 0, W, 0], [0, H, H/2, 0], 'k--', linewidth=1)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Top View θ = {np.degrees(optimal_theta):.2f}°')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    
    # 3D plot (inclined plane and trajectory)
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw the inclined plane
    X = np.linspace(0, W, 20)
    Y = np.linspace(0, H, 20)
    X, Y = np.meshgrid(X, Y)
    
    # Plane equation z = ax + by + d
    d = r
    b = (l - r) / H
    a = (c - r - b * (H / 2)) / W
    Z = a * X + b * Y + d
    
    # Plot the surface with a grid
    ax.plot_surface(X, Y, Z, alpha=0.5, color='cyan', edgecolor='gray', linewidth=0.1)
    
    # Add grid lines on the plane
    grid_size = 10  # Grid spacing
    
    # X grid lines
    for i in range(0, int(W) + 1, grid_size):
        y_line = np.linspace(0, H, 100)
        x_line = np.ones_like(y_line) * i
        z_line = a * x_line + b * y_line + d
        ax.plot(x_line, y_line, z_line, 'k-', alpha=0.3)
    
    # Y grid lines
    for j in range(0, int(H) + 1, grid_size):
        x_line = np.linspace(0, W, 100)
        y_line = np.ones_like(x_line) * j
        z_line = a * x_line + b * y_line + d
        ax.plot(x_line, y_line, z_line, 'k-', alpha=0.3)
    
    # Draw the trajectory
    ax.plot(x_traj, y_traj, z_traj, 'r-', linewidth=3, label='Ball Trajectory')
    ax.scatter(0, H/2, a*0 + b*(H/2) + d, color='green', s=100, label='Start Point')
    ax.scatter(x_target, y_target, a*x_target + b*y_target + d, color='blue', s=100, label='Target Point')
    
    # Plot the corners of the 3D plane
    ax.scatter(0, 0, r, color='red', s=50, label=f'R(0,0,{r})')
    ax.scatter(0, H, l, color='purple', s=50, label=f'L(0,H,{l})')
    ax.scatter(W, H/2, c, color='brown', s=50, label=f'C(W,H/2,{c})')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D View θ = {np.degrees(optimal_theta):.2f}°')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

# Main execution function
def main():
    hole = [(80, 50), (100, 50), (120, 50), (140, 50)]

    # Parameter settings
    H = 800  # Height of the plane
    W = 120  # Width of the plane
    
    # Target point
    x_target = 80
    y_target = 50
    
    # Heights at three points
    r = 0    # Height at R(0, 0)
    l = 20   # Height at L(0, H)
    c = 10   # Height at C(W, H/2)
    
    # Initial velocity
    v0 = 15
    
    # Calculate the optimal launch angle and trajectory
    optimal_theta, trajectory = simulate_ball_motion(H, W, x_target, y_target, r, l, c, v0)
    
    # Display the results
    print(f"Target Point: ({x_target}, {y_target})")
    print(f"Optimal Theta: {np.degrees(optimal_theta):.2f} degrees")
    
    # Plot the results
    plot_results(H, W, x_target, y_target, r, l, c, optimal_theta, trajectory, hole)

if __name__ == "__main__":
    main()