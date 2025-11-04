from pathlib import Path
from typing import Optional, List

def _slug(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-")

class AssetManager:
    def __init__(self, assets_dir: str = "./assets"):
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def find_asset(self, product_name: str) -> Optional[Path]:
        exts = [".png", ".jpg", ".jpeg", ".webp"]
        slug = _slug(product_name)

        for base in [self.assets_dir, self.assets_dir / "generated"]:
            for name in [product_name, slug]:
                for ext in exts:
                    p = base / f"{name}{ext}"
                    if p.exists():
                        return p
        return None

    def get_missing_assets(self, products: List[str]) -> List[str]:
        return [p for p in products if self.find_asset(p) is None]
