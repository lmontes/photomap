import pathlib
from PIL import Image

RAW_IMAGE_DIR = pathlib.Path("data/images")
BIG_IMAGE_DIR = pathlib.Path("public/images")
THUMBNAIL_DIR = pathlib.Path("public/thumbnails")


def transform_image_name(name):
    return name.replace("-", "").replace(" ", "").replace(".", "").replace("jpg", ".jpg")


for img_path in RAW_IMAGE_DIR.glob("*.jpg"):
    path = BIG_IMAGE_DIR / transform_image_name(img_path.name)
    if not path.exists():
        print(f"{img_path} -> {path}")
        image = Image.open(img_path)
        image.thumbnail((2160, 2160))
        image.save(path)

for img_path in RAW_IMAGE_DIR.glob("*.jpg"):
    path = THUMBNAIL_DIR / transform_image_name(img_path.name)
    if not path.exists():
        print(f"{img_path} -> {path}")
        image = Image.open(img_path)
        image.thumbnail((256, 256))
        image.save(path)
