import json
from vkbottle import API
import asyncio
import requests

#url = "https://id.vk.com/oauth2/auth"

#data = {
#    "client_id": "53210837",
#    "grant_type": "authorization_code",
#    "code_verifier": "JdDh0c7IW80334lFDBZcPGCCEgWbec9NJJvWRdVM-uM",
#    "device_id": "SrdGHIA9Jxv2aRXOnB1ly4rFYW4V7wExoNzn_WcP5h3VswdFZ2gVjEZAnAY9_yav9fHdi_IZAe7KFIoUIaixrQ",
#   "code": "vk2.a.0V-yIs0wHl_dKuEXVwhQ85AyTY_wVTa4eG2hKuw5OUwcF2xFlYSYq-aGuA5bWJ61os6XoMaSzjs6-j7_YNiFBySmWeZKYjpQOMpLlItA-w2x7IfMl0i5A2yf2zcqomsQ096GVNxASnw5byA9hDphwwLIJN30AvEPsjspekjDAb4mgH7FX7fcvfSg6SdWbB1JsDgNRso-jzSnTJ9xUzLwcAqHiv604tDhuZdS9GBa2Vw",
#    "redirect_uri": "https://app.diagrams.net/"
#}

#response = requests.post(url, data=data)

#if response.status_code == 200:
#    print("Access Token Response:", response.json())
#else:
#    print("Error:", response.status_code, response.text)


api = API(token="vk2.a.STk8HwuIDvTpU4KcfJfO2gSO6Z52mN9dMdT2XJQmKhb46zz5_5xUP0uBDnYH58QPHUjpfJE5Ib3RE3kUxH0RJxYZqSPMe74aLfH2S-fxh3-pp2FVLN9zmBYWv-_1G-qoGuVP8jAe4svA0f3DoBoufyNuenhucoEm4x3Eg84ja0c5D24zkBRXFlTVEb4lmN_eu6DOLwILW_KgM_bV69ht6BXqMEzp7VfV0pg2qP3kgyg-amOI5CJ8Djfp66AKqMNN")

async def main():
    await api.wall.post(message='hello world')

asyncio.run(main())