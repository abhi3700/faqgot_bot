import json

item_dict = dict(stats= json.dumps(dict(correct_count= 0)))
print(item_dict)
print(item_dict.get('stats'))
print(json.loads(item_dict['stats']).get('correct_count'))