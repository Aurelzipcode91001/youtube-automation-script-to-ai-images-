# **Story-to-Image Generator for Shorts & Videos** 🎥📸  

![AI Story to Image](images/story_to_image_example.jpg)

This script automates **image generation for YouTube Shorts and videos**. It analyzes a given story/script and generates high-quality images in **JPG format**, which can be used for video creation.  

---

## **📌 Features**  
✅ **Automated Image Generation** → Converts a script into a sequence of images  
✅ **Optimized for Shorts (9:16 format)** → Can be changed for different video formats  
✅ **Supports Large Scripts** → Can generate **up to 1,000 images**  
✅ **Customizable AI Models** → Uses `gpt-4o-mini` but can be replaced  
✅ **Flexible Image Quality** → Depends on **prompt quality** & AI model  
✅ **Fast & Efficient** → Uses **Replicate’s Flux-Schnell** model  

![AI Generated Example](images/ai_generated_example.jpg)

---

## **🛠 How It Works**
1. **Enter Your Story/Script** → The script analyzes the story and extracts key scenes.  
2. **Generate Image Prompts** → OpenAI creates **realistic, cinematic** image prompts.  
3. **Create Images with Replicate** → The script sends prompts to the **Flux-Schnell model** on Replicate.  
4. **Download & Save Images** → The images are resized and saved as high-quality JPG files.  

🔹 **By default, the aspect ratio is set to 9:16 for YouTube Shorts, but it can be changed.**  
🔹 **The AI model (`gpt-4o-mini`) can be replaced with other OpenAI models.**  

---

## **💰 Cost Estimation (February 2025)**
- **Flux-Schnell model on Replicate**: **100 images ≈ $0.30 USD**  
- **Better results with Flux-Dev model** (higher quality but slightly more expensive)  

🔹 **Costs may change based on Replicate’s pricing.**  

---

## **📌 Requirements**
- Python 3.8+  
- Install dependencies:  
  ```sh
  pip install openai requests pillow python-dotenv replicate tqdm
