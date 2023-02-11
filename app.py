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
        # To do

    def move_to_next_page(self, page_no):
        """Next page clicker!"""
        time.sleep(2)
        try:
            next_page = self.wait.until(
                EC.element_to_be_clickable((By.ID, "datatable_next"))
            )
            # download_file()
            if "disabled" not in next_page.get_attribute("class"):
                a_link = next_page.find_element(By.XPATH, "//a[text()='Next']")
                a_link.click()
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
