import time, vk, json

with open("config.json", 'r') as f:
  config = json.load(f)

group_id = config['group']['id']
session = vk.Session(access_token=config['access_token'])
vk_api = vk.API(session, v="5.92", lang="ru")

banned = 0
limit = config['group']['limit']
sleep = config['group']['sleep']
block_ids = []

with open('src/welcome.txt', 'r') as f:
  print(f.read())
  
print("ID группы:", group_id)
print("Кол-во участников:", vk_api.groups.getMembers(group_id=group_id, count=1)['count'])

def activate (offset=0):
  global block_ids
  followers = vk_api.groups.getMembers(group_id=group_id, offset=offset, count=1000)

  follows_count = followers['count']
  
  users = vk_api.users.get(user_ids=followers['items'], fields="deactivated")

  for follow_info in users:
    follow_id = follow_info['id']
    
    if "deactivated" in follow_info.keys() and follow_info['deactivated'] == "banned":
      block_ids.append(follow_id)
      print("Найдено собачек:", len(block_ids), end='\r')
      time.sleep(0.01)

  if (follows_count > offset):
    activate(offset=(offset + 1000))


activate(0)

print("")
print("Начинаю удаление...")
for user_id in block_ids:
  if limit > banned:
    vk_api.groups.removeUser(group_id=group_id, user_id=user_id)
    banned = banned + 1
    print("Удалено собачек {} из {}".format(banned, (len(block_ids) if limit > len(block_ids) else limit)),  end='\r')
    time.sleep(sleep)

print("")
print("Завершено!")