from collections import Counter
from modules import user, item

def recommend_for_existing(user_id):
    purchases = user.get_user_purchases(user_id)
    if not purchases:
        return []

    most_common = Counter(purchases).most_common(1)[0][0]
    all_items = item.list_items()
    recommendations = [i for i in all_items if i[2] == most_common]
    return recommendations

def recommend_for_new(tipo):
    all_items = item.list_items()
    recommendations = [i for i in all_items if i[2] == tipo]
    return recommendations
