import os
from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(image_path):
    """
    Extracts metadata from an image file.

    :param image_path: Path to the image file
    :return: Dictionary containing metadata
    """
    metadata = {}
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value

    except Exception as e:
        print(f"Error extracting metadata from {image_path}: {e}")

    return metadata

def traverse_directory(directory):
    """
    Traverses a directory and extracts metadata from image files.

    :param directory: Path to the directory
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png', 'tiff', 'bmp', 'gif')):
                image_path = os.path.join(root, file)
                metadata = extract_metadata(image_path)
                print(f"Metadata for {image_path}:")
                for key, value in metadata.items():
                    print(f"  {key}: {value}")
                print("\n")

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ")
    traverse_directory(directory_path)
