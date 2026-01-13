from json import load
import os
from time import sleep
from typing import Optional, Union
import PIL.Image
import google.generativeai as genai
from . import ApiKeyNotFoundError



class ImageToText:
    """Generates similar text prompts for a given image

    ### To get started
    ```
    obj =  ImageToText("config.json")
    print(obj.get_text_prompts("test.jpg"))
    ```
    """

    def __init__(
        self,
        file_path: Union[str, os.PathLike],
        model: Optional[str] = "gemini-2.5-flash",
        api_key_limit: Optional[int] = 50,
    ) -> None:
        """
        Args:
            file_path: string containing relative/absolute path of the configuration file
            model: model used for text prompt generation (default = "gemini-2.5-flash")
            api_key_limit: number of requests to be made using the api key before rotating it (default = 50)
        """
        self.___API_KEYS = []
        self.___img_count = 0
        self.___api_key_limit = api_key_limit
        self.___model = genai.GenerativeModel(model)
        self.___load_api_keys(file_path)

    def ___rotate_api_keys(self) -> None:
        """Rotates the api key based on the api_key_limit set if multiple api keys are available"""
        api_key_idx = (self.___img_count // self.___api_key_limit) - 1
        if api_key_idx < self.___no_of_api_keys:
            genai.configure(api_key=self.___API_KEYS[api_key_idx])
        else:
            api_key_idx = 0
            self.___img_count = 0

    def ___load_api_keys(self, file_path: Union[str, os.PathLike]) -> None:
        """Loads the api keys from file path into a list

        Args:
            file_path: string containing relative/absolute path of the configuration file

        Raises:
            ApiKeyNotFoundError: if no API key is found in the specified file
        """

        with open(file_path, "r") as f:
            config_file = load(f)
            self.___API_KEYS = config_file["gemini_pro_api_key"]
            self.___safety_settings = config_file["safety_setting"]

        self.___no_of_api_keys = len(self.___API_KEYS)

        if self.___no_of_api_keys == 0:
            raise ApiKeyNotFoundError("No API key found in the specified file")

        self.___rotate_api_keys()

    def get_text_prompts(
        self, image_path: Union[str, os.PathLike], no_of_prompts: Optional[int] = 10
    ) -> list[str]:
        """Generates similar text prompts similar to the given image's

        Args:
            image_path: string containing relative/absolute path of the image
            no_of_prompts: The number of similar text prompts to be generated (default = 10)

        Returns:
            prompts: list of prompts similar to the given image
        """
        img = PIL.Image.open(image_path)
        prompt = [
            f"generate {no_of_prompts} descriptions of images similar to given image and end each description with a ^",
            img,
        ]
        response = self.___model.generate_content(
            prompt, stream=True, safety_settings=self.___safety_settings
        )
        response.resolve()
        prompts = response.text.split("^")

        self.___img_count += 1

        if self.___no_of_api_keys != 1 and self.___img_count % self.___api_key_limit:
            self.___rotate_api_keys()
        else:
            sleep(60)
        
        prompts = [pmpt for pmpt in prompts if pmpt != '']
        return prompts[:no_of_prompts]
