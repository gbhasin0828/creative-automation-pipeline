import json
import yaml
from pathlib import Path
from typing import Dict, List

class CampaignBrief:
    def __init__(self, data: Dict):
        self.products: List[str] = data.get("products", [])
        self.message: str = data.get("message", "")
        self.region: str = data.get("region", "")
        self.audience: str = data.get("audience", "")
        self._validate()

    def _validate(self):
        if len(self.products) < 1:
            raise ValueError("Brief must contain at least 1 product.")
        if not self.message:
            raise ValueError("Brief must include a campaign message.")

def load_brief(filepath: str) -> CampaignBrief:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Brief file not found: {filepath}")
    with open(path, "r") as f:
        if path.suffix == ".json":
            data = json.load(f)
        elif path.suffix in [".yaml", ".yml"]:
            data = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    return CampaignBrief(data)
