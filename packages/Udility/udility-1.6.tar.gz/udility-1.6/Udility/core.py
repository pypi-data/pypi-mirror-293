import os
from openai import OpenAI
import cairosvg
from PIL import Image
import matplotlib.pyplot as plt

class SVGIllustrator:
    def __init__(self, api_key=None, base_url="https://openrouter.ai/api/v1"):
        """
        Initialize the SVGIllustrator with OpenAI API key and base URL.
        """
        if not api_key:
            api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key not provided or set in environment variables.")
        
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.max_tokens = 60000

    def get_detailed_instructions(self, text_description):
        """
        Get detailed instructions for creating an SVG illustration from a text description.
        """
        response = self.client.chat.completions.create(
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
        
        detailed_instructions = response.choices[0].message.content
        return detailed_instructions

    def generate_svg_from_instructions(self, detailed_instructions):
        """
        Generate SVG code based on detailed instructions.
        """
        response = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://yourwebsite.com",  # Optional, replace with your site URL
                "X-Title": "SVG Generator App",  # Optional, replace with your app name
            },
            model="nousresearch/hermes-3-llama-3.1-405b",
            messages=[
                {
                    "role": "user",
                    "content": f"You are an AI that generates SVG code based on detailed instructions. Only provide SVG code without additional text or styling. Only provide valid SVG code including animation elements without additional text or styling. The SVG code should start with '<svg>' and end with '</svg>'. Here's the instruction for the SVG image script: {detailed_instructions}.",
                },
            ],
        )
        
        svg_code = response.choices[0].message.content
        return svg_code

    def svg_to_png(self, svg_code, output_filename='output.png'):
        """
        Convert SVG code to a PNG image.
        """
        # Save SVG to a temporary file
        with open('temp.svg', 'w') as file:
            file.write(svg_code)
        
        # Convert the SVG to PNG
        cairosvg.svg2png(url='temp.svg', write_to=output_filename)

    def display_image(self, image_path):
        """
        Display a PNG image using matplotlib.
        """
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    def create_illustration(self, text_description):
        """
        Process a text description to generate and display an SVG image.
        """
        # Step 1: Get detailed instructions for SVG creation
        detailed_instructions = self.get_detailed_instructions(text_description)
        print("Detailed Instructions:\n", detailed_instructions)  # Print for verification
        
        # Step 2: Generate SVG from detailed instructions
        svg_code = self.generate_svg_from_instructions(detailed_instructions)
        print("Generated SVG Code:\n", svg_code)  # Print SVG code for verification
        
        # Step 3: Convert SVG to PNG
        self.svg_to_png(svg_code)
        
        # Step 4: Display the PNG image
        self.display_image('output.png')
