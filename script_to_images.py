import os
import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import time
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import replicate
import concurrent.futures
from tqdm import tqdm
from datetime import datetime

# 🔹 Load the .env file with an absolute path
dotenv_path = "/Users/yourpath"
load_dotenv(dotenv_path)

# 🔹 Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

# 🔹 Debugging: Check if the keys are loaded
print(f"DEBUG: OPENAI_API_KEY = {'Found' if OPENAI_API_KEY else 'Not found'}")
print(f"DEBUG: REPLICATE_API_KEY = {'Found' if REPLICATE_API_KEY else 'Not found'}")

# 🔹 Storage paths
base_dir = "/Users/your_images_folder"
images_dir = os.path.join(base_dir, "images")  # Images are stored here
prompts_dir = os.path.join(base_dir, "imageprompts")  # New folder structure for prompts

# 🔹 Create directories if they do not exist
os.makedirs(images_dir, exist_ok=True)
os.makedirs(prompts_dir, exist_ok=True)

prompt_file = os.path.join(prompts_dir, "prompts.txt")

# 🔹 OpenAI: Analyze the story & generate image prompts
def analyze_story_and_generate_prompts(story):
    print("📖 OpenAI is analyzing the story for Shorts...")

    try:
        print("🟡 Sending request to OpenAI...")

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Generate photorealistic image prompts in 9:16 format without any text. The images should be cinematic, highly detailed, and realistic."},
                    {"role": "user", "content": story}
                ],
                "temperature": 0.5,
                "max_tokens": 500
            },
            timeout=30
        )

        response_json = response.json()
        output_text = response_json["choices"][0]["message"]["content"]
        print(f"🟢 OpenAI response received: {output_text[:200]}...")

        image_prompts = [line.strip() for line in output_text.split("\n") if line.strip() and line[0].isdigit()]
        return image_prompts

    except requests.exceptions.Timeout:
        print("❌ OpenAI API error: Timeout exceeded!")
        return []
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return []

# 🔹 Image generation with Replicate
def generate_image(prompt, idx):
    replicate_client = replicate.Client(api_token=REPLICATE_API_KEY)

    try:
        print(f"🖼️ Sending image {idx+1} for generation with Replicate...")

        improved_prompt = f"{prompt}, ultra-detailed, 4K resolution, cinematic lighting, sharp focus, no text, no captions, no watermarks"

        output_urls = replicate_client.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": improved_prompt, "aspect_ratio": "9:16"}
        )

        if not output_urls:
            print(f"❌ No image URL received from Replicate for image {idx+1}.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(images_dir, f"image_{timestamp}_{idx+1}.jpg")

        with requests.Session() as session:
            response = session.get(output_urls[0], timeout=20)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            target_size = (1080, 1920)
            image = image.resize(target_size, Image.LANCZOS)
            image.save(image_path, "JPEG", quality=95)

            print(f"✅ Image {idx+1} saved: {image_path}")

    except Exception as e:
        print(f"❌ Error generating image with Replicate for image {idx+1}: {e}")

# 🔹 Generate multiple images in parallel
def generate_images_with_replicate(prompts):
    print("🎨 Starting parallel image generation with Replicate...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_image, prompt, idx): idx for idx, prompt in enumerate(prompts)}
        
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="🔄 Generating images"):
            idx = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"❌ Error generating image with Replicate for image {idx+1}: {e}")

# 🔹 Save prompts & generate images
def save_prompts():
    print("🟡 save_prompts() was called!")  
    story = text_area.get("1.0", tk.END).strip()
    if not story:
        print("❌ No story entered!")
        return

    print("🔄 OpenAI is analyzing the story for Shorts...")
    root.update_idletasks()

    image_prompts = analyze_story_and_generate_prompts(story)

    if not image_prompts:
        print("❌ No prompts generated!")
        return

    print(f"📜 Saving prompts in: {prompt_file}")
    with open(prompt_file, "w", encoding="utf-8") as file:
        for prompt in image_prompts:
            file.write(prompt + "\n")

    print("🎨 Starting image generation with Replicate...")
    generate_images_with_replicate(image_prompts)

# 🔹 Start GUI
root = tk.Tk()
root.title("📱 Story to Shorts Image-Prompt Generator")
root.geometry("900x600")

label = tk.Label(root, text="📱 Enter your story and press Save:", font=("Arial", 14))
label.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20, font=("Arial", 12))
text_area.pack(padx=20, pady=10, expand=True, fill="both")

save_button = tk.Button(root, text="Save", font=("Arial", 14), command=save_prompts)
save_button.pack(pady=10)

root.mainloop()
