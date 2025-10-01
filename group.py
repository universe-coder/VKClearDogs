import time, vk, json, requests

with open("config.json", 'r') as f:
  config = json.load(f)

group_id = config['group']['id']
vk_api = vk.API(access_token=config['access_token'], v="5.92", lang="ru")

def remove_user_with_retry(user_id, max_retries=3):
    """Remove user with retry logic for network errors"""
    for attempt in range(max_retries):
        try:
            vk_api.groups.removeUser(group_id=group_id, user_id=user_id)
            return True
        except (vk.exceptions.VkAPIError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                print("Ошибка сети, повтор через 5 сек... (попытка {}/{})".format(attempt + 1, max_retries), end='\r')
                time.sleep(5)  # Wait 5 seconds before retry
            else:
                print("Не удалось удалить пользователя {} после {} попыток: {}".format(user_id, max_retries, e), end='\r')
                return False
    return False

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
    if remove_user_with_retry(user_id):
      banned = banned + 1
      print("Удалено собачек {} из {}".format(banned, (len(block_ids) if limit > len(block_ids) else limit)),  end='\r')
    time.sleep(sleep)

print("")
print("Завершено!")