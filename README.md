🚀 Creative Automation Pipeline
🎯 Overview

The Creative Automation Pipeline is a Streamlit app that helps marketers, designers, and product managers instantly create marketing campaign images using OpenAI’s DALL·E 3.

You simply describe your products and campaign message — the app generates polished campaign visuals in multiple sizes, with or without AI-generated product images.

The app supports:

✅ Auto image generation via DALL·E 3

✅ Uploading your own product photos (skips AI generation)

✅ Auto resizing and caption overlays (square, story, and landscape)

✅ Organized outputs in /outputs/<product_name>/

🧭 How to Use
🪄 Streamlit App Inputs
Field	Description	Example
OpenAI API Key	- I will provide this in a separate email or you can use your own. 
OpenAI Project ID (Optional)	Leave blank unless your organization uses multiple OpenAI projects	(blank)
Products (one per line)	List one or more product names — each will generate its own set of assets	Eco Bottle
Pepsi Bottle
Campaign Message	A short tagline or marketing message to overlay on each image	Join PepsiCo’s sustainability revolution!
Product Assets (Optional)	Upload existing images if you don’t want the AI to generate new ones.
File names must match product names.	Upload eco-bottle.png or eco-bottle.jpg
🧠 Example — End-to-End Flow

Let’s say you want to create assets for an upcoming sustainability campaign.

1️⃣ Enter Products

Eco Bottle
Pepsi Bottle


2️⃣ Enter Campaign Message

Join PepsiCo’s sustainability revolution.


3️⃣ Upload Product Assets (optional)

Upload an image file named eco-bottle.png

Leave pepsi bottle without an image → DALL·E 3 will auto-generate it.

4️⃣ Click Generate Campaign Assets

💥 The app will:

Detect uploaded assets (uses them directly)

Generate missing ones using OpenAI DALL·E 3

Overlay your campaign message

Produce 3 images per product:

Square (1080×1080)

Story (1080×1920)

Landscape (1920×1080)

Save all results in /outputs/<product_name>/

🧾 Output Example

After running, you’ll find:

outputs/
├── Eco Bottle/
│   ├── square_1080x1080.png
│   ├── story_1080x1920.png
│   └── landscape_1920x1080.png
└── Pepsi Bottle/
    ├── square_1080x1080.png
    ├── story_1080x1920.png
    └── landscape_1920x1080.png


You’ll also see a preview of each image in the Streamlit UI.

💡 Features Summary

✅ Simple Streamlit UI for configuration and user inputs
✅ Uses OpenAI DALL·E 3 for image generation
✅ Automatically overlays text and resizes assets
✅ Allows manual uploads to skip AI generation
✅ Generates three formats per product
✅ Organizes output files automatically

📁 Folder Structure
creative-automation-pipeline/
│
├── app.py                   # Streamlit UI entry point
├── requirements.txt          # Python dependencies
├── .gitignore
│
├── src/
│   ├── asset_manager.py      # Manages product image assets
│   ├── brief_parser.py       # Parses campaign brief input
│   ├── image_generator.py    # Handles OpenAI image generation
│   ├── image_processor.py    # Resizes and adds text overlays
│   └── pipeline.py           # Orchestrates the workflow
│
├── assets/                   # User-uploaded or pre-existing product assets
│   └── .gitkeep
│
└── outputs/                  # Generated campaign images
    └── .gitkeep

💻 Local Setup (for Users)
1️⃣ Clone the repository
git clone https://github.com/gbhasin0828/creative-automation-pipeline.git
cd creative-automation-pipeline

2️⃣ Create and activate a virtual environment

Windows PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1


macOS / Linux

python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app.py


Then open http://localhost:8501
 in your browser.

⚙️ Requirements
Tool	Version
Python	3.10+
Streamlit	1.38+
OpenAI SDK	1.35+
Pillow	10.1.0+

All dependencies are listed in requirements.txt.

