import requests
import json
import conversation
import posts
import subscriptions
import comments

# Метод для пересказа диалога
def get_vk_chat_history(peer_id, access_token):
    # URL и параметры строки запроса
    url = "https://api.vk.com/method/messages.getHistory"
    query_params = {
        "v": "5.246",
        "client_id": "6287487"
    }

    # Данные для тела запроса 
    form_data = {
        "peer_id": peer_id, # Идентификатор чата
        "start_cmid": 339782,
        "count": 32,
        "offset": -1,
        "extended": 1,
        "group_id": 0,
        "fwd_extended": 1,
        "fields": "id,first_name,last_name",
        "access_token": access_token # Токен доступа
    }

    # Заголовки из запроса
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://vk.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            url,
            params=query_params,
            data=form_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе для peer_id {peer_id}: {str(e)}")
        return None

# Метод для получения постов, которые вызвали наибольшую реакцию
def get_vk_post_reactions(domain, access_token): 
    # URL и параметры строки запроса 
    url = "https://api.vk.com/method/wall.get" 
 
    # Данные для тела запроса  
    form_data = { 
        "domain": domain, #Короткий адрес пользователя или сообщества. 
        "offset": 0, 
        "count": 32, 
        "filter": "all", 
        "extended": 0, 
        "fields": "id,owner_id,date,comments,likes,reposts,views", 
        "access_token": access_token, 
        "v": "5.251", 
    } 
 
    # Заголовки из запроса 
    headers = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0", 
        "Referer": "https://vk.com/", 
        "Content-Type": "application/x-www-form-urlencoded" 
    } 
 
    try: 
        response = requests.post( 
            url, 
            data=form_data, 
            headers=headers 
        ) 
        response.raise_for_status() 
        return response.json() 
    except Exception as e: 
        print(f"Ошибка при запросе для domain {domain}: {str(e)}") 
        return None

# Метод для описания личности пользователя по его подпискам на сообщества
def get_vk_subscriptions(user_id, access_token):
    # URL и параметры строки запроса
    url = "https://api.vk.com/method/groups.get"

    # Данные для тела запроса 
    form_data = {
        "v": "5.199",
        "user_id": user_id, #Идентификатор пользователя, информацию о сообществах которого требуется получить.
        "count": 10,
        "extended": 1,
        "offset": 0,
        "filter": "groups",
        "fields": "description,members_count,name",
        "access_token": access_token
    }

    # Заголовки из запроса
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://vk.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            url,
            data=form_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе для user_id {user_id}: {str(e)}")
        return None

# Метод для получения часто задаваемых вопросов под конкретным постом
def get_vk_q_and_a(owner_id, post_id, access_token):
    # URL и параметры строки запроса
    url = "https://api.vk.com/method/wall.getComments"
    # Данные для тела запроса 
    form_data = {
        "owner_id": owner_id, #Идентификатор владельца страницы (пользователь или сообщество).
        "post_id": post_id, #Идентификатор записи на стене.
        "count": 100,
        "extended": 1,
        "need_likes": 1, 
        "sort": "desc",
        "fields": "name",
        "access_token": access_token,
        "v": "5.199",
    }

    # Заголовки из запроса
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://vk.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            url,
            data=form_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе для owner_id {owner_id}: {str(e)}")
        return None

        
# Пример использования

#токен вк(можно найти открыв код страницы с диалогом в браузере->network->ищем access_token в самом низу)
ACCESS_TOKEN = "vk1.a.x5HUSXcVkvJDkN6ziv0uXAsv9IamhlBf-31Q4_olB6mmDmp1ErXXLPEir4XrDVXf4GFO_lHqfPwtgmC3QkWWRPwmVxF_0fLyAy__Bt0B2FqGr0S45WXsFQxq5nvpb4pvGMiXxTOplYbIhSojaOJ6SnsnM9JknBdM1bpZMzUak6FB0CGkvMqyY-FwpPxk8d-lzfFKpP_Ym3OXG7Cmd7gTtA"  
#айди диалога(можно найти открыв код страницы с диалогом в браузере->network->ищем peer_id)
CHAT_ID = 567023851 
USER_ID = 270365181
POST_ID = 3836


char = input('Выберите method: ')
if(char == '1'):
    # пересказ диалога
    chat = None
    result = get_vk_chat_history(CHAT_ID, ACCESS_TOKEN)
    print(result)

    chat = conversation.parse_vk_messages(result)
    prompt = None
    print(chat)

    if chat:
        prompt = conversation.conversation_to_prompt(chat, "Перескажи данный диалог?")

    print(prompt)
elif(char == '2'):
    # обсуждения
    chat = None
    result = get_vk_chat_history(CHAT_ID, ACCESS_TOKEN)
    print(result)

    chat = conversation.parse_vk_messages(result)
    prompt = None
    print(chat)

    if chat:
        prompt = conversation.conversation_to_prompt(chat, "Какие темы у моих друзей вызывают самые яркие дисскусии?")

    print(prompt)
elif(char == '3'):
    # популярные посты
    postList = None 
    result = get_vk_post_reactions(USER_ID, ACCESS_TOKEN) 
    print(result) 
    
    postList = posts.parse_vk_posts(result) 
    prompt = None 
    print(postList) 
    
    if postList: 
        prompt = posts.posts_to_prompt(postList, "Проанализируй посты и реакцию на них. Какие посты получают больше реакций и почему?") 
    
    print(prompt)
elif(char == '4'):
    # описание по подпискам
    subs = None
    result = get_vk_subscriptions(USER_ID, ACCESS_TOKEN)
    print(result)

    subs = subscriptions.parse_vk_subscriptions(result)
    prompt = None
    print(subs)

    if subs:
        prompt = subscriptions.subscriptions_to_prompt(subs, "Опиши личность пользователя по его подпискам на вышеперечисленные сообщества")

    print(prompt)
elif(char == '5'):
    # часто задаваемые вопросы из комментариев
    thread = None
    result = get_vk_q_and_a(USER_ID, POST_ID,ACCESS_TOKEN)
    print(result)

    thread = comments.parse_vk_comments(result)
    prompt = None
    print(thread)

    if thread:
        prompt = comments.comments_to_prompt(thread, "Создай список часто задаваемых вопросов в комментариях от подписчиков и предложи возможные ответы")

    print(prompt)




'''
def get_vk_newsfeed(owner_id, post_id, access_token):
    # URL и параметры строки запроса
    url = "https://api.vk.com/method/newsfeed.getRecommended"
    query_params = {
        "v": "5.246"
    }

    # Данные для тела запроса 
    form_data = {
        "fields": "name",
        "access_token": access_token
    }

    # Заголовки из запроса
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://vk.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            url,
            params=query_params,
            data=form_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при запросе для owner_id {owner_id}: {str(e)}")
        return None
'''

