from json import load,dumps
import os
from typing import Union
from . import ImageToText
from . import TextToImage
from time import sleep
from . import ApiKeyNotFoundError
from multiprocessing import Process, Manager, Lock

def get_text_prompts(image_path: str, no_of_prompts=10):
    """Generates similar text prompts similar to the images in directory

    Args:
        image_dir: string containing relative/absolute path of the image directory
        no_of_prompts: The number of similar text prompts to be generated (default = 10)

    Returns:
        prompts: list of prompts similar to the given image
    """
    obj = ImageToText.ImageToText(r".\lib\config.json")
    # image_path = input("Enter path of the image\n")
    prompts = obj.get_text_prompts(image_path, no_of_prompts)

    print("Prompt Generation Done!")

    return prompts


def spawn_generate_image(API_KEY: str, prompt:str, dir_path:Union[str, os.PathLike] , generated_images , Lock):
    obj = TextToImage.TextToImage(API_KEY)
    image = obj.generate_image(prompt, dir_path)
    generated_images[image] = prompt


def generate_images(
    prompts: list[str],
    dir_path: Union[str, os.PathLike],
    api_key_file_path: Union[str, os.PathLike],
):
    """Generates images based on the given text prompts"""

    with open(api_key_file_path, "r") as f:
        config_file = load(f)
        API_KEY = config_file.get("stable_diffusion_api_key")

    if not API_KEY:
        raise ApiKeyNotFoundError("No API key found in the specified file")

    API_KEY = API_KEY[0]

    process_list = []
    generated_images = {}
    with Manager() as manager:
        images = manager.dict()  
        lock = Lock() 
        for prompt in prompts:
            p = Process(target=spawn_generate_image, args=(API_KEY, prompt, dir_path, images, lock))
            p.start()
            process_list.append(p)

        for process in process_list:
            process.join()

        generated_images = dict(images)
    return generated_images

