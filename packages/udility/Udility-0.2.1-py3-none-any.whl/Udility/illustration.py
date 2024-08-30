# illustration.py

import os
from openai import OpenAI
import cairosvg
from PIL import Image
import matplotlib.pyplot as plt
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
                "content": f"Generate quick instructions for creating an SVG illustration for the following user's prompt: '{text_description}'."
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
                "content": f"You are an AI that generates SVG code based on detailed instructions. Provide SVG code only. Here are the instructions: {detailed_instructions}"
            },
        ],
    )
    
    return response.choices[0].message.content

def svg_to_png(svg_code, output_filename='output.png'):
    with open('temp.svg', 'w') as file:
        file.write(svg_code)
    cairosvg.svg2png(url='temp.svg', write_to=output_filename)

def display_image(image_path):
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def main(text_description):
    detailed_instructions = get_detailed_instructions(text_description)
    svg_code = generate_svg_from_instructions(detailed_instructions)
    svg_to_png(svg_code)
    display_image('output.png')

if __name__ == "__main__":
    main("Lifecycle of amoeba.")
