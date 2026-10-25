import cv2
import pathlib

RAW_IMAGE_DIR = pathlib.Path("data/images")
BIG_IMAGE_DIR = pathlib.Path("public/images")
THUMBNAIL_DIR = pathlib.Path("public/thumbnails")


def transform_image_name(name):
    return (
        name.replace("-", "")
        .replace(" ", "")
        .replace(".", "")
        .replace("jpg", ".jpg")
    )


def resize_image(img_path, target_path, max_size):
    # cv2.imread carga la imagen. Si está corrupta o no existe, devuelve None
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"Error: No se pudo leer la imagen {img_path}")
        return

    # Obtener dimensiones actuales (alto, ancho)
    h, w = img.shape[:2]

    # Calcular el factor de escala manteniendo la relación de aspecto
    scale = max_size / max(h, w)

    # Si la imagen ya es más pequeña que el objetivo, opcionalmente podrías saltarte el reescalado,
    # pero para replicar .thumbnail() de Pillow que reduce, calculamos las nuevas dimensiones:
    new_w = int(w * scale)
    new_h = int(h * scale)

    # cv2.INTER_AREA es el mejor método de interpolación para reducir tamaño (evita moiré)
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Guardar la imagen optimizada
    cv2.imwrite(str(target_path), resized_img)


def process_images(target_dir, max_size):
    # Asegura que el directorio de destino exista
    target_dir.mkdir(parents=True, exist_ok=True)

    for img_path in RAW_IMAGE_DIR.glob("*.jpg"):
        path = target_dir / transform_image_name(img_path.name)

        if not path.exists():
            print(f"{img_path} -> {path}")
            try:
                resize_image(img_path, path, max_size)
            except Exception as e:
                print(f"Error inesperado en {img_path}: {e}")


# Procesar imágenes grandes (máximo 2160px)
process_images(BIG_IMAGE_DIR, 2160)

# Procesar miniaturas (máximo 256px)
process_images(THUMBNAIL_DIR, 256)
