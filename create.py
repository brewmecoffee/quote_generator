from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import sys
import time

# Global font cache for better performance
FONT_CACHE = {}

def load_font(font_path, font_size):
    """
    Load a font with fallback options. Uses a global cache to avoid reloading fonts.
    
    Parameters:
    - font_path: Path to the desired font file
    - font_size: Size of the font to load
    
    Returns:
    - The loaded font object
    """
    # Check if this font+size combination is in the cache
    cache_key = f"{font_path}_{font_size}"
    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]
    
    try:
        # First try the specified font path
        font = ImageFont.truetype(font_path, font_size)
        print(f"Using font from: {font_path}")
        
    except Exception as e:
        print(f"Failed to load font from {font_path}: {e}")
        font = None
        
        # Try a sequence of fallback options
        fallback_options = [
            # Check for JosefinSans in current directory
            ("JosefinSans-Regular.ttf", None),
            # Common Windows font
            ("arial.ttf", None),
            # macOS
            ("Arial.ttf", None),
            # Linux
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", None),
        ]
        
        for font_file, custom_message in fallback_options:
            try:
                font = ImageFont.truetype(font_file, font_size)
                message = custom_message or f"Using {font_file} as fallback"
                print(message)
                break
            except Exception:
                continue
        
        # Last resort: use default font
        if font is None:
            font = ImageFont.load_default()
            print("Using default font as fallback")
    
    # Cache the font for future use
    FONT_CACHE[cache_key] = font
    return font

def validate_parameters(image_size, font_size, author_font_size, padding):
    """
    Validate input parameters to ensure they make sense.
    
    Parameters:
    - image_size: Tuple of (width, height)
    - font_size: Size of the quote text
    - author_font_size: Size of the author text
    - padding: Padding from the edges
    
    Returns:
    - True if parameters are valid, False otherwise
    """
    if not isinstance(image_size, tuple) or len(image_size) != 2:
        print("Error: image_size must be a tuple of (width, height)")
        return False
    
    if image_size[0] <= 0 or image_size[1] <= 0:
        print("Error: image dimensions must be positive")
        return False
        
    if font_size <= 0 or author_font_size <= 0:
        print("Error: font sizes must be positive")
        return False
        
    if padding < 0 or padding * 2 >= min(image_size):
        print("Error: invalid padding value")
        return False
        
    # Check if text area would be too small
    if image_size[0] - (2 * padding) <= 0 or image_size[1] - (2 * padding) - author_font_size - 40 <= 0:
        print("Error: padding is too large for the image size")
        return False
        
    return True

