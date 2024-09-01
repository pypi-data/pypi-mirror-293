from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.file_downloader import get_file, download_image
from selenium.webdriver.common.by import By
from typing import Union
# Check: https://github.com/gabrielkheisa/instagram-downloader/blob/main/run.py
# He downloads with selenium
# This and the one below: https://stackoverflow.com/a/48705202
# This code (https://github.com/instaloader/instaloader/tree/master) is used
# by RocketAPI to charge you
def get_instagram_video(url: str, output_filename: Union[str, None] = None):
    scrapper = ChromeScrapper()

    # 1st. Go to: https://downloadgram.org/video-downloader.php
    DOWNLOAD_INSTAGRAM_VIDEO_UTL = 'https://downloadgram.org/video-downloader.php'
    scrapper.go_to_web_and_wait_util_loaded(DOWNLOAD_INSTAGRAM_VIDEO_UTL)

    # We need to place the url in the input and press enter
    url_input = scrapper.find_element_by_id('url')
    url_input.send_keys(url)

    submit_button = scrapper.find_element_by_id('submit')
    submit_button.click()

    # We need to wait until video is shown
    video_element = scrapper.find_element_by_element_type('video')
    video_source_element = video_element.find_element(By.TAG_NAME, 'source')

    thumbnail_image_url = video_element.get_attribute('poster')
    video_source_url = video_source_element.get_attribute('src')

    # TODO: Remove this, it is just a test
    download_image(thumbnail_image_url, 'test_instagram_image.png')

    return get_file(video_source_url, output_filename)