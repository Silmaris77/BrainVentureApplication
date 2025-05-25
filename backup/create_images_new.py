import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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

def create_neuroleader_type_images():
    """Create placeholder images for each neuroleader type."""
    # Create the directory if it doesn't exist
    neuroleader_img_dir = os.path.join("static", "images", "neuroleader_types")
    os.makedirs(neuroleader_img_dir, exist_ok=True)
      # Load neuroleader types data
    types_data = load_neuroleader_types()
    print(f"Loaded {len(types_data)} neuroleader types")
    
    # Create images for each type
    for type_info in types_data:
        type_id = type_info["id"]
        print(f"Creating images for {type_id}...")
        
        try:
            # Create main image
            main_img_path = create_type_main_image(type_id, type_info, neuroleader_img_dir)
            print(f"  - Created main image: {main_img_path}")
            
            # Create brain activity visualization
            brain_img_path = create_type_brain_image(type_id, type_info, neuroleader_img_dir)
            print(f"  - Created brain image: {brain_img_path}")
        except Exception as e:
            print(f"Error creating images for {type_id}: {e}")
    
    print("Neuroleader type images created successfully!")

def load_neuroleader_types():
    """Load neuroleader types from the JSON file."""
    try:
        filepath = os.path.join("data", "content", "neuroleader_types.json")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load neuroleader types: {e}")
        return []

def create_type_main_image(type_id, type_info, output_dir):
    """Create a main representative image for a neuroleader type."""
    # Color mapping for each type
    colors = {
        "neuroanalityk": (52, 152, 219),  # Blue
        "neuroreaktor": (231, 76, 60),    # Red
        "neurobalanser": (155, 89, 182),  # Purple
        "neuroempata": (46, 204, 113),    # Green
        "neuroinnowator": (241, 196, 15), # Yellow
        "neuroinspirator": (230, 126, 34) # Orange
    }
    
    # Get color for this type or use default
    color = colors.get(type_id, (200, 200, 200))
    
    # Create image
    img = Image.new('RGB', (600, 400), color=color)
    d = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        desc_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Add type name
    d.text((30, 30), type_info["name"], fill=(255, 255, 255), font=title_font)
    
    # Add icon
    d.text((30, 90), type_info["icon"], fill=(255, 255, 255), font=title_font)
    
    # Add short description
    text_lines = split_text(type_info["short_description"], 40)
    y_pos = 150
    for line in text_lines:
        d.text((30, y_pos), line, fill=(255, 255, 255), font=desc_font)
        y_pos += 30
    
    # Save the image
    img_path = os.path.join(output_dir, f"{type_id}.png")
    img.save(img_path)
    return img_path

def create_type_brain_image(type_id, type_info, output_dir):
    """Create a brain activity visualization for a neuroleader type."""
    # Set up the figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a brain outline
    brain_x = np.linspace(0, 10, 100)
    brain_top = 6 + 2 * np.sin(brain_x) - 0.2 * (brain_x - 5) ** 2
    brain_bottom = 2 + 0.5 * np.sin(brain_x / 2)
    
    # Fill brain shape
    ax.fill_between(brain_x, brain_bottom, brain_top, color='#e0e0e0')
    
    # Default title
    title = f"Aktywność mózgu: {type_id}"
    
    # Add activation areas based on type
    if type_id == "neuroanalityk":
        # Prefrontal cortex activation (low)
        ax.fill_between([7, 9.5], [6, 7], [7, 7.5], color='#3498db', alpha=0.5)
        # Amygdala activation (high)
        ax.fill_between([4.5, 5.5], [3, 3], [4, 4], color='#e74c3c', alpha=0.7)
        title = "Niska aktywność kory przedczołowej, wysoka aktywność ciała migdałowatego"
    
    elif type_id == "neuroreaktor":
        # Limbic system activation (high)
        ax.fill_between([4, 6], [3, 3], [5, 5], color='#e74c3c', alpha=0.7)
        # Prefrontal cortex activation (low)
        ax.fill_between([7, 9.5], [6, 7], [7, 7.5], color='#3498db', alpha=0.3)
        title = "Wysoka aktywność układu limbicznego, niska aktywność kory przedczołowej"
    
    elif type_id == "neurobalanser":
        # Balanced activation
        ax.fill_between([7, 9.5], [6, 7], [7, 7.5], color='#3498db', alpha=0.6)
        ax.fill_between([4, 6], [3, 3], [5, 5], color='#2ecc71', alpha=0.6)
        title = "Zrównoważona aktywność kory przedczołowej i układu limbicznego"
    
    elif type_id == "neuroempata":
        # Oxytocin system (high)
        ax.fill_between([3, 5], [4, 4], [6, 6], color='#2ecc71', alpha=0.7)
        # Mirror neurons (high)
        ax.fill_between([6, 8], [5, 5], [6.5, 6.5], color='#9b59b6', alpha=0.7)
        title = "Wysoka aktywność układu oksytocynowego i neuronów lustrzanych"
    
    elif type_id == "neuroinnowator":
        # Default mode network (high)
        ax.fill_between([2, 4], [5, 5], [7, 7], color='#f39c12', alpha=0.7)
        # Hippocampus (high)
        ax.fill_between([5, 6], [3.5, 3.5], [5, 5], color='#9b59b6', alpha=0.7)
        title = "Wysoka aktywność sieci trybu domyślnego i hipokampu"
    
    elif type_id == "neuroinspirator":
        # Limbic system (high)
        ax.fill_between([4, 6], [3, 3], [5, 5], color='#e67e22', alpha=0.7)
        # Anterior cingulate cortex (high)
        ax.fill_between([6, 8], [4.5, 4.5], [6, 6], color='#f1c40f', alpha=0.7)
        title = "Wysoka aktywność układu limbicznego i przedniej kory zakrętu obręczy"
    
    # Remove axes
    ax.axis('off')
    
    # Add title
    plt.title(title)
    plt.tight_layout()
    
    # Save the image
    img_path = os.path.join(output_dir, f"{type_id}_brain.png")
    plt.savefig(img_path)
    plt.close()
    
    return img_path

def split_text(text, max_length):
    """Split text into lines of maximum length."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
        
    return lines

if __name__ == "__main__":
    create_logo()
    create_default_avatar()
    create_neuroleader_type_images()
    print("All images created successfully!")
