import os
import requests
from pathlib import Path

# Font URLs with correct paths
FONTS = {
    "Inter": {
        "regular": "https://rsms.me/inter/font-files/Inter-Regular.woff2",
        "bold": "https://rsms.me/inter/font-files/Inter-Bold.woff2",
        "italic": "https://rsms.me/inter/font-files/Inter-Italic.woff2",
        "bold_italic": "https://rsms.me/inter/font-files/Inter-BoldItalic.woff2",
    },
    "Roboto": {
        "regular": "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf",
        "bold": "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf",
        "italic": "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Italic.ttf",
        "bold_italic": "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-BoldItalic.ttf",
    },
    "SourceCodePro": {
        "regular": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",
        "bold": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Bold.ttf",
        "italic": "https://github.com/adobe-fonts/source-code-pro/raw/release/OTF/SourceCodePro-It.otf",
        "bold_italic": "https://github.com/adobe-fonts/source-code-pro/raw/release/OTF/SourceCodePro-BoldIt.otf",
    }
}

# Font directory
FONT_DIR = Path(__file__).parent / "app" / "static" / "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

def download_font(url, filename):
    output_path = FONT_DIR / filename
    print(f"Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded {filename} successfully")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def main():
    print(f"Downloading fonts to: {FONT_DIR}")
    
    for family, variants in FONTS.items():
        for style, url in variants.items():
            if style == "regular":
                filename = f"{family}-Regular.ttf"
            elif style == "bold":
                filename = f"{family}-Bold.ttf"
            elif style == "italic":
                filename = f"{family}-Italic.ttf"
            elif style == "bold_italic":
                filename = f"{family}-BoldItalic.ttf"
            
            # Handle the case of OTF files for Source Code Pro
            if ".otf" in url and ".ttf" in filename:
                filename = filename.replace(".ttf", ".otf")
            
            # Handle the case of WOFF2 files for Inter
            if ".woff2" in url and ".ttf" in filename:
                filename = filename.replace(".ttf", ".woff2")
            
            download_font(url, filename)

if __name__ == "__main__":
    main() 