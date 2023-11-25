import numpy as np

def average_indices(prob_threshold, closeness_threshold, data):
    """
    Averages indices that are close to each other based on a closeness threshold.

    
    :param prob_threshold: The threshold for selecting initial indices.
    :param closeness_threshold: Maximum gap between indices to consider them part of the same group.
    :data: The array on which the operation is performed.
    :return: List of averaged indices.
    """
    Pcp_sum = np.exp(data).sum(0)
    above_threshold_indices = np.where(Pcp_sum > prob_threshold)[0]

    groups = []
    current_group = []

    for index in above_threshold_indices:
        if not current_group or index - current_group[-1] <= closeness_threshold:
            current_group.append(index)
        else:
            groups.append(current_group)
            current_group = [index]

    if current_group:
        groups.append(current_group)

    averaged_indices = [int(round(sum(group) / len(group))) for group in groups]

    return averaged_indices

