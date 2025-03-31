CLAIM_STATUS_CODE = {"approve": "Approved", "reject": "Rejected", "pending": "Pending"}
logged_in_username = ""


def get_logged_in_username():
    return logged_in_username


def set_logged_in_username(username):
    global logged_in_username
    logged_in_username = username
