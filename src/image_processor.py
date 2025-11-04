from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple

class ImageProcessor:
    ASPECT_RATIOS = {
        "square": (1080, 1080),
        "story": (1080, 1920),
        "landscape": (1920, 1080),
    }

    def resize_to_aspect_ratio(self, image_path: Path, target_size: Tuple[int, int]) -> Image.Image:
        img = Image.open(image_path).convert("RGB")
        tw, th = target_size
        tr = tw / th
        w, h = img.size
        r = w / h
        if r > tr:
            new_w = int(h * tr)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / tr)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        return img

    def overlay_text(self, image: Image.Image, message: str) -> Image.Image:
        img = image.copy()
        draw = ImageDraw.Draw(img, "RGBA")
        w, h = img.size
        try:
            font_size = int(w * 0.05)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), message, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = int(w * 0.05)
        x = (w - tw) // 2
        y = h - th - pad * 2
        bg = [x - pad, y - pad, x + tw + pad, y + th + pad]
        draw.rectangle(bg, fill=(0, 0, 0, 180))
        draw.text((x, y), message, fill=(255, 255, 255, 255), font=font)
        return img

    def process_product(self, image_path: Path, message: str, output_dir: Path, product_name: str):
        product_dir = output_dir / product_name
        product_dir.mkdir(parents=True, exist_ok=True)
        for ratio, size in self.ASPECT_RATIOS.items():
            resized = self.resize_to_aspect_ratio(image_path, size)
            final = self.overlay_text(resized, message)
            out = product_dir / f"{ratio}_{size[0]}x{size[1]}.png"
            final.save(out, quality=95)
            print(f"  ✓ {ratio}: {out}")
