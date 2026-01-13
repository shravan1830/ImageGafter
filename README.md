
# ImageGafter

ImageGafter is a Python-based tool that addresses image scarcity in deep learning by combining image-to-text generation with generative image synthesis.

The system first converts an input image into descriptive textual prompts using large language models (LLMs). These prompts are then used to generate diverse new images, effectively expanding the dataset. This approach helps create richer training data for building more robust and accurate deep learning models.



## Run Locally

Clone the project

```bash
  git clone https://github.com/pioneerHitesh/ImageGafter.git
```

Go to the project directory

```bash
  cd ImageGafter
```

(Recommended) Create a virtual environment

```bash
  python -m venv env
```

Activate it

```bash
  .\env\Scripts\activate
```





Install dependencies

```bash
  pip install -r requirements.txt
```

Configure API Keys
    
- Copy the example config file:

```
  copy lib\config.example.json lib\config.json
```

- Open lib/config.json and add your API keys:

```
{
  "gemini_pro_api_key": ["YOUR_GEMINI_API_KEY"],
  "stable_diffusion_api_key": ["YOUR_IMAGEPIPELINE_API_KEY"]
}
```

Start the server

```bash
  python app.py
```


## Demo


[![ImageGafter Demo](https://img.youtube.com/vi/atXewhItKzs/0.jpg)](https://www.youtube.com/watch?v=atXewhItKzs)

Click the image to watch the demo on YouTube.

## Contributing

Pull requests are welcome.
Please ensure your changes do not include secrets or local configuration files.


## License

[MIT](https://choosealicense.com/licenses/mit/)

