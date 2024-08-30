# animation.py

import os
import time
import re
from openai import OpenAI
from selenium import webdriver
from PIL import Image
from Udility.auth import authenticate

# Ensure user is authenticated and API key is set
authenticate()

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_detailed_instructions(text_description):
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yourwebsite.com", 
            "X-Title": "SVG Generator App",
        },
        model="nousresearch/hermes-3-llama-3.1-405b",
        messages=[
            {
                "role": "user",
                "content": f"Generate instructions for creating an SVG illustration with animation for the following user's prompt: '{text_description}'."
            },
        ],
    )
    
    return response.choices[0].message.content

def generate_svg_from_instructions(detailed_instructions):
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yourwebsite.com",
            "X-Title": "SVG Generator App",
        },
        model="nousresearch/hermes-3-llama-3.1-405b",
        messages=[
            {
                "role": "user",
                "content": f"You are an AI that generates SVG code based on detailed instructions. Provide SVG code only including animation elements. Here are the instructions: {detailed_instructions}"
            },
        ],
    )
    
    svg_code = response.choices[0].message.content
    svg_extracted = extract_svg_code(svg_code)
    if not svg_extracted:
        raise ValueError("Invalid SVG code generated. Please check the LLM response.")
    
    return svg_extracted

def extract_svg_code(text):
    svg_match = re.search(r"<svg[\s\S]*</svg>", text)
    return svg_match.group(0) if svg_match else None

def save_svg_to_html(svg_code, html_filename='temp_animation.html'):
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }}
            svg {{ width: 100vw; height: 100vh; }}
        </style>
    </head>
    <body>
        {svg_code}
    </body>
    </html>
    """
    with open(html_filename, 'w') as html_file:
        html_file.write(html_content)

def svg_to_frames(svg_code, output_dir='frames', frame_count=30, frame_delay=0.1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    save_svg_to_html(svg_code)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get('file://' + os.path.abspath('temp_animation.html'))
    driver.set_window_size(800, 600)

    for frame in range(frame_count):
        time.sleep(frame_delay)
        frame_filename = os.path.join(output_dir, f'frame_{frame:03d}.png')
        driver.save_screenshot(frame_filename)

    driver.quit()

    return output_dir

def frames_to_gif(frames_dir='frames', output_gif='animation.gif', frame_duration=100):
    frames = [os.path.join(frames_dir, f) for f in sorted(os.listdir(frames_dir)) if f.endswith('.png')]
    imgs = [Image.open(frame) for frame in frames]
    imgs[0].save(output_gif, save_all=True, append_images=imgs[1:], duration=frame_duration, loop=0)

def main(text_description):
    try:
        detailed_instructions = get_detailed_instructions(text_description)
        svg_code = generate_svg_from_instructions(detailed_instructions)
        frames_dir = svg_to_frames(svg_code)
        frames_to_gif(frames_dir)
        print(f"Animated GIF created as 'animation.gif'.")
    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main("Visual representation of distance vs displacement.")
