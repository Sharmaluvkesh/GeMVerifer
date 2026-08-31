import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_stick_figure(draw, x, y, label, font_label):
    # Head circle
    draw.ellipse([x-25, y-80, x+25, y-30], fill=None, outline=(255, 255, 255, 255), width=3)
    # Body line
    draw.line([(x, y-30), (x, y+40)], fill=(255, 255, 255, 255), width=3)
    # Arms
    draw.line([(x-40, y-10), (x+40, y-10)], fill=(255, 255, 255, 255), width=3)
    # Legs
    draw.line([(x, y+40), (x-35, y+100)], fill=(255, 255, 255, 255), width=3)
    draw.line([(x, y+40), (x+35, y+100)], fill=(255, 255, 255, 255), width=3)
    # Label text below
    w_label = len(label) * 8
    draw.text((x - w_label, y + 120), label, fill=(203, 213, 225, 255), font=font_label)

def draw_3d_cube(draw, x, y, w, h, depth, label, font_main):
    # Front face
    front = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    draw.polygon(front, fill=(30, 41, 59, 240), outline=(255, 103, 31, 255), width=3)
    
    # Top face
    top = [(x, y), (x+depth, y-depth), (x+w+depth, y-depth), (x+w, y)]
    draw.polygon(top, fill=(51, 65, 85, 240), outline=(255, 103, 31, 255), width=3)

    # Right side face
    side = [(x+w, y), (x+w+depth, y-depth), (x+w+depth, y+h-depth), (x+w, y+h)]
    draw.polygon(side, fill=(15, 23, 42, 240), outline=(255, 103, 31, 255), width=3)

    # Text in front face
    draw.text((x + 20, y + h//2 - 25), "⚡ FastAPI Gateway", fill=(255, 255, 255, 255), font=font_main)
    draw.text((x + 20, y + h//2 + 10), "& Security Engine", fill=(255, 103, 31, 255), font=font_main)

def create_grid_architecture_diagram():
    # 3200 x 1400 Canvas
    width, height = 3200, 1400
    image = Image.new("RGBA", (width, height), (18, 18, 18, 255)) # Dark Eraser/Excalidraw canvas
    draw = ImageDraw.Draw(image)

    # Dark Grid Lines Pattern (matching user's reference image)
    grid_size = 40
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=(40, 40, 40, 255), width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=(40, 40, 40, 255), width=1)

    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 48)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_label = ImageFont.truetype("arial.ttf", 22)
        font_box_title = ImageFont.truetype("arial.ttf", 26)
        font_box_sub = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_subtitle = font_label = font_box_title = font_box_sub = ImageFont.load_default()

    # Title Banner
    draw.text((80, 40), "GeMVerifier — Platform System Flow Diagram", fill=(255, 255, 255, 255), font=font_title)
    draw.text((80, 100), "Eraser.io / Excalidraw Style System Architecture Blueprint", fill=(156, 163, 175, 255), font=font_subtitle)

    # 1. Left Actor: Buyer (Procurement)
    draw_stick_figure(draw, 220, 680, "Buyer (Procurement)", font_label)

    # Arrow from Left Actor to 3D Cube
    draw.line([(320, 680), (520, 680)], fill=(255, 255, 255, 255), width=3)
    draw.polygon([(510, 670), (530, 680), (510, 690)], fill=(255, 255, 255, 255))

    # 2. Central 3D Cube Box (FastAPI Gateway)
    draw_3d_cube(draw, 540, 580, 300, 200, 50, "FastAPI Gateway", font_label)

    # 3. Middle Column: 4 Stacked Rounded Boxes (AI Pipeline)
    mid_boxes = [
        ("📄 pdfplumber Table Extractor", "Parses multi-column PDF tables & text", (255, 103, 31, 255)),
        ("📐 Rule & Spec Evaluator", "Min core count & tolerance (+/- %) checks", (16, 185, 129, 255)),
        ("🤖 Gemini 2.5 Pro Matcher", "Semantic technical spec equivalence", (6, 182, 212, 255)),
        ("⚖️ Compliance Scoring Engine", "0-100% score & disqualification rationale", (99, 102, 241, 255))
    ]

    mid_box_x = 1150
    mid_box_w = 640
    mid_box_h = 135
    box_gap = 45
    start_y = 350

    mid_y_centers = []

    for i, (title, desc, outline_color) in enumerate(mid_boxes):
        by = start_y + i * (mid_box_h + box_gap)
        cy = by + mid_box_h // 2
        mid_y_centers.append(cy)

        # Draw rounded rectangle box
        draw.rectangle([mid_box_x, by, mid_box_x + mid_box_w, by + mid_box_h], fill=(24, 24, 27, 240), outline=outline_color, width=3)
        draw.text((mid_box_x + 30, by + 30), title, fill=(255, 255, 255, 255), font=font_box_title)
        draw.text((mid_box_x + 30, by + 75), desc, fill=(156, 163, 175, 255), font=font_box_sub)

        # Fanning arrows from 3D Cube (x=890, y=680) to each middle box (x=1150, y=cy)
        draw.line([(890, 680), (mid_box_x - 10, cy)], fill=(200, 200, 200, 255), width=2)
        # Arrowhead
        angle = math.atan2(cy - 680, mid_box_x - 10 - 890)
        ax1 = (mid_box_x - 10) - 15 * math.cos(angle - 0.3)
        ay1 = cy - 15 * math.sin(angle - 0.3)
        ax2 = (mid_box_x - 10) - 15 * math.cos(angle + 0.3)
        ay2 = cy - 15 * math.sin(angle + 0.3)
        draw.polygon([(mid_box_x - 10, cy), (ax1, ay1), (ax2, ay2)], fill=(200, 200, 200, 255))

    # 4. Right Column: 4 Stacked Rounded Boxes (Outputs & UI Views)
    right_boxes = [
        ("🖥️ Command Dashboard View", "Live pop-out vendor evaluation cards", (59, 130, 246, 255)),
        ("📊 Compliance Verification Matrix", "Side-by-side spec comparison table", (245, 158, 11, 255)),
        ("🤖 GeM-Bot Interactive Drawer", "AI Assistant chat modal for queries", (249, 115, 22, 255)),
        ("📥 PDF & Excel Exporter", "Official ReportLab PDF & Excel sheets", (34, 197, 94, 255))
    ]

    right_box_x = 2050
    right_box_w = 640

    for i, (title, desc, outline_color) in enumerate(right_boxes):
        by = start_y + i * (mid_box_h + box_gap)
        cy = by + mid_box_h // 2

        # Draw rounded rectangle box
        draw.rectangle([right_box_x, by, right_box_x + right_box_w, by + mid_box_h], fill=(24, 24, 27, 240), outline=outline_color, width=3)
        draw.text((right_box_x + 30, by + 30), title, fill=(255, 255, 255, 255), font=font_box_title)
        draw.text((right_box_x + 30, by + 75), desc, fill=(156, 163, 175, 255), font=font_box_sub)

        # Connecting straight horizontal arrows between Middle Column and Right Column
        draw.line([(mid_box_x + mid_box_w + 10, cy), (right_box_x - 10, cy)], fill=(200, 200, 200, 255), width=2)
        draw.polygon([(right_box_x - 20, cy - 8), (right_box_x - 5, cy), (right_box_x - 20, cy + 8)], fill=(200, 200, 200, 255))

    # 5. Right Actor: Vendor (Seller / Bidder)
    draw_stick_figure(draw, 2980, 680, "Vendor (Seller)", font_label)

    # Arrow from Right Column (x=2690) to Right Actor (x=2900)
    draw.line([(right_box_x + right_box_w + 10, 680), (2900, 680)], fill=(255, 255, 255, 255), width=3)
    draw.polygon([(2890, 670), (2910, 680), (2890, 690)], fill=(255, 255, 255, 255))

    # Save PNG files
    out_path_static = os.path.join("backend", "static", "gemverifier_grid_architecture.png")
    out_path_artifact = os.path.join("C:\\Users\\LUVKESH\\.gemini\\antigravity\\brain\\bf68fb00-f885-4612-8424-8338356e2951", "gemverifier_grid_architecture.png")

    image.save(out_path_static)
    image.save(out_path_artifact)
    print(f"Exact Grid Architecture Diagram saved to {out_path_static} and {out_path_artifact}")

if __name__ == "__main__":
    create_grid_architecture_diagram()
