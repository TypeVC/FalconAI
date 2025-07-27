import os
import time
from pathlib import Path
from typing import Optional
import pollinations
from PIL import Image

class ImageGenerator:
    """Enhanced image generator with better configuration and error handling."""
    
    def __init__(self, output_dir: str = "Database/Images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration
        self.config = {
            "model": "flux-cablyai",
            "width": 1024,
            "height": 1024,
            "enhance": False,
            "nologo": True,  # Changed to True for cleaner images
            "private": False,
            "seed": None,  # Use None for random seeds
        }
        
        self.default_negative = (
            "Anime, cartoony, childish, low quality, blurry, bad anatomy, "
            "bad hands, text, watermark, signature, poorly drawn"
        )
    
    def generate_image(self, prompt: str, negative: Optional[str] = None, 
                      filename: Optional[str] = None) -> Optional[str]:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description for image generation
            negative: Negative prompt to avoid certain elements
            filename: Custom filename (without extension)
            
        Returns:
            Path to generated image file or None if failed
        """
        if not prompt.strip():
            print("Error: Empty prompt provided")
            return None
            
        try:
            # Generate unique filename if not provided
            if filename is None:
                timestamp = int(time.time())
                filename = f"generated_image_{timestamp}"
            
            filepath = self.output_dir / f"{filename}.png"
            
            # Initialize image model with current config
            image_model = pollinations.image(
                model=self.config["model"],
                seed=self.config["seed"] or int(time.time()) % 10000,
                width=self.config["width"],
                height=self.config["height"],
                enhance=self.config["enhance"],
                nologo=self.config["nologo"],
                private=self.config["private"],
            )
            
            print(f"Generating image with prompt: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
            
            # Generate image
            image_model.generate(
                prompt=prompt,
                negative=negative or self.default_negative,
                save=True,
                file=str(filepath),
            )
            
            # Verify file was created
            if filepath.exists():
                print(f"Image successfully generated: {filepath}")
                return str(filepath)
            else:
                print("Error: Image file was not created")
                return None
                
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def open_image(self, filepath: str) -> bool:
        """
        Open an image file with the default system viewer.
        
        Args:
            filepath: Path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(filepath):
                print(f"Error: Image file does not exist: {filepath}")
                return False
                
            image = Image.open(filepath)
            image.show()
            print(f"Opened image: {filepath}")
            return True
            
        except Exception as e:
            print(f"Error opening image: {e}")
            return False
    
    def update_config(self, **kwargs):
        """Update configuration parameters."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                print(f"Updated {key} to {value}")
            else:
                print(f"Warning: Unknown config parameter '{key}' ignored")
    
    def list_generated_images(self):
        """List all generated images in the output directory."""
        images = list(self.output_dir.glob("*.png"))
        if images:
            print(f"Found {len(images)} generated images:")
            for img in sorted(images):
                print(f"  - {img.name}")
        else:
            print("No generated images found")
        return images

def interactive_mode(prompt):
    """Run the image generator in interactive mode."""
    generator = ImageGenerator()
    user_input = prompt
    # Generate and open image
    filepath = generator.generate_image(user_input)
    generator.open_image(filepath)


def main(prompt: str = None):
    """Main function - can be called programmatically or as standalone."""
    generator = ImageGenerator()
    
    if prompt:
        # Direct usage with provided prompt
        filepath = generator.generate_image(prompt)
        if filepath:
            generator.open_image(filepath)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main("A serene landscape with mountains and a river at sunset")