def create_quote_image(quote_text, author_text="12 am Stories", output_filename="quote.png", 
                      image_size=(1080, 1080), background_color="black", 
                      text_color="white", font_path="fonts/JosefinSans-Light.ttf", font_size=80,
                      author_font_size=40, padding=120, line_spacing=18, border=False):
    """
    Create a minimalist quote image with left-aligned text on a black background.
    
    Parameters:
    - quote_text: The quote to display
    - author_text: The attribution text (appears at bottom)
    - output_filename: The filename to save the image
    - image_size: Tuple of (width, height)
    - background_color: Image background color
    - text_color: Text color
    - font_path: Path to a font file (default: 'fonts/JosefinSans-Light.ttf')
    - font_size: Size of the quote text
    - author_font_size: Size of the author text
    - padding: Padding from the edges
    - line_spacing: Spacing between lines
    - border: Whether to draw a border around the text area (for debugging)
    
    Returns:
    - Path to the created image file or None if an error occurred
    """
    # Validate parameters
    if not validate_parameters(image_size, font_size, author_font_size, padding):
        return None
    
    try:
        # Create a new image with the specified background color
        img = Image.new('RGB', image_size, color=background_color)
        draw = ImageDraw.Draw(img)
        
        # Define the text box dimensions
        text_box_margin = padding
        text_box_width = image_size[0] - (2 * text_box_margin)
        text_box_height = image_size[1] - (2 * text_box_margin) - author_font_size - 40  # Leave space for author
        
        # Draw border if requested (for debugging)
        if border:
            draw.rectangle(
                [(text_box_margin, text_box_margin), 
                 (image_size[0] - text_box_margin, image_size[1] - text_box_margin - author_font_size - 40)], 
                outline="yellow", width=3
            )
        
        # Adaptive font sizing - start with the provided font size and reduce until text fits
        current_font_size = font_size
        lines = []
        fits = False
        
        while not fits and current_font_size > 20:  # Minimum font size
            # Load the font for this size
            quote_font = load_font(font_path, current_font_size)
            
            # Calculate maximum width for text wrapping
            max_width = text_box_width
            
            # Wrap the quote text respecting newlines
            paragraphs = quote_text.split('\n')
            lines = []
            
            for paragraph in paragraphs:
                # If the paragraph is empty, add a blank line to preserve spacing
                if not paragraph.strip():
                    lines.append('')
                    continue
                    
                words = paragraph.split()
                current_line = []
                
                for word in words:
                    # Try adding the word to the current line
                    test_line = ' '.join(current_line + [word])
                    
                    # Check if the line with the new word fits within max_width
                    try:
                        line_width = quote_font.getlength(test_line)
                    except:
                        # Fallback for older Pillow versions
                        try:
                            line_width = sum(quote_font.getbbox(char)[2] for char in test_line)
                        except:
                            # Last resort fallback
                            line_width = len(test_line) * (current_font_size // 2)
                    
                    if line_width <= max_width:
                        current_line.append(word)
                    else:
                        # Line is too long, start a new one
                        if current_line:  # Don't add empty lines
                            lines.append(' '.join(current_line))
                        current_line = [word]
                
                # Add the last line if it's not empty
                if current_line:
                    lines.append(' '.join(current_line))
            
            # Calculate text position
            line_height = current_font_size + line_spacing
            total_text_height = len(lines) * line_height
            
            # Check if the text fits vertically
            if total_text_height <= text_box_height:
                fits = True
            else:
                current_font_size -= 5  # Reduce font size and try again
        
        # Position the text to be centered within the text box, but each line left-aligned
        y_position = text_box_margin + (text_box_height - total_text_height) // 2
        x_position = text_box_margin  # Left margin
        
        # Draw each line of text left-aligned
        for line in lines:
            draw.text((x_position, y_position), line, fill=text_color, font=quote_font)
            y_position += line_height
        
        # Load the author font
        author_font = load_font(font_path, author_font_size)
        
        # Draw the author text at the bottom left
        author_x = padding  # Left align at padding
        author_y = image_size[1] - padding
        
        draw.text(
            (author_x, author_y - author_font_size),
            author_text,
            fill=text_color,
            font=author_font
        )
        
        # Save the image
        output_dir = os.path.dirname(output_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        img.save(output_filename)
        return output_filename
        
    except Exception as e:
        print(f"Error creating quote image: {e}")
        return None

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create a progress bar in the console.
    
    Parameters:
    - iteration: Current iteration (Int)
    - total: Total iterations (Int)
    - prefix: Prefix string (Str)
    - suffix: Suffix string (Str)
    - length: Character length of bar (Int)
    - fill: Bar fill character (Str)
    """
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
    # Print a new line when complete
    if iteration == total:
        print()

def batch_create_quote_images(quotes_file, output_folder="quote_images", 
                             author_text="12 am Stories", image_size=(1080, 1080),
                             font_size=80, font_path="fonts/JosefinSans-Light.ttf", border=False):
    """
    Process a text file with quotes separated by '---' delimiters and create 
    an image for each quote.
    
    The text file should have quotes separated by '---' like this:
    
    First quote text here
    which can span multiple lines
    ---
    Second quote text here
    ---
    Third quote text here
    
    Parameters:
    - quotes_file: Path to the text file containing quotes separated by '---'
    - output_folder: Folder to save the generated images
    - author_text: Attribution text for all images
    - image_size: Size of the output images (width, height)
    - font_size: Size of the quote text
    - font_path: Path to a font file
    - border: Whether to draw a border around the text area (for debugging)
    
    Returns:
    - Number of successfully created images
    """
    # Create output folder if it doesn't exist
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except Exception as e:
        print(f"Error creating output folder: {e}")
        return 0
    
    # Read quotes from file
    try:
        if not os.path.exists(quotes_file):
            print(f"Error: Quotes file '{quotes_file}' not found")
            return 0
            
        with open(quotes_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading quotes file: {e}")
        return 0
    
    # Split content by '---' separator
    quotes = [quote.strip() for quote in content.split('---') if quote.strip()]
    
    if not quotes:
        print(f"No quotes found in {quotes_file}")
        return 0
        
    print(f"Found {len(quotes)} quotes in the file.")
    
    # Create an image for each quote
    success_count = 0
    for i, quote in enumerate(quotes):
        # Display progress bar
        print_progress_bar(i, len(quotes), prefix='Progress:', suffix=f'Quote {i+1}/{len(quotes)}', length=40)
        
        output_filename = os.path.join(output_folder, f"quote_{i+1}.png")
        result = create_quote_image(
            quote_text=quote,
            author_text=author_text,
            output_filename=output_filename,
            image_size=image_size,
            font_size=font_size,
            font_path=font_path,
            border=border
        )
        
        if result:
            success_count += 1
    
    # Complete the progress bar
    print_progress_bar(len(quotes), len(quotes), prefix='Progress:', suffix='Complete', length=40)
    print(f"Successfully created {success_count}/{len(quotes)} quote images in '{output_folder}' folder.")
    return success_count

# Example usage
if __name__ == "__main__":
    # Process quotes from a file where quotes are separated by '---'
    batch_create_quote_images(
        "quotes.txt", 
        font_size=80,
        font_path="fonts/JosefinSans-Light.ttf"
    )