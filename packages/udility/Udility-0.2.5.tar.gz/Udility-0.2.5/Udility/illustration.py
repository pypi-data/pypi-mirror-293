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
    """Generate detailed instructions for SVG illustration."""
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yourwebsite.com",
            "X-Title": "SVG Generator App",
        },
        model="nousresearch/hermes-3-llama-3.1-405b",
        messages=[
            {
                "role": "user",
                "content": f"Generate quick instructions for creating an SVG illustration for the following user's prompt: '{text_description}'. Provide all necessary details to build a well-defined image for this query.",
            },
        ],
    )
    
    return response.choices[0].message.content

def generate_svg_from_instructions(detailed_instructions):
    """Generate SVG code from detailed instructions."""
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yourwebsite.com",
            "X-Title": "SVG Generator App",
        },
        model="nousresearch/hermes-3-llama-3.1-405b",
        messages=[
            {
                "role": "user",
                "content": f"You are an AI that generates SVG code based on detailed instructions. Provide SVG code without additional text or styling. The SVG code should start with '<svg>' and end with '</svg>'. Here are the instructions: {detailed_instructions}.",
            },
        ],
    )
    
    return response.choices[0].message.content

def svg_to_png(svg_code, output_filename='output.png'):
    """Convert SVG code to a PNG image file."""
    with open('temp.svg', 'w') as file:
        file.write(svg_code)
    
    cairosvg.svg2png(url='temp.svg', write_to=output_filename)

def display_image(image_path):
    """Display the generated image."""
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def main(text_description):
    """Main function to generate and display an SVG illustration from a text description."""
    detailed_instructions = get_detailed_instructions(text_description)
    print("Detailed Instructions:\n", detailed_instructions)  # Print for verification
    
    svg_code = generate_svg_from_instructions(detailed_instructions)
    print("Generated SVG Code:\n", svg_code)  # Print SVG code for verification
    
    svg_to_png(svg_code)
    
    display_image('output.png')

if __name__ == "__main__":
    main("Lifecycle of amoeba.")
