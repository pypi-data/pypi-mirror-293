
from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.file_downloader import get_file
from selenium.webdriver.common.by import By
from typing import Union

def get_facebook_video(url: str, output_filename: Union[str, None] = None):
    """
    Gets the Facebook video (reel) from the provided 'url' (if valid)
    and returns its data or stores it locally as 'output_filename' if
    provided.
    """
    scrapper = ChromeScrapper()
    scrapper.go_to_web_and_wait_util_loaded(url)

    # We need to wait until video is shown
    video_element = scrapper.find_element_by_element_type_waiting('video')
    video_source_url = video_element.get_attribute('src')

    # This just downloads the thumbnail but, for what (?)
    # thumbnail_image_url = video_element.get_attribute('poster')
    # download_image(thumbnail_image_url, 'test_instagram_image.png')

    return get_file(video_source_url, output_filename)