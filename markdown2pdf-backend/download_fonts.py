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
    "OpenSans": {
        "regular": "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Regular.ttf",
        "bold": "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Bold.ttf",
        "italic": "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Italic.ttf",
        "bold_italic": "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-BoldItalic.ttf",
    },
    "SourceSansPro": {
        "regular": "https://github.com/adobe-fonts/source-sans/raw/release/TTF/SourceSansPro-Regular.ttf",
        "bold": "https://github.com/adobe-fonts/source-sans/raw/release/TTF/SourceSansPro-Bold.ttf",
        "italic": "https://github.com/adobe-fonts/source-sans/raw/release/TTF/SourceSansPro-It.ttf",
        "bold_italic": "https://github.com/adobe-fonts/source-sans/raw/release/TTF/SourceSansPro-BoldIt.ttf",
    },
    "WorkSans": {
        "regular": "https://github.com/weiweihuanghuang/Work-Sans/raw/master/fonts/static/TTF/WorkSans-Regular.ttf",
        "bold": "https://github.com/weiweihuanghuang/Work-Sans/raw/master/fonts/static/TTF/WorkSans-Bold.ttf",
        "italic": "https://github.com/weiweihuanghuang/Work-Sans/raw/master/fonts/static/TTF/WorkSans-Italic.ttf",
        "bold_italic": "https://github.com/weiweihuanghuang/Work-Sans/raw/master/fonts/static/TTF/WorkSans-BoldItalic.ttf",
    },
    "IBMPlexSans": {
        "regular": "https://github.com/IBM/plex/raw/master/packages/plex-sans/fonts/complete/ttf/IBMPlexSans-Regular.ttf",
        "bold": "https://github.com/IBM/plex/raw/master/packages/plex-sans/fonts/complete/ttf/IBMPlexSans-Bold.ttf",
        "italic": "https://github.com/IBM/plex/raw/master/packages/plex-sans/fonts/complete/ttf/IBMPlexSans-Italic.ttf",
        "bold_italic": "https://github.com/IBM/plex/raw/master/packages/plex-sans/fonts/complete/ttf/IBMPlexSans-BoldItalic.ttf",
    },
    "SourceCodePro": {
        "regular": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",
        "bold": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Bold.ttf",
        "italic": "https://github.com/adobe-fonts/source-code-pro/raw/release/OTF/SourceCodePro-It.otf",
        "bold_italic": "https://github.com/adobe-fonts/source-code-pro/raw/release/OTF/SourceCodePro-BoldIt.otf",
    },
    "Lato": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Bold.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Italic.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-BoldItalic.ttf",
    },
    "NunitoSans": {
        "regular": "https://github.com/googlefonts/NunitoSans/raw/main/fonts/ttf/NunitoSans-Regular.ttf",
        "bold": "https://github.com/googlefonts/NunitoSans/raw/main/fonts/ttf/NunitoSans-Bold.ttf",
        "italic": "https://github.com/googlefonts/NunitoSans/raw/main/fonts/ttf/NunitoSans-Italic.ttf",
        "bold_italic": "https://github.com/googlefonts/NunitoSans/raw/main/fonts/ttf/NunitoSans-BoldItalic.ttf",
    },
    # Apple SF-style fonts (Albert Sans available through Google Fonts API)
    "AlbertSans": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/albertsans/AlbertSans%5Bwght%5D.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/albertsans/AlbertSans%5Bwght%5D.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/albertsans/AlbertSans-Italic%5Bwght%5D.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/albertsans/AlbertSans-Italic%5Bwght%5D.ttf",
    },
    "HankenGrotesk": {
        "regular": "https://github.com/marcologous/hanken-grotesk/raw/master/fonts/ttf/HankenGrotesk-Regular.ttf",
        "bold": "https://github.com/marcologous/hanken-grotesk/raw/master/fonts/ttf/HankenGrotesk-Bold.ttf",
        "italic": "https://github.com/marcologous/hanken-grotesk/raw/master/fonts/ttf/HankenGrotesk-Italic.ttf",
        "bold_italic": "https://github.com/marcologous/hanken-grotesk/raw/master/fonts/ttf/HankenGrotesk-BoldItalic.ttf",
    },
    # Helvetica Neue-style fonts
    "Archivo": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo-Italic%5Bwdth,wght%5D.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo-Italic%5Bwdth,wght%5D.ttf",
    },
    "Manrope": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf",
    },
    "Barlow": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Regular.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Bold.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Italic.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-BoldItalic.ttf",
    },
    # Futura-style fonts (geometric sans serif)
    "Jost": {
        "regular": "https://github.com/google/fonts/raw/main/ofl/jost/Jost%5Bwght%5D.ttf",
        "bold": "https://github.com/google/fonts/raw/main/ofl/jost/Jost%5Bwght%5D.ttf",
        "italic": "https://github.com/google/fonts/raw/main/ofl/jost/Jost-Italic%5Bwght%5D.ttf",
        "bold_italic": "https://github.com/google/fonts/raw/main/ofl/jost/Jost-Italic%5Bwght%5D.ttf",
    },
    "Spartan": {
        "regular": "https://github.com/theleagueof/league-spartan/raw/master/fonts/ttf/LeagueSpartan-Regular.ttf",
        "bold": "https://github.com/theleagueof/league-spartan/raw/master/fonts/ttf/LeagueSpartan-Bold.ttf",
        "italic": "https://github.com/theleagueof/league-spartan/raw/master/fonts/ttf/LeagueSpartan-Regular.ttf",
        "bold_italic": "https://github.com/theleagueof/league-spartan/raw/master/fonts/ttf/LeagueSpartan-Bold.ttf",
    },
    "Formera": {
        "regular": "https://github.com/noirblancrouge/Formera/raw/master/fonts/ttf/Formera-Regular.ttf",
        "bold": "https://github.com/noirblancrouge/Formera/raw/master/fonts/ttf/Formera-Bold.ttf",
        "italic": "https://github.com/noirblancrouge/Formera/raw/master/fonts/ttf/Formera-Italic.ttf",
        "bold_italic": "https://github.com/noirblancrouge/Formera/raw/master/fonts/ttf/Formera-BoldItalic.ttf",
    },
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