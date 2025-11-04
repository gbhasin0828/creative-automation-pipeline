"""
Streamlit web interface for Creative Automation Pipeline.
Run with: streamlit run app.py
"""
import os
import json
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI
from src.pipeline import CreativePipeline

# ---------------- Page ----------------
st.set_page_config(page_title="Creative Automation Pipeline", page_icon="🎨", layout="wide")
st.title("🎨 Creative Automation Pipeline")

# ---------------- Sidebar: credentials ----------------
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
project_id = st.sidebar.text_input("OpenAI Project ID (proj_…)", help="Exact ID from Console → Projects (optional but recommended)")

if not api_key:
    st.warning("Enter your OpenAI API key to continue.")
    st.stop()

# Store for process (do NOT clear env; respect proxies/CA bundles)
os.environ["OPENAI_API_KEY"] = api_key
if project_id:
    os.environ["OPENAI_PROJECT_ID"] = project_id

# Client bound to the chosen project
client = OpenAI(api_key=api_key, project=(project_id or None))
st.sidebar.caption(f"Key prefix: {api_key[:8]}…  |  Project: {project_id or 'default routing'}")

# ---------------- Connectivity + billing probe ----------------
try:
    # Auth / network
    _ = list(client.models.list())
    st.sidebar.success("✅ Connection successful")
    # Tiny paid call to surface billing limits
    client.images.generate(model="gpt-image-1", prompt="gray square", size="1024x1024")
    st.sidebar.success("✅ Billing active")
except Exception as e:
    st.sidebar.error(f"❌ API test failed: {type(e).__name__}: {e}")
    st.stop()

# ---------------- Brief inputs ----------------
st.header("Campaign Brief")
col1, col2 = st.columns(2)
with col1:
    products_input = st.text_area("Products (one per line)", height=100)
    campaign_message = st.text_input("Campaign Message")
with col2:
    region = st.text_input("Region / Market", value="North America")
    audience = st.text_input("Target Audience", value="Millennials")

# ---------------- Optional uploads ----------------
st.header("Product Assets (Optional)")
uploaded_files = st.file_uploader(
    "Upload existing product images",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
)

# ---------------- Run pipeline ----------------
st.markdown("---")
if st.button("Generate Campaign Assets", type="primary"):
    products = [p.strip() for p in products_input.split("\n") if p.strip()]
    if not products:
        st.error("Enter at least one product.")
        st.stop()
    if not campaign_message:
        st.error("Enter a campaign message.")
        st.stop()

    brief = {
        "products": products,
        "message": campaign_message,
        "region": region,
        "audience": audience,
    }

    assets_dir = Path("./assets")
    assets_dir.mkdir(exist_ok=True)
    if uploaded_files:
        for f in uploaded_files:
            with open(assets_dir / f.name, "wb") as out:
                out.write(f.getbuffer())

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(brief, tmp, indent=2)
        brief_path = tmp.name

    try:
        with st.spinner("Generating campaign assets..."):
            pipeline = CreativePipeline()
            results = pipeline.run(brief_path)

        st.success("✅ Done!")
        outdir = Path(results["output_dir"])
        for product in results["products"]:
            st.subheader(product)
            pdir = outdir / product
            if pdir.exists():
                cols = st.columns(3)
                for idx, ratio in enumerate(["square", "story", "landscape"]):
                    files = list(pdir.glob(f"{ratio}_*.png"))
                    if files:
                        with cols[idx]:
                            st.image(str(files[0]), caption=ratio.title(), width="stretch")
        st.info(f"All assets saved to: `{results['output_dir']}`")
    except Exception as e:
        st.error(str(e))
    finally:
        Path(brief_path).unlink(missing_ok=True)
