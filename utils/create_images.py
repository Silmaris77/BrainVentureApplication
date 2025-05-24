import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os

def create_logo():
    """Create a simple logo for the BrainVenture app."""
    img = Image.new('RGB', (400, 200), color=(52, 152, 219))
    d = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    d.text((100, 80), "BrainVenture", fill=(255, 255, 255), font=font)
    
    # Add a simple brain icon
    d.ellipse((50, 70, 90, 110), fill=(255, 255, 255))
    d.ellipse((60, 60, 80, 80), fill=(255, 255, 255))
    
    # Save the image
    img_path = os.path.join("static", "images", "brainventure_logo.png")
    img.save(img_path)
    return img_path

def create_default_avatar():
    """Create a simple default avatar."""
    img = Image.new('RGB', (200, 200), color=(44, 62, 80))
    d = ImageDraw.Draw(img)
    
    # Draw a simple avatar
    d.ellipse((50, 30, 150, 130), fill=(189, 195, 199))
    d.rectangle((50, 130, 150, 200), fill=(189, 195, 199))
    
    # Save the image
    img_path = os.path.join("static", "images", "default_avatar.png")
    img.save(img_path)
    return img_path

if __name__ == "__main__":
    create_logo()
    create_default_avatar()
    print("Images created successfully!")
