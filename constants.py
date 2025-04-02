CLAIM_STATUS_CODE = {"approve": "Approved", "reject": "Rejected", "pending": "Pending"}
logged_in_username = ""
# premium_reducers = ""
# policies = []


def get_logged_in_username():
    return logged_in_username


# def get_premium_reducers():
#     return


# def get_policies():
#     return policies


def set_logged_in_username(username):
    global logged_in_username
    logged_in_username = username


# def set_policies(policy):
#     global policies
#     policies.append(policy)
