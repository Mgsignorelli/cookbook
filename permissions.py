from flask_login import current_user

anon_routes = [
    "index",
    "login",
    "register",
    "send_assets",
    "send_images",
    "recipe_show",
]

logged_in_routes = [
    "index",
    "send_assets",
    "send_images",
    "logout",
    "recipe_show",
]


def can(permission):
    if current_user.is_anonymous:
        if permission in anon_routes:
            return True
        return False

    if current_user.is_admin:
        return True

    if permission in logged_in_routes:
        return True

    return False