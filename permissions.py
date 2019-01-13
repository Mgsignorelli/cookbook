from flask_login import current_user

anon_routes = [
    "index",
    "login",
    "send_assets",
    "send_images",
    "recipe_show",
    "recipe_index",
    "user_create",
    "user_store",
]

logged_in_routes = [
    "logout",
    "allergy_create",
    "allergy_store"
    "category_create",
    "category_store",
    "recipe_create",
    "recipe_store",
    "recipe_vote",
    "ingredient_create",
    "ingredient",
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