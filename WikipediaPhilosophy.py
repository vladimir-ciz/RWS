from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WikipediaPageElements:
    def __init__(self, driver):
        self.driver = driver

    def get_link_elements(self):
        xpath_expression = (
            '//div[@id="mw-content-text"]//a[not(contains(@class, "external")) '
            'and string-length(normalize-space()) > 0 '
            'and not(contains(@href, "/wikipedia.org/wiki/:"))]'
        )
        return self.driver.find_elements(By.XPATH, xpath_expression)


class WikipediaPageActions:
    def __init__(self, driver, elements):
        self.driver = driver
        self.elements = elements

    def click_link(self, index):
        link_elements = self.elements.get_link_elements()
        visible_links = [link for link in link_elements if link.is_displayed()]

        if 0 <= index < len(visible_links):
            visible_links[index].click()
        else:
            raise ValueError(f"Invalid link index: {index}")


def count_redirects(run_url):
    driver = webdriver.Chrome()
    driver.get(run_url)

    redirects_count = 0
    visited_urls = {}
    elements = WikipediaPageElements(driver)
    actions = WikipediaPageActions(driver, elements)

    try:
        while "Philosophy" not in driver.title:
            redirects_count += 1
            current_url = driver.current_url

            # Check if the current URL has been visited before
            if current_url in visited_urls:
                visit_count = visited_urls[current_url]
                print(f"URL already visited {visit_count} time(s): {current_url}")
                visited_urls[current_url] += 1
                actions.click_link(visit_count)  # Click on the link corresponding to the visit count
            else:
                visited_urls[current_url] = 1
                actions.click_link(1)  # Click on the first link
    finally:
        driver.quit()

    if "Philosophy" in driver.title:
        print(f"Number of redirects to Philosophy: {redirects_count}")


if __name__ == "__main__":
    run_url = "https://en.wikipedia.org/wiki/Special:Random"
    count_redirects(run_url)
