from multiprocessing import cpu_count,Pool

from lib import ImageGafter

API_KEY_FILE = r".\lib\config.json"
prompts = ["A cat in the garden"]
def main():
    images = ImageGafter.generate_images(prompts, "outputs", API_KEY_FILE)
    print(images)

if __name__ == "__main__":
    main()