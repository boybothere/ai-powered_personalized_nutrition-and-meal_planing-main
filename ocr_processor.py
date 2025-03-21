from PIL import Image
import pytesseract

# For Windows, specify the Tesseract path if necessary
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_ingredients(image):
    """
    Extracts text from an image using OCR.
    """
    try:
        img = Image.open(image)
        text = pytesseract.image_to_string(img)

        # Extract only the ingredient section if it exists
        ingredients_start = text.lower().find("ingredients")
        if ingredients_start != -1:
            ingredients = text[ingredients_start:]
        else:
            ingredients = text  # Fallback to full text

        return ingredients.strip()

    except Exception as e:
        return f"Error during OCR processing: {e}"
