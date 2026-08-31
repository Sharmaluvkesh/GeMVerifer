import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_user_avatar_badge(draw, x, y, w, h, icon_text, title, subtitle, bg_color, border_color, font_title, font_sub):
    # Rounded card badge for User Persona instead of stickman
    draw.rectangle([x, y, x+w, y+h], fill=bg_color, outline=border_color, width=3)
    # Icon circle inside badge
    draw.ellipse([x+w//2-35, y+25, x+w//2+35, y+95], fill=border_color)
    draw.text((x+w//2-18, y+35), icon_text, fill=(255, 255, 255, 255), font=font_title)
    
    # Title & Subtitle text
    tw = len(title) * 7
    draw.text((x+w//2 - tw, y+110), title, fill=(255, 255, 255, 255), font=font_title)
    sw = len(subtitle) * 5
    draw.text((x+w//2 - sw, y+150), subtitle, fill=(226, 232, 240, 255), font=font_sub)

def draw_3d_cube_rich(draw, x, y, w, h, depth, font_main):
    # Front face (Royal Navy Blue)
    front = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    draw.polygon(front, fill=(15, 30, 75, 255), outline=(255, 103, 31, 255), width=3)
    
    # Top face (Saffron Orange)
    top = [(x, y), (x+depth, y-depth), (x+w+depth, y-depth), (x+w, y)]
    draw.polygon(top, fill=(255, 103, 31, 255), outline=(15, 30, 75, 255), width=3)

    # Right side face (Dark Blue Accent)
    side = [(x+w, y), (x+w+depth, y-depth), (x+w+depth, y+h-depth), (x+w, y+h)]
    draw.polygon(side, fill=(9, 18, 48, 255), outline=(255, 103, 31, 255), width=3)

    # Text in front face
    draw.text((x + 20, y + h//2 - 25), "⚡ FastAPI Gateway", fill=(255, 255, 255, 255), font=font_main)
    draw.text((x + 20, y + h//2 + 10), "& Security Engine", fill=(255, 180, 120, 255), font=font_main)

def create_final_architecture_diagram():
    # 3200 x 1400 Canvas
    width, height = 3200, 1400
    
    # Light background with subtle slate grid
    image = Image.new("RGBA", (width, height), (248, 250, 252, 255))
    draw = ImageDraw.Draw(image)

    # Subtle Grid Lines
    grid_size = 40
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=(226, 232, 240, 255), width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=(226, 232, 240, 255), width=1)

    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 48)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_label = ImageFont.truetype("arial.ttf", 22)
        font_box_title = ImageFont.truetype("arial.ttf", 26)
        font_box_sub = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_subtitle = font_label = font_box_title = font_box_sub = ImageFont.load_default()

    # Clean Official Header (NO AI or Light Theme mention)
    draw.text((80, 45), "GeMVerifier — System Architecture Diagram", fill=(11, 30, 54, 255), font=font_title)
    draw.text((80, 105), "Government e-Marketplace Automated Technical Evaluation Platform", fill=(71, 85, 105, 255), font=font_subtitle)

    # 1. Left Actor: Professional Procurement Officer Avatar Badge
    draw_user_avatar_badge(
        draw, 80, 580, 280, 200, "🏛️", 
        "Buyer Portal", "Procurement Officer", 
        (255, 103, 31, 255), (194, 65, 12, 255), 
        font_box_title, font_box_sub
    )

    # Arrow from Left Avatar Badge to 3D Gateway Cube
    draw.line([(360, 680), (520, 680)], fill=(15, 23, 42, 255), width=3)
    draw.polygon([(510, 670), (530, 680), (510, 690)], fill=(15, 23, 42, 255))

    # 2. Central 3D Cube Box (FastAPI Gateway)
    draw_3d_cube_rich(draw, 540, 580, 300, 200, 50, font_label)

    # 3. Middle Column: 4 ALL-COLORED VIBRANT GRADIENT CARDS (AI Processing Pipeline)
    mid_boxes = [
        ("📄 pdfplumber Table Extractor", "Parses multi-column PDF tables & text", (255, 103, 31, 255), (234, 88, 12, 255)),   # Saffron Orange
        ("📐 Rule & Spec Evaluator", "Min core count & tolerance (+/- %) checks", (4, 106, 56, 255), (22, 101, 52, 255)),   # Emerald Green
        ("🤖 Gemini 2.5 Pro Matcher", "Semantic technical spec equivalence", (2, 132, 199, 255), (3, 105, 161, 255)),       # Cyan Blue
        ("⚖️ Compliance Scoring Engine", "0-100% score & disqualification rationale", (79, 70, 229, 255), (67, 56, 202, 255)) # Indigo
    ]

    mid_box_x = 1150
    mid_box_w = 640
    mid_box_h = 135
    box_gap = 45
    start_y = 350

    for i, (title, desc, fill_color, border_color) in enumerate(mid_boxes):
        by = start_y + i * (mid_box_h + box_gap)
        cy = by + mid_box_h // 2

        # Draw FULLY COLORED VIBRANT BLOCK
        draw.rectangle([mid_box_x, by, mid_box_x + mid_box_w, by + mid_box_h], fill=fill_color, outline=border_color, width=3)
        draw.text((mid_box_x + 30, by + 30), title, fill=(255, 255, 255, 255), font=font_box_title)
        draw.text((mid_box_x + 30, by + 75), desc, fill=(241, 245, 249, 255), font=font_box_sub)

        # Fanning arrows from 3D Cube (x=890, y=680) to each middle box (x=1150, y=cy)
        draw.line([(890, 680), (mid_box_x - 10, cy)], fill=(15, 23, 42, 255), width=3)
        # Arrowhead
        angle = math.atan2(cy - 680, mid_box_x - 10 - 890)
        ax1 = (mid_box_x - 10) - 15 * math.cos(angle - 0.3)
        ay1 = cy - 15 * math.sin(angle - 0.3)
        ax2 = (mid_box_x - 10) - 15 * math.cos(angle + 0.3)
        ay2 = cy - 15 * math.sin(angle + 0.3)
        draw.polygon([(mid_box_x - 10, cy), (ax1, ay1), (ax2, ay2)], fill=(15, 23, 42, 255))

    # 4. Right Column: 4 ALL-COLORED VIBRANT GRADIENT CARDS (Outputs & User Views)
    right_boxes = [
        ("🖥️ Command Dashboard View", "Live pop-out vendor evaluation cards", (30, 58, 138, 255), (30, 48, 110, 255)),   # Royal Navy
        ("📊 Compliance Verification Matrix", "Side-by-side spec comparison table", (217, 119, 6, 255), (180, 83, 9, 255)),   # Amber Gold
        ("🤖 GeM-Bot Interactive Drawer", "AI Assistant chat modal for queries", (234, 88, 12, 255), (194, 65, 12, 255)),    # Saffron Orange
        ("📥 PDF & Excel Exporter", "Official ReportLab PDF & Excel sheets", (22, 163, 74, 255), (21, 128, 61, 255))       # Forest Green
    ]

    right_box_x = 2050
    right_box_w = 640

    for i, (title, desc, fill_color, border_color) in enumerate(right_boxes):
        by = start_y + i * (mid_box_h + box_gap)
        cy = by + mid_box_h // 2

        # Draw FULLY COLORED VIBRANT BLOCK
        draw.rectangle([right_box_x, by, right_box_x + right_box_w, by + mid_box_h], fill=fill_color, outline=border_color, width=3)
        draw.text((right_box_x + 30, by + 30), title, fill=(255, 255, 255, 255), font=font_box_title)
        draw.text((right_box_x + 30, by + 75), desc, fill=(241, 245, 249, 255), font=font_box_sub)

        # Connecting straight horizontal arrows between Middle Column and Right Column
        draw.line([(mid_box_x + mid_box_w + 10, cy), (right_box_x - 10, cy)], fill=(15, 23, 42, 255), width=3)
        draw.polygon([(right_box_x - 20, cy - 8), (right_box_x - 5, cy), (right_box_x - 20, cy + 8)], fill=(15, 23, 42, 255))

    # 5. Right Actor: Professional Vendor Avatar Badge
    draw_user_avatar_badge(
        draw, 2820, 580, 280, 200, "🏢", 
        "Vendor Portal", "Seller / Bidder", 
        (4, 106, 56, 255), (22, 101, 52, 255), 
        font_box_title, font_box_sub
    )

    # Arrow from Right Column (x=2690) to Right Avatar Badge (x=2820)
    draw.line([(right_box_x + right_box_w + 10, 680), (2820, 680)], fill=(15, 23, 42, 255), width=3)
    draw.polygon([(2810, 670), (2830, 680), (2810, 690)], fill=(15, 23, 42, 255))

    # Save PNG files
    out_path_static = os.path.join("backend", "static", "gemverifier_architecture.png")
    out_path_artifact = os.path.join("C:\\Users\\LUVKESH\\.gemini\\antigravity\\brain\\bf68fb00-f885-4612-8424-8338356e2951", "gemverifier_architecture.png")

    image.save(out_path_static)
    image.save(out_path_artifact)
    print(f"Final Architecture Diagram saved to {out_path_static} and {out_path_artifact}")

if __name__ == "__main__":
    create_final_architecture_diagram()
