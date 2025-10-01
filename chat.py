import time, vk, json

with open("config.json", 'r') as f:
  config = json.load(f)

chat_id = config['chat']['id']
vk_api = vk.API(access_token=config['access_token'], v="5.92", lang="ru")

banned = 0
limit = config['chat']['limit']
sleep = config['chat']['sleep']
block_ids = []

with open('src/welcome.txt', 'r') as f:
  print(f.read())

users = vk_api.messages.getChatUsers(chat_id=chat_id,fields="about")
  
print("ID чата:", chat_id)
print("Кол-во участников:", len(users))

for user_info in users:
  user_id = user_info['id']

  if "deactivated" in user_info.keys() and user_info['deactivated'] == "banned":
    block_ids.append(user_id)
    print("Найдено собачек:", len(block_ids), end="\r")
    time.sleep(0.01)

print("")
print("Начинаю удаление...")
for user_id in block_ids:
  if limit > banned:
    vk_api.messages.removeChatUser(chat_id=chat_id, user_id=user_id)
    banned = banned + 1
    print("Удалено собачек: {} из {}".format(banned, (len(block_ids) if limit > len(block_ids) else limit)), end="\r")
    time.sleep(sleep)
    
print("")
print("Завершено!")
