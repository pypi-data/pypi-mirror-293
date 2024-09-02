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

model_name = 'aisak-ai/O'

# Create model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map='auto',
    trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True)

# User input for text prompt and image URL
prompt = input("You: ")
image_url = input("Enter the image URL (leave empty for default): ")

# Default image URL
default_image_url = 'https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcRM0OQsITDDUQ-PCjobiXAyUfEQn1sOAkjorPKB2miR-sYx_aCjqMSevH2Y4WjIvPoA'

# Use default image URL if user input is empty
if not image_url.strip():
    image_url = default_image_url
    # Add prefix to indicate ignoring the image
    prompt = "[IGNORE THE IMAGE, ONLY LOOK AT THE TEXT, BE CONCISE] " + prompt

messages = [
    {"role": "user", "content": f'<image>\n{prompt}'}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

text_chunks = [tokenizer(chunk).input_ids for chunk in text.split('<image>')]
input_ids = torch.tensor(text_chunks[0] + [-200] + text_chunks[1], dtype=torch.long).unsqueeze(0)

# Fetch and process the image from the URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Convert image to tensor
image_tensor = model.process_images([image], model.config).to(dtype=model.dtype)

# Generate
output_ids = model.generate(
    input_ids,
    images=image_tensor,
    temperature=0.7,
    max_new_tokens=4096,
    use_cache=True)[0]

print("AISAK:")
print(tokenizer.decode(output_ids[input_ids.shape[1]:], skip_special_tokens=True).strip())
