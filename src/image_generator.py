import time
import base64
from pathlib import Path
from dataclasses import dataclass
from PIL import Image, ImageDraw
from openai import OpenAI, RateLimitError, BadRequestError

def _slug(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-")

@dataclass
class ImageGenConfig:
    model: str = "gpt-image-1"
    size: str = "1024x1024"
    throttle_secs: float = 13.0  # ~5 images/min

class ImageGenerator:
    def __init__(self, api_key: str, project_id: str | None = None, config: ImageGenConfig | None = None):
        if not api_key:
            raise ValueError("API key required from Streamlit.")
        # Bind client to the explicit project if provided
        self.client = OpenAI(api_key=api_key, project=(project_id or None))
        self.config = config or ImageGenConfig()

    def _placeholder(self, text: str, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (1024, 1024), (240, 240, 240))
        d = ImageDraw.Draw(img)
        d.text((40, 40), "Placeholder", fill=(0, 0, 0))
        d.text((40, 100), text[:280], fill=(0, 0, 0))
        img.save(path)
        return path

    def generate_product_image(self, product_name: str, output_dir: Path, region: str = "", audience: str = "") -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{_slug(product_name)}.png"
        outpath = output_dir / fname
        if outpath.exists():
            return outpath

        prompt = f"Professional marketing image of {product_name}. Clean studio lighting, modern commercial look."
        if region: prompt += f" Target market: {region}."
        if audience: prompt += f" Target audience: {audience}."

        backoff = 2
        while True:
            try:
                resp = self.client.images.generate(
                    model=self.config.model,
                    prompt=prompt,
                    size=self.config.size,
                    n=1,
                )
                b64 = resp.data[0].b64_json
                with open(outpath, "wb") as f:
                    f.write(base64.b64decode(b64))
                time.sleep(self.config.throttle_secs)
                return outpath

            except RateLimitError as e:
                wait = backoff
                try:
                    wait = int(getattr(e, "response", None).headers.get("retry-after", backoff))  # type: ignore[attr-defined]
                except Exception:
                    pass
                time.sleep(wait)
                backoff = min(backoff * 2, 30)

            except BadRequestError as e:
                msg = str(e).lower()
                if "billing_hard_limit_reached" in msg:
                    return self._placeholder(f"{product_name} (billing cap reached)", outpath)
                if "model_not_found" in msg:
                    return self._placeholder(f"{product_name} (model unavailable)", outpath)
                return self._placeholder(f"{product_name} (error)", outpath)

            except Exception:
                return self._placeholder(f"{product_name} (error)", outpath)
