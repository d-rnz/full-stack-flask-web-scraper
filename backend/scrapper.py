from playwright.sync_api import sync_playwright
import sqlite3


DB_PATH = "Z:\\00 CLOUD\\05 Projects\\03 Apps\\full-stack-flask-web-scraper\\backend\\instance\\manga.db"
PAGES = 3

links = [
    "https://www.mgeko.com/jumbo/manga/",
    "https://asuratoon.com/",
    # "https://reaperscans.com/",
]

###########################################################################
# TODO: Edit when the website is updated

# Right click on one item -> inspect element
# Right click on the element -> copy Xpath
# Remove index from the xpath

mgeko_xpath = '//*[@id="latest-updates"]/section[3]/ul/li'
asura_xpath = '//*[@id="content"]/div/div[1]/div[5]/div[2]/div'

###########################################################################


def get_mgeko(page, titles):
    manga_list = []
    items_list = page.query_selector_all(mgeko_xpath)

    for item in items_list:
        manga_dict = {}

        try:
            ###########################################################################
            # TODO: Edit when the website is updated

            # Use .query_selector() + "TAG.CLASS" or "TAG#ID" to get the element
            # Use .get_attribute("ATTRIBUTE") to get the value of the attribute
            # Use .inner_text() to get the text inside the element

            manga_dict["image_url"] = item.query_selector("img").get_attribute("src")
            manga_dict["title"] = item.query_selector("h4").inner_text()
            # Parse the latest chapter to a float
            ch = item.query_selector("h5").inner_text()
            ch = ch.partition("Chapter ")[2]
            if "eng" in ch:
                parts = ch.split("-")

                if parts[1].isdigit():
                    ch = "f{parts[0]}.{parts[1]}"
                else:
                    ch = parts[0]
            else:
                ch = 0
            manga_dict["latest_chapter"] = float(ch)
            manga_dict["link"] = item.query_selector("a").get_attribute("href")

            ###########################################################################

        except Exception as e:
            print("mgeko:", e)

        try:
            if manga_dict["title"] in titles:
                manga_list.append(manga_dict)

        except Exception as e:
            print("mgeko:", e)

    return manga_list


def get_asura(page, titles):
    manga_list = []
    items_list = page.query_selector_all(asura_xpath)

    for item in items_list:
        manga_dict = {}

        try:
            ###########################################################################
            # TODO: Edit when the website is updated

            manga_dict["image_url"] = item.query_selector("img").get_attribute(
                "data-src"
            )
            manga_dict["title"] = item.query_selector("h4").inner_text()
            # Parse the latest chapter to a float
            ch = item.query_selector("li").query_selector("a").inner_text()
            ch = ch.partition("Chapter ")[2]
            ch = ch.partition(" ")[0]
            manga_dict["latest_chapter"] = float(ch)
            manga_dict["link"] = item.query_selector("a.series").get_attribute("href")

            ###########################################################################

        except Exception as e:
            print("asura:", e)

        try:
            if manga_dict["title"] in titles:
                manga_list.append(manga_dict)

        except Exception as e:
            print("asura:", e)

    return manga_list


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get the titles related to asura from the database
    c.execute("SELECT title FROM manga WHERE website = 'asura'")
    asura_list = c.fetchall()
    asura_titles = [lst[0] for lst in asura_list]

    # Get the titles related to mgeko from the database
    c.execute("SELECT title FROM manga WHERE website = 'mgeko'")
    mgeko_list = c.fetchall()
    mgeko_titles = [lst[0] for lst in mgeko_list]

    # Launch playwright context manager
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i in links:
            page.goto(i)

            # Wait for the page to load
            page.wait_for_timeout(3000)

            manga_list = []

            if "mgeko" in i:
                for _ in range(1, PAGES + 1):
                    manga_list += get_mgeko(page, mgeko_titles)
                    page.get_by_text("chevron_right").first.click()
                    page.wait_for_timeout(3000)

            elif "asura" in i:
                for _ in range(1, PAGES + 1):
                    manga_list += get_asura(page, asura_titles)
                    page.get_by_text("Next ").first.click()
                    page.wait_for_timeout(3000)

            print(manga_list)

            for manga in manga_list:
                c.execute(
                    "UPDATE manga SET image_url = :image_url, latest_chapter = :latest_chapter, link = :link WHERE title = :title",
                    {
                        "image_url": manga["image_url"],
                        "latest_chapter": manga["latest_chapter"],
                        "link": manga["link"],
                        "title": manga["title"],
                    },
                )

        browser.close()

    conn.commit()
    conn.close()


if __name__ == "__main__":

    main()
