import time, vk, json

with open("config.json", 'r') as f:
  config = json.load(f)

user_id = config['profile']['id']
session = vk.Session(access_token=config['access_token'])
vk_api = vk.API(session, v="5.92", lang="ru")

banned = 0
limit = config['profile']['limit']
sleep = config['profile']['sleep']
block_ids = []

with open('src/welcome.txt', 'r') as f:
  print(f.read())
  
print("ID профиля:", user_id)
print("Кол-во подписчиков:", vk_api.users.getFollowers(user_id=user_id, count=1)['count'])

def activate (offset=0):
  global banned, limit, sleep
  followers = vk_api.users.getFollowers(user_id=user_id, offset=offset, count=1000,fields="about")

  follows_count = followers['count']

  for follow_info in followers['items']:
    follow_id = follow_info['id']
    
    if "deactivated" in follow_info.keys() and follow_info['deactivated'] == "banned" and limit > 0:
      block_ids.append(follow_id)
      print("Найдено собачек:", len(block_ids), end="\r")
      time.sleep(0.01)

  if (follows_count > offset):
    activate(offset=(offset + 1000))

activate(0)

print("")
print("Начинаю удаление...")
for user_id in block_ids:
  if limit > banned:
    vk_api.account.ban(owner_id=user_id)
    banned = banned + 1
    print("Удалено собачек: {} из {}".format(banned, (len(block_ids) if limit > len(block_ids) else limit)), end="\r")
    time.sleep(sleep)
    
print("")
print("Завершено!")