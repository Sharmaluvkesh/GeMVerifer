import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_creative_ppt_diagram():
    # Compact 16:6 Wide Ratio for Half PPT Slide (3200 x 1200)
    width, height = 3200, 1200
    image = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(image)

    # Subtle Grid Dots
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255, 18))

    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 52)
        font_subtitle = ImageFont.truetype("arial.ttf", 26)
        font_node_title = ImageFont.truetype("arial.ttf", 32)
        font_pill = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = font_subtitle = font_node_title = font_pill = ImageFont.load_default()

    # Creative Header
    draw.text((80, 50), "GeMVerifier — AI Architecture Flow", fill=(255, 255, 255, 255), font=font_title)
    draw.text((80, 115), "Smart India Hackathon • Compact PPT Presentation Slide View", fill=(148, 163, 184, 255), font=font_subtitle)

    # Live Badge
    draw.rectangle([2750, 50, 3120, 105], fill=(16, 185, 129, 30), outline=(16, 185, 129, 200), width=2)
    draw.text((2780, 65), "LIVE ENGINE v3.0", fill=(52, 211, 153, 255), font=font_pill)

    # 4 Main Creative Nodes (Horizontal Flow)
    nodes = [
        {
            "num": "01",
            "title": "USER & PORTALS",
            "symbol": "🌐",
            "color": (255, 103, 31, 255), # Saffron
            "pills": ["🏛️ Buyer Portal", "🏢 Vendor Pre-Check", "🤖 GeM-Bot Assistant", "📊 Compliance Matrix"]
        },
        {
            "num": "02",
            "title": "GATEWAY & SECURITY",
            "symbol": "⚡",
            "color": (99, 102, 241, 255), # Indigo
            "pills": ["⚡ FastAPI Router", "🔐 SHA-256 / JWT Auth", "👤 Persona Switcher", "🛡️ Role Security"]
        },
        {
            "num": "03",
            "title": "AI VERIFICATION",
            "symbol": "🧠",
            "color": (16, 185, 129, 255), # Emerald
            "pills": ["📄 pdfplumber Parser", "📐 Tolerance Checks", "🤖 Gemini 2.5 Pro", "⚖️ 0-100% Scoring"]
        },
        {
            "num": "04",
            "title": "DATA & EXPORT",
            "symbol": "💾",
            "color": (59, 130, 246, 255), # Blue
            "pills": ["🗄️ SQLite Database", "📁 PDF Storage", "📄 PDF Report Export", "📊 Excel Matrix Export"]
        }
    ]

    center_y = 650
    node_x_positions = [420, 1180, 1940, 2700]

    # Draw Connecting Flow Lines with Arrows first (Behind Nodes)
    for i in range(len(node_x_positions) - 1):
        x1 = node_x_positions[i] + 160
        x2 = node_x_positions[i+1] - 160
        
        # Neon Connecting Pipeline
        draw.line([(x1, center_y), (x2, center_y)], fill=(56, 189, 248, 255), width=6)
        
        # Animated Flow Circle Orbs along line
        for offset in [0.25, 0.5, 0.75]:
            ox = x1 + (x2 - x1) * offset
            draw.ellipse([ox-12, center_y-12, ox+12, center_y+12], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)

        # Right Arrow Head
        draw.polygon([
            (x2 - 15, center_y - 15),
            (x2 + 10, center_y),
            (x2 - 15, center_y + 15)
        ], fill=(56, 189, 248, 255))

    # Draw Creative Circular/Badge Nodes
    for i, node in enumerate(nodes):
        cx = node_x_positions[i]
        cy = center_y

        # Glowing Outer Aura Ring
        draw.ellipse([cx-140, cy-140, cx+140, cy+140], fill=node["color"][:3] + (30,), outline=node["color"], width=3)
        # Inner Circular Node Badge
        draw.ellipse([cx-115, cy-115, cx+115, cy+115], fill=(30, 41, 59, 240), outline=node["color"], width=4)

        # Symbol & Stage Number
        draw.text((cx-25, cy-75), node["symbol"], fill=(255, 255, 255, 255), font=font_title)
        draw.text((cx-18, cy-10), node["num"], fill=node["color"], font=font_pill)
        draw.text((cx - len(node["title"])*8, cy+25), node["title"], fill=(255, 255, 255, 255), font=font_node_title)

        # Floating Pill Badges (2 Above, 2 Below)
        pill_offsets = [
            (-230, -310), (20, -310), # Top row
            (-230, 180),  (20, 180)   # Bottom row
        ]

        for p_idx, pill_text in enumerate(node["pills"]):
            px_off, py_off = pill_offsets[p_idx]
            px = cx + px_off
            py = cy + py_off
            pw, ph = 210, 60

            # Pill card
            draw.rectangle([px, py, px+pw, py+ph], fill=(15, 23, 42, 230), outline=node["color"], width=2)
            draw.text((px+15, py+18), pill_text, fill=(241, 245, 249, 255), font=font_pill)

    # Save compact PPT diagram image
    out_path_static = os.path.join("backend", "static", "gemverifier_creative_ppt.png")
    out_path_artifact = os.path.join("C:\\Users\\LUVKESH\\.gemini\\antigravity\\brain\\bf68fb00-f885-4612-8424-8338356e2951", "gemverifier_creative_ppt.png")

    image.save(out_path_static)
    image.save(out_path_artifact)
    print(f"Creative PPT Diagram saved to {out_path_static} and {out_path_artifact}")

if __name__ == "__main__":
    create_creative_ppt_diagram()
