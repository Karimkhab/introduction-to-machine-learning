def get_dominant_eigenvalue_and_eigenvector(data, num_steps):
    """
    data: np.ndarray – symmetric diagonalizable real-valued matrix
    num_steps: int – number of power method steps

    Returns:
    eigenvalue: float – dominant eigenvalue estimation after `num_steps` steps
    eigenvector: np.ndarray – corresponding eigenvector estimation
    """
    r = np.random.random((data.shape[0], 1))

    for step in range(num_steps):
        v = data.dot(r)
        r = v / np.linalg.norm(v)

    eigenvalue = r.T.dot(data.dot(r)) / r.T.dot(r)
    return float(eigenvalue), r.squeeze()