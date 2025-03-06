# Quote Image Generator

A Python utility for generating minimalist quote images from text, perfect for social media posts, inspirational content, or creative projects.

![Example Quote Image](https://i.imgur.com/7MM3Eu0.png)

## Features

- Generate elegant, minimalist quote images with customizable styling
- Process multiple quotes in batch from a text file
- Preserve line breaks and paragraph formatting from your original quotes
- Automatic text sizing to fit quotes of any length
- Left-aligned text with clean, modern styling
- Custom attribution text (e.g., "12 am Stories")
- Font fallback system to ensure compatibility across systems
- Progress bar visualization for batch processing

## Requirements

- Python 3.6+
- Pillow (PIL Fork) library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/quote_generator.git
   cd quote_generator
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install pillow
   ```

4. Make sure you have a fonts directory with at least one font file. The default is "fonts/JosefinSans-Light.ttf".

## Usage

### Preparing Your Quotes

Create a text file (e.g., `quotes.txt`) with your quotes separated by `---`, like this:

```
Life is what happens when you're busy making other plans.

- John Lennon
---
The only way to do great work is to love what you do.
---
Be the change that you wish to see in the world.
```

### Generating Images

Run the script to generate images for all quotes in your file:

```
python create.py
```

By default, this will:
- Read quotes from `quotes.txt`
- Save images to the `quote_images` folder
- Use "12 am Stories" as the attribution text
- Create 1080×1080 pixel images

### Customizing Output

Edit the function call at the bottom of `create.py` to customize:

```python
batch_create_quote_images(
    "quotes.txt",                     # Input file
    output_folder="custom_folder",    # Custom output folder
    author_text="Your Brand Name",    # Custom attribution
    image_size=(1200, 800),           # Custom dimensions
    font_size=70,                     # Custom font size
    font_path="fonts/YourFont.ttf"    # Custom font
)
```

### Single Image Generation

You can also programmatically generate a single image:

```python
create_quote_image(
    quote_text="Your quote text here",
    author_text="Your attribution",
    output_filename="my_quote.png",
    image_size=(1080, 1080),
    background_color="black",
    text_color="white",
    font_size=80
)
```

## Project Structure

```
quote_generator/
│
├── create.py          # Main script
├── quotes.txt         # Input quotes file
├── fonts/             # Directory for font files
│   └── JosefinSans-Light.ttf
│
└── quote_images/      # Output directory (created automatically)
    ├── quote_1.png
    ├── quote_2.png
    └── ...
```

## Advanced Options

The `create_quote_image()` function supports these additional parameters:

- `background_color`: Image background color (default: "black")
- `text_color`: Quote text color (default: "white")
- `padding`: Margin around text (default: 120px)
- `line_spacing`: Space between text lines (default: 18px)
- `author_font_size`: Size for attribution text (default: 40px)
- `border`: Debug option to show text boundaries (default: False)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
