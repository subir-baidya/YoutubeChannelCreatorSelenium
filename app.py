import random
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

names_file = Path(__file__).with_name("names.txt")
indian_names = []
for line in names_file.read_text(encoding="utf-8").splitlines():
    full_name = line.strip()
    if full_name:
        indian_names.append(full_name)

if not indian_names:
    raise ValueError(f"No names found in {names_file}")

options = Options()
# options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
options.profile = str(
    Path.home() / "Library/Application Support/Firefox/Profiles/1gW1JQdE.Profile 6"
)

driver = webdriver.Firefox(options=options)

try:
    while True:
        driver.get("https://www.youtube.com/channel_switcher")
        print("Page title:", driver.title)

        switcher_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-switcher-page-renderer/div[2]/div[3]/ytd-button-renderer/yt-button-shape/a/yt-light-shape/yt-light-touch-feedback-shape",
                )
            )
        )
        switcher_button.click()

        channel_name = random.choice(indian_names)
        name_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-channel-creation-dialog-renderer/div/div[5]/div[1]/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/tp-yt-iron-input/input",
                )
            )
        )
        name_input.clear()
        name_input.send_keys(channel_name)
        print(f"Entered channel name: {channel_name}")

        next_button_xpath = (
            "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/"
            "ytd-channel-creation-dialog-renderer/div/div[6]/"
            "ytd-button-renderer[2]/yt-button-shape/button/"
            "yt-touch-feedback-shape"
        )
        try:
            next_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
            next_button.click()
            print("Clicked the channel dialog button.")
        except TimeoutException:
            print(
                "The channel dialog button did not become clickable within 30 seconds."
            )

        print("Starting next cycle. Press Ctrl+C to stop.")

finally:
    if driver is not None:
        driver.quit()
