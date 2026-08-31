import os
from PIL import Image, ImageDraw, ImageFont

def create_ppt_architecture_diagram():
    # 4K Ultra-HD Resolution for crisp PowerPoint Presentation Slides (3200 x 1800)
    width, height = 3200, 1800
    image = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark Slate background
    draw = ImageDraw.Draw(image)

    # Subtle Grid Dots Pattern
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255, 20))

    # Fonts with large, bold sizes for PPT clarity
    try:
        font_title = ImageFont.truetype("arial.ttf", 64)
        font_subtitle = ImageFont.truetype("arial.ttf", 32)
        font_stage_num = ImageFont.truetype("arial.ttf", 36)
        font_stage_title = ImageFont.truetype("arial.ttf", 40)
        font_item_title = ImageFont.truetype("arial.ttf", 30)
        font_item_sub = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = font_subtitle = font_stage_num = font_stage_title = font_item_title = font_item_sub = ImageFont.load_default()

    # Top Banner Header (PPT Slide Header)
    draw.rectangle([80, 60, 3120, 180], fill=(30, 41, 59, 230), outline=(255, 103, 31, 200), width=3)
    draw.text((120, 85), "GeMVerifier — System Architecture Overview", fill=(255, 255, 255, 255), font=font_title)
    draw.text((120, 155), "Automated Technical Verification Engine for Government e-Marketplace (GeM)", fill=(148, 163, 184, 255), font=font_subtitle)

    # 4 Main Stages side-by-side layout (Perfect for PPT Half-Slide view)
    stages = [
        {
            "num": "01",
            "title": "FRONTEND & PORTALS",
            "subtitle": "User Interface Layer",
            "accent": (255, 103, 31, 255), # Saffron
            "bg": (255, 103, 31, 25),
            "items": [
                ("🏛️ Buyer Portal", "Tender Notice & Bid Uploads"),
                ("🏢 Vendor Portal", "Seller Catalog Pre-Check"),
                ("📊 Compliance Matrix", "Side-by-Side Spec Comparison"),
                ("🤖 GeM-Bot Assistant", "Interactive AI Chat Drawer")
            ]
        },
        {
            "num": "02",
            "title": "API & SECURITY",
            "subtitle": "FastAPI Gateway",
            "accent": (99, 102, 241, 255), # Indigo
            "bg": (99, 102, 241, 25),
            "items": [
                ("⚡ FastAPI Gateway", "Async REST API Controllers"),
                ("🔐 Auth & JWT Engine", "SHA-256 Hasher + Bearer Tokens"),
                ("👤 Persona Manager", "Vendor / Buyer / Both Roles"),
                ("🛡️ Security & CORS", "Role-Based Access Control")
            ]
        },
        {
            "num": "03",
            "title": "AI VERIFICATION",
            "subtitle": "Core Processing Engine",
            "accent": (16, 185, 129, 255), # Emerald
            "bg": (16, 185, 129, 25),
            "items": [
                ("📄 pdfplumber Extractor", "Multi-column PDF Table Parsing"),
                ("📐 Rule & Spec Parser", "Min Core & Tolerance Checks"),
                ("🤖 Gemini 2.5 Pro", "Semantic Equivalence Matcher"),
                ("⚖️ Scoring Engine", "0-100% Score & Disqualification")
            ]
        },
        {
            "num": "04",
            "title": "DATA & EXPORT",
            "subtitle": "Persistence Layer",
            "accent": (59, 130, 246, 255), # Blue
            "bg": (59, 130, 246, 25),
            "items": [
                ("🗄️ SQLite Database", "SQLAlchemy User & Tender DB"),
                ("📁 Document Storage", "Raw Tender & Bid PDF Store"),
                ("📄 PDF Report Generator", "ReportLab Official PDF Export"),
                ("📊 Excel Exporter", "OpenPyXL Matrix Export")
            ]
        }
    ]

    col_width = 690
    gap = 70
    start_x = 80
    start_y = 230
    box_height = 1450

    for i, stage in enumerate(stages):
        x1 = start_x + i * (col_width + gap)
        x2 = x1 + col_width
        y1 = start_y
        y2 = y1 + box_height

        # Container Card
        draw.rectangle([x1, y1, x2, y2], fill=(15, 23, 42, 240), outline=stage["accent"], width=4)

        # Stage Header Box
        draw.rectangle([x1, y1, x2, y1 + 130], fill=stage["accent"])
        draw.text((x1 + 25, y1 + 20), stage["num"], fill=(255, 255, 255, 220), font=font_stage_num)
        draw.text((x1 + 90, y1 + 20), stage["title"], fill=(255, 255, 255, 255), font=font_stage_title)
        draw.text((x1 + 90, y1 + 75), stage["subtitle"], fill=(255, 255, 255, 220), font=font_subtitle)

        # Sub-Items inside each column
        item_y = y1 + 170
        for title, desc in stage["items"]:
            item_h = 270
            draw.rectangle([x1 + 25, item_y, x2 - 25, item_y + item_h], fill=(30, 41, 59, 220), outline=stage["accent"], width=2)
            draw.text((x1 + 45, item_y + 40), title, fill=(255, 255, 255, 255), font=font_item_title)
            draw.text((x1 + 45, item_y + 110), desc, fill=(148, 163, 184, 255), font=font_item_sub)
            item_y += item_h + 30

        # Flow Arrows between columns
        if i < len(stages) - 1:
            arrow_x1 = x2 + 10
            arrow_x2 = x2 + gap - 10
            arrow_y = y1 + box_height // 2
            
            # Thick Neon Arrow Line
            draw.line([(arrow_x1, arrow_y), (arrow_x2, arrow_y)], fill=(56, 189, 248, 255), width=8)
            draw.polygon([
                (arrow_x2 - 20, arrow_y - 20),
                (arrow_x2 + 15, arrow_y),
                (arrow_x2 - 20, arrow_y + 20)
            ], fill=(56, 189, 248, 255))

    # Save HD PNG for PPT Presentation Slide
    out_path_static = os.path.join("backend", "static", "gemverifier_ppt_architecture.png")
    out_path_artifact = os.path.join("C:\\Users\\LUVKESH\\.gemini\\antigravity\\brain\\bf68fb00-f885-4612-8424-8338356e2951", "gemverifier_ppt_architecture.png")

    image.save(out_path_static)
    image.save(out_path_artifact)
    print(f"PPT Slide Diagram saved to {out_path_static} and {out_path_artifact}")

if __name__ == "__main__":
    create_ppt_architecture_diagram()
