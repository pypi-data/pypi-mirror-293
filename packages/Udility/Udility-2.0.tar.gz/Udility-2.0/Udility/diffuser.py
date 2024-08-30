import os
from openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import cairosvg

# Fetch the OpenRouter API key from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise EnvironmentError("The OpenRouter API key is not set. Please set it as an environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def get_detailed_instructions(text_description):
    """
    Get detailed instructions for creating an SVG illustration from a text description.
    
    Args:
        text_description (str): The text description of the desired image.
        
    Returns:
        str: The detailed instructions for creating the SVG.
    """
    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://yourwebsite.com",  # Optional, replace with your site URL
                "X-Title": "SVG Generator App",  # Optional, replace with your app name
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
    except Exception as e:
        raise RuntimeError(f"Failed to get detailed instructions: {e}")

def generate_svg_from_instructions(detailed_instructions):
    """
    Generate SVG code from detailed instructions.
    
    Args:
        detailed_instructions (str): Detailed instructions for SVG creation.
        
    Returns:
        str: SVG code.
    """
    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://yourwebsite.com",
                "X-Title": "SVG Generator App",
            },
            model="nousresearch/hermes-3-llama-3.1-405b",
            messages=[
                {
                    "role": "user",
                    "content": f"You are an AI that generates SVG code based on detailed instructions. Only provide SVG code without additional text or styling. The SVG code should start with '<svg>' and end with '</svg>'. Here's the instruction for the SVG image script: {detailed_instructions}.",
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate SVG code: {e}")

def svg_to_png(svg_code, output_filename='output.png'):
    """
    Convert SVG code to a PNG image.
    
    Args:
        svg_code (str): SVG code to be converted.
        output_filename (str): Output filename for the PNG image.
    """
    try:
        # Convert SVG to PNG using BytesIO for in-memory handling
        png_data = cairosvg.svg2png(bytestring=svg_code.encode('utf-8'))
        with open(output_filename, 'wb') as file:
            file.write(png_data)
    except Exception as e:
        raise RuntimeError(f"Failed to convert SVG to PNG: {e}")

def display_image(image_path):
    """
    Display a PNG image.
    
    Args:
        image_path (str): The path to the PNG image file.
    """
    try:
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    except Exception as e:
        raise RuntimeError(f"Failed to display image: {e}")

def generate_image_from_text(text_description, output_filename='output.png'):
    """
    Generate an image from text description and display it.
    
    Args:
        text_description (str): The description of the desired SVG image.
        output_filename (str): The output filename for the PNG image.
    """
    detailed_instructions = get_detailed_instructions(text_description)
    svg_code = generate_svg_from_instructions(detailed_instructions)
    svg_to_png(svg_code, output_filename)
    display_image(output_filename)
