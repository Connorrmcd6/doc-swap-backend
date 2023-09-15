import numpy as np
import pandas as pd
import random


def assign_users(n_locations, post_available, assignment_ids):
    while True:
        assignment = np.random.randint(0, n_locations)
        if post_available[assignment] > 0:
            assignment_ids.append(assignment)
            post_available[assignment] -= 1
            return assignment_ids

def generator(n_users, n_choices, location_df_path):

    province_data = {
        "province_name": ["GP", "WC", "NC", "EC", "KZN", "LP", "MP", "NW", "FS"],
        "province_id": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }

    provinces = pd.DataFrame(province_data)

    location_df = pd.read_csv(location_df_path)
    location_df = location_df.merge(provinces, on='province_name', how='left')
    location_df.index.names = ['hospital_id']

    user_ids = list(np.arange(1, n_users+1))
    post_available = list(location_df.number_of_posts_available)
    n_locations = len(list(location_df.index))
    assignment_ids = []
    user_choices = []
    choice_weights = []

    '''Generate initial assignments for each user with a cap on number of students assigned to the same place'''
    for i in user_ids:
        assign_users(n_locations, post_available, assignment_ids)

    '''Generate n_choices for each user with a weighting for each choice'''
    for i in range(n_users):
        l = list(location_df.index)
        remove_assignment = l.pop(assignment_ids[i])
        choices = []
        weights = []
        w = 1
        for j in range(n_choices):
            random_choice = l.pop(random.randrange(len(l)))
            choices.append(random_choice)
            weights.append(w)
            w = w + 1

        user_choices.append(choices)
        choice_weights.append(weights)

    data = {
        "user_id": [],
        "assignment_id": [],
        "choice_id": [],
        "choice_weight": [],
    }

    for i in range(n_users):
        for j in range(n_choices):
            data["user_id"].append(user_ids[i])
            data["assignment_id"].append(assignment_ids[i])
            data["choice_id"].append(user_choices[i][j])
            data["choice_weight"].append(choice_weights[i][j])

    edge_list = pd.DataFrame(data)
    edge_list.index.names = ['edge_id']

    return edge_list
