from collections import defaultdict
import json

with open('data.json', 'r') as file:
    data = json.load(file)["records"]

active_users = defaultdict(set)
login_users = set()
temp = set()
login_times = {}



for item in data:
    hour = int(item['time'].split(' ')[1].split(':')[0])
    
    if item['type'] == 'Login':
        user_id = item["id"]
        login_time = item['time']
        temp.add(item["id"])
        if user_id not in login_times:
            login_times[user_id] = [login_time]
        else:
            login_times[user_id].append(login_time)
        active_users[hour].update(temp)
        login_users.add(item['id'])

    elif item['type'] == 'Logout':
        if item['id'] in login_users:
            if item["id"] in login_times:
              last_login_time_str = login_times[item["id"]][-1]
              last_login_hour = int(last_login_time_str.split(' ')[1].split(':')[0])
              for h in range(last_login_hour, hour+1):
                active_users[h].add(item["id"])
              del login_times[item["id"]]

            active_users[hour].update(temp)
            login_users.remove(item['id'])
            temp.remove(item["id"])
        else:
            # Handle user logging out without logging in
            for h in range(0, hour + 1):
                active_users[h].add(item['id'])

while login_times:
    user_id, login_times_list = login_times.popitem()
    last_login_time_str = login_times_list[-1]
    last_login_hour = int(last_login_time_str.split(' ')[1].split(':')[0])
    for h in range(last_login_hour, 24):
        active_users[h].add(user_id)

# To Generate the output
output = ''
for hour in range(24):
    if hour < 10:
        hour_range = f'0{hour}-{hour + 1}'
    else:
        hour_range = f'{hour}-{hour + 1}'
    
    user_list = sorted(active_users[hour])
    output += f'{hour_range} {user_list}\n' if user_list else f'{hour_range} \n'

print(output)
