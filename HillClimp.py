import numpy as np

# Define the objective function (for example: maximize f(x) = -x^2 + 5)
def objective(x):
    return -x[0] ** 2 + 5

# Generate neighboring solutions
def generate_neighbors(x, step_size=0.1):
    return [np.array([x[0] + step_size]), np.array([x[0] - step_size])]

# Hill Climbing Algorithm
def hill_climbing(objective, initial, n_iterations=100, step_size=0.1):
    current = np.array([initial])
    current_eval = objective(current)
    for i in range(n_iterations):
        neighbors = generate_neighbors(current, step_size)
        neighbor_evals = [objective(n) for n in neighbors]
        best_idx = np.argmax(neighbor_evals)
        if neighbor_evals[best_idx] > current_eval:
            current = neighbors[best_idx]
            current_eval = neighbor_evals[best_idx]
            print(f"Step {i+1}: x = {current[0]:.4f}, f(x) = {current_eval:.4f}")
        else:
            print("No better neighbors found. Algorithm converged.")
            break
    return current, current_eval

# Example usage
final_position, final_value = hill_climbing(objective, initial=2.0)
print("Best solution:", final_position, "Optimal value:", final_value)
