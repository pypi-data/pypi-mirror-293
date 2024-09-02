import numpy as np

def binary_string_to_array(binary_string):
    """
    Convert a binary string to an array of integers.

    Parameters:
    binary_string (str): The binary string.

    Returns:
    list of int: The converted array of integers.
    """
    return [int(bit) for bit in binary_string]

def normalize_counts(counts):
    """
    Normalize the counts of quantum state measurement results.

    Parameters:
    counts (dict): The counts of quantum state measurement results.

    Returns:
    dict: The normalized counts.
    """
    total = sum(counts.values())
    return {state: count / total for state, count in counts.items()}

def log_message(message, level="INFO"):
    """
    Print a log message.

    Parameters:
    message (str): The log message.
    level (str): The log level, default is "INFO".
    """
    print(f"[{level}] {message}")

def apply_activation_function(data, function="sigmoid"):
    """
    Apply an activation function.

    Parameters:
    data (array-like): The input data.
    function (str): The type of activation function, default is "sigmoid".

    Returns:
    array-like: The data after applying the activation function.
    """
    if function == "sigmoid":
        return 1 / (1 + np.exp(-data))
    elif function == "tanh":
        return np.tanh(data)
    elif function == "relu":
        return np.maximum(0, data)
    else:
        raise ValueError(f"Unsupported activation function: {function}")
