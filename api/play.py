from playwright.async_api import async_playwright

async def episode_list(url_anime, total):
    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=50)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            locale='es-CO',
            timezone_id='America/Bogota',
        )
        page = await context.new_page()
        await page.goto(url_anime, wait_until="load")

        # Get list episode
        ul = page.locator('#episodeList')
        list_episode = await ul.evaluate("""
        (ul) => {
            const urls = []
            ul.childNodes.forEach(li => li.childNodes.forEach(
                liChild => {
                    if (liChild.localName === 'a') {
                        let data = {"url":liChild.href}
                        liChild.childNodes.forEach(items => {
                            switch(items.localName) {
                                case "figure":
                                    data.img = items.childNodes[0].currentSrc
                                    break
                                case "h3":
                                    data.title = items.textContent
                                    break
                                case "p":
                                    data.episode = items.textContent
                                    break
                                case "span":
                                    data.premiere_date = items.textContent
                                    break
                                default:
                                    break
                            }
                        })
                        urls.push(data)
                    } 
                }
            ))
            return urls
        }
        """)  # pendiente virtual scroll

        await page.close()
        await browser.close()
        total_episode = list_episode[:total]
        return {"total": len(total_episode), "episodes": total_episode}


async def episode_server(url_episode):
    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=50)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            locale='es-CO',
            timezone_id='America/Bogota',
        )
        page = await context.new_page()
        await page.goto(url_episode, wait_until="load")
        server_list = await server_info(page)
        await page.close()
        return {"url": url_episode, "server": server_list}


async def server_info(page):
    server_data = []

    content_option_server_ul = page.locator('//*[@id="XpndCn"]/div[1]/ul')
    options_server_li = content_option_server_ul.locator('xpath=child::*')

    total_li = await options_server_li.count()
    for index in range(total_li):
        li = options_server_li.nth(index)
        name = await server_name(li)
        a = options_server_li.nth(index).locator("a")
        await a.click()

        iframe_content = page.locator('#video_box') # Div donde se muestran los videos
        url_iframe = await server_frame_url(iframe_content=iframe_content)

        server_data.append({"name": name, "iframe": url_iframe})

    return server_data


async def server_name(li):
    return await li.evaluate("""
        (element) => {
            if(!element) return 'Element not found';

            if(!element.dataset.originalTitle && !element.title)
                return 'Server name not found.';

            return element.dataset.originalTitle || element.title;
        }""")


async def server_frame_url(iframe_content):
    exist_iframe = await iframe_content.evaluate("""
    ( element ) => {
        let existIframe = false;
        for (let nodeElement of element.childNodes) { 
             if(nodeElement.localName === 'iframe'){
                    existIframe = true;
                break;
             }
        }
        return existIframe;
    }""")
    if exist_iframe is False:
        await iframe_content.locator('button:has-text("Aceptar y Continuar")').click()
    return await iframe_content.locator('iframe').get_attribute("src")



