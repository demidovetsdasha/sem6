import vk_api

vk_session = vk_api.VkApi(token='14e22b7c14e22b7c14e22b7ce317c9e032114e214e22b7c732a4e556b70f1b035ff081e')

vk = vk_session.get_api()

print(vk.users.get(user_id=236017320))
print(vk.users.get(user_id=233307768))