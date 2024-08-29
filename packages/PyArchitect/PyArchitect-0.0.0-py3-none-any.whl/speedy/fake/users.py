import numpy as np

def generate_user_id(max_users: int):
    """
    Generates a user_id based on a Pareto distribution.
    80% of the rows will be assigned to 20% of the users.

    Returns:
    int: A user_id.
    """
    # Pareto distribution parameters
    shape, mode = 1.16, 1

    # Generate a random number from the Pareto distribution
    pareto_num = (np.random.pareto(shape) + 1) * mode

    # Scale the number to the range of user_ids
    user_id = int(pareto_num * max_users / (mode + shape))

    # Ensure the user_id is within the valid range
    user_id = max(min(user_id, max_users), 1)

    return user_id


def generate_user_id_normal(max_users: int):
    """
    Generates a user_id based on a normal distribution.
    The majority of the user_ids will be around the mean.

    Returns:
    int: A user_id.
    """
    # Normal distribution parameters
    mean, std_dev = 0, 0.1

    # Generate a random number from the normal distribution
    normal_num = np.random.normal(mean, std_dev) + 0.5

    # Ensure the user_id is within the valid range
    user_id = int(normal_num * max_users)
    if normal_num <= 0 : 
        user_id = 1

    return user_id
