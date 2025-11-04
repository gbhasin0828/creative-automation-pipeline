"""
Main pipeline orchestrator for creative automation.
"""
import os
from pathlib import Path

from .brief_parser import load_brief
from .asset_manager import AssetManager, _slug
from .image_generator import ImageGenerator
from .image_processor import ImageProcessor

class CreativePipeline:
    def __init__(self, assets_dir: str = "./assets", output_dir: str = "./outputs"):
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        self.asset_manager = AssetManager(assets_dir)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing API key; please enter it in the Streamlit sidebar.")
        project_id = os.getenv("OPENAI_PROJECT_ID")  # optional

        self.image_generator = ImageGenerator(api_key=api_key, project_id=project_id)
        self.image_processor = ImageProcessor()

    def run(self, brief_path: str) -> dict:
        brief = load_brief(brief_path)

        # Which products need generation?
        missing = self.asset_manager.get_missing_assets(brief.products)
        gen_dir = self.assets_dir / "generated"
        generated_count = 0

        if missing:
            for p in missing:
                self.image_generator.generate_product_image(p, gen_dir, brief.region, brief.audience)
                generated_count += 1

        processed = 0
        for p in brief.products:
            asset = self.asset_manager.find_asset(p)
            if asset is None:
                asset = self.assets_dir / "generated" / f"{_slug(p)}.png"
            if asset.exists():
                self.image_processor.process_product(asset, brief.message, self.output_dir, p)
                processed += 1

        return {
            "success": True,
            "products": brief.products,
            "generated_count": generated_count,
            "processed_count": processed,
            "total_assets": processed * 3,
            "output_dir": str(self.output_dir),
        }
