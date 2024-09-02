# aisak.py
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import requests
from io import BytesIO
import warnings

# Disable some warnings
transformers.logging.set_verbosity_error()
transformers.logging.disable_progress_bar()
warnings.filterwarnings('ignore')

# Set device
torch.set_default_device('cuda')  # or 'cpu'


class AISAKModel:
    def __init__(self, model_name='aisak-ai/O'):
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='auto',
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

    def generate_response(self, prompt, image_url=None):
        # Default image URL
        default_image_url = 'https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcRM0OQsITDDUQ-PCjobiXAyUfEQn1sOAkjorPKB2miR-sYx_aCjqMSevH2Y4WjIvPoA'

        if not image_url:
            image_url = default_image_url
            prompt = "[IGNORE THE BLANK IMAGE, ONLY LOOK AT THE TEXT] " + prompt

        messages = [
            {"role": "user", "content": f'<image>\n{prompt}'}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        text_chunks = [self.tokenizer(chunk).input_ids for chunk in text.split('<image>')]
        input_ids = torch.tensor(text_chunks[0] + [-200] + text_chunks[1], dtype=torch.long).unsqueeze(0)

        # Fetch and process the image from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Convert image to tensor
        image_tensor = self.model.process_images([image], self.model.config).to(dtype=self.model.dtype)

        # Generate
        output_ids = self.model.generate(
            input_ids,
            images=image_tensor,
            temperature=0.5,
            max_new_tokens=4096,
            use_cache=True
        )[0]

        return self.tokenizer.decode(output_ids[input_ids.shape[1]:], skip_special_tokens=True).strip()
