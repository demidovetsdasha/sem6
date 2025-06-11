import asyncio
from playwright.async_api import async_playwright

# Конфигурационные параметры
TOKEN = '.'

async def get_vk_token():
    global TOKEN
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Обработчик для перехвата запросов
        def check_request(request):
            global TOKEN

            try:
                json = request.post_data_json
                if "access_token" in json:
                    TOKEN = json['access_token']
            except:
                pass

        page.on('requestfinished', check_request)

        # Формируем URL для авторизации
        auth_url = 'https://vk.com/'

        await page.goto(auth_url)

        #page.get_by_text('Войти другим способом').click()
        #page.locator('.vkuiFormField__content').locator('input').fill(LOGIN)
        #page.get_by_text('Войти').first.click()
        #page.get_by_text('Подтвердить другим способом').click()
        #page.get_by_text('QR-код').click()

        await page.wait_for_url('https://vk.com/feed')

        #await page.get_by_test_id("search_global_tab_friends").get_by_text("Друзья").click(timeout=60000)

        token = ''
        while True:
            if(token != TOKEN):
                print(TOKEN)
                token = TOKEN
            
            await page.wait_for_timeout(30000)
            await page.goto('https://vk.com/feed')

        context.close()
        browser.close()

asyncio.run(get_vk_token())
