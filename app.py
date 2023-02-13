from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


class VRP_REP_Scrapper:
    """Vehicle Routing Problem Repository Scrapper"""

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.vrp-rep.org/datasets.html")
        self.wait = WebDriverWait(self.driver, 10)
        self.download_interval = 10
        self.switch_page_interval = 5

    def set_option_to_max(self):
        """Show max entries"""
        select = Select(self.driver.find_element(By.NAME, "datatable_length"))
        options = select.options
        max_option = max([int(e.text) for e in options])
        select.select_by_value(str(max_option))

        # Start navigating and downloading the file
        self.move_to_next_page(1)

    def download_file(self):
        """Download the file"""
        table_rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
        i = 0
        while i < len(table_rows):
            row = table_rows[i]
            download_links = row.find_element(
                By.XPATH, "./td/a[contains(@href,'download')]"
            )
            download_links.click()
            time.sleep(self.download_interval)
            i += 1
            # refinding the element after each download
            # table_rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")

    def move_to_next_page(self, page_no):
        """Next page clicker!"""
        try:
            next_page = self.wait.until(
                EC.element_to_be_clickable((By.ID, "datatable_next"))
            )
            self.download_file()
            if "disabled" not in next_page.get_attribute("class"):
                a_link = next_page.find_element(By.XPATH, "//a[text()='Next']")
                a_link.click()
                time.sleep(self.switch_page_interval)
                page_no += 1
                print("Moving to Page:", page_no)
                self.move_to_next_page(page_no)
            else:
                print("\nQuiting the driver!")
                self.quit_driver()
        except StaleElementReferenceException:
            self.move_to_next_page(page_no)

    def quit_driver(self):
        """Quit the driver"""
        self.driver.quit()


if __name__ == "__main__":
    scrapper = VRP_REP_Scrapper()
    scrapper.set_option_to_max()
