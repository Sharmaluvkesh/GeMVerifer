import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram():
    # 2400 x 1400 HD Canvas
    width, height = 2400, 1450
    image = Image.new("RGBA", (width, height), (11, 19, 41, 255))
    draw = ImageDraw.Draw(image)

    # Grid Dots Background
    for x in range(0, width, 40):
        for y in range(0, height, 40):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255, 15))

    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 44)
        font_subtitle = ImageFont.truetype("arial.ttf", 22)
        font_header = ImageFont.truetype("arial.ttf", 28)
        font_box_title = ImageFont.truetype("arial.ttf", 22)
        font_box_desc = ImageFont.truetype("arial.ttf", 16)
        font_tag = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = font_subtitle = font_header = font_box_title = font_box_desc = font_tag = ImageFont.load_default()

    # Title Bar
    draw.text((80, 50), "GeMVerifier — System Architecture Blueprint", fill=(255, 255, 255, 255), font=font_title)
    draw.text((80, 105), "AI-Powered Technical Bid Evaluation Engine for Government e-Marketplace (GeM)", fill=(148, 163, 184, 255), font=font_subtitle)

    # Status Badge
    draw.rectangle([1950, 55, 2320, 105], fill=(16, 185, 129, 40), outline=(16, 185, 129, 180), width=2)
    draw.text((1975, 70), "PROD READY v3.0", fill=(52, 211, 153, 255), font=font_header)

    # Helper function to draw rounded box with header
    def draw_layer_container(x1, y1, x2, y2, title, subtitle, color_accent, color_bg):
        # Background card
        draw.rectangle([x1, y1, x2, y2], fill=color_bg, outline=color_accent, width=2)
        # Header banner
        draw.rectangle([x1, y1, x2, y1+55], fill=color_accent)
        draw.text((x1+25, y1+14), title, fill=(255, 255, 255, 255), font=font_header)
        draw.text((x2-320, y1+18), subtitle, fill=(255, 255, 255, 220), font=font_tag)

    def draw_node_box(x, y, w, h, title, desc, tag, border_color):
        draw.rectangle([x, y, x+w, y+h], fill=(15, 23, 42, 230), outline=border_color, width=2)
        draw.text((x+20, y+18), title, fill=(255, 255, 255, 255), font=font_box_title)
        draw.text((x+20, y+50), desc, fill=(148, 163, 184, 255), font=font_box_desc)
        # Tag pill
        tw = len(tag) * 9 + 20
        draw.rectangle([x+20, y+h-36, x+20+tw, y+h-12], fill=(30, 41, 59, 255), outline=border_color, width=1)
        draw.text((x+30, y+h-32), tag, fill=(203, 213, 225, 255), font=font_tag)

    # LAYER 1: USER & PRESENTATION
    draw_layer_container(80, 160, 2320, 410, "1. Presentation & User Persona Layer (Frontend)", "Tailwind CSS + HTML5 + Web Widgets", (255, 103, 31, 255), (15, 23, 42, 180))
    
    draw_node_box(110, 245, 520, 135, "🏛️ Buyer Procurement Portal", "Upload GeM Tender Notice PDF & Vendor Bids", "Procurement Officer", (245, 158, 11, 255))
    draw_node_box(660, 245, 520, 135, "🏢 Vendor Pre-Check Portal", "Audit product catalog PDF against target specs", "Seller / Bidder", (16, 185, 129, 255))
    draw_node_box(1210, 245, 520, 135, "📊 Compliance Matrix View", "Side-by-side spec comparison matrix with scores", "Matrix Viewer", (6, 182, 212, 255))
    draw_node_box(1760, 245, 520, 135, "🤖 GeM-Bot AI Assistant", "Sticky 3D mascot chat drawer for disqualification AI", "Interactive Assistant", (249, 115, 22, 255))

    # Down Arrow 1
    for x in [370, 920, 1470, 2020]:
        draw.line([(x, 410), (x, 465)], fill=(255, 103, 31, 255), width=3)
        draw.polygon([(x-8, 455), (x+8, 455), (x, 468)], fill=(255, 103, 31, 255))

    # LAYER 2: SECURITY & API GATEWAY
    draw_layer_container(80, 470, 2320, 690, "2. API Security & Gateway Layer (FastAPI Asynchronous Engine)", "Python 3.12 + FastAPI + PyJWT", (99, 102, 241, 255), (15, 23, 42, 180))
    
    draw_node_box(110, 545, 700, 120, "🔐 Authentication & JWT Engine", "SHA-256 + Salt Hasher & Bearer Token Validator", "Security Gateway", (129, 140, 248, 255))
    draw_node_box(840, 545, 700, 120, "🔄 Persona Role Switcher Middleware", "Enforces active role permissions (VENDOR / BIDDER / BOTH)", "Access Control", (129, 140, 248, 255))
    draw_node_box(1570, 545, 710, 120, "⚡ REST API Router Controllers", "Endpoints: /api/v1/auth • /api/v1/analyze • /api/v1/report", "Async Routing", (129, 140, 248, 255))

    # Down Arrow 2
    for x in [460, 1190, 1925]:
        draw.line([(x, 690), (x, 745)], fill=(99, 102, 241, 255), width=3)
        draw.polygon([(x-8, 735), (x+8, 735), (x, 748)], fill=(99, 102, 241, 255))

    # LAYER 3: CORE AI VERIFICATION PIPELINE
    draw_layer_container(80, 750, 2320, 1020, "3. Core AI Technical Verification Pipeline", "Google Gemini 2.5 Pro + pdfplumber Parser", (16, 185, 129, 255), (15, 23, 42, 180))
    
    draw_node_box(110, 835, 520, 150, "📄 pdfplumber Table Extractor", "Extracts structured tables, specs & text\nfrom multi-page tender PDFs", "PDF Parser", (52, 211, 153, 255))
    draw_node_box(660, 835, 520, 150, "📐 Tolerance & Rule Evaluator", "Parses min thresholds, +/- % ranges,\nISO 9001 & Turnover certificates", "Rule Engine", (20, 184, 166, 255))
    draw_node_box(1210, 835, 520, 150, "🤖 Gemini 2.5 Pro Matcher", "Executes semantic parameter equivalence\nmatching & term mapping", "LLM Reasoning", (6, 182, 212, 255))
    draw_node_box(1760, 835, 520, 150, "⚖️ Scoring & Disqualifier", "Calculates 0-100% technical score\n& generates disqualification rationale", "Compliance Engine", (74, 222, 128, 255))

    # Down Arrow 3
    for x in [370, 920, 1470, 2020]:
        draw.line([(x, 1020), (x, 1075)], fill=(16, 185, 129, 255), width=3)
        draw.polygon([(x-8, 1065), (x+8, 1065), (x, 1078)], fill=(16, 185, 129, 255))

    # LAYER 4: DATA & STORAGE LAYER
    draw_layer_container(80, 1080, 2320, 1300, "4. Data Persistence & Government Export Layer", "SQLite DB + ReportLab PDF + OpenPyXL Excel", (59, 130, 246, 255), (15, 23, 42, 180))
    
    draw_node_box(110, 1155, 700, 120, "🗄️ SQLite Database (SQLAlchemy ORM)", "Stores User Profile, Tender Notice, Bids & Reports", "DB Storage", (96, 165, 250, 255))
    draw_node_box(840, 1155, 700, 120, "📁 Raw Document Repository", "Stores uploaded raw tender PDFs in /uploaded_files", "File System", (96, 165, 250, 255))
    draw_node_box(1570, 1155, 710, 120, "📥 Government PDF & Excel Exporter", "Generates official PDF reports & Excel side-by-side matrices", "Export Engine", (96, 165, 250, 255))

    # Footer note
    draw.text((80, 1340), "GeMVerifier Architecture — 100% Vector Crisp Flow Diagram | Smart India Hackathon (SIH)", fill=(148, 163, 184, 255), font=font_subtitle)

    output_path = os.path.join("backend", "static", "architecture_diagram.png")
    image.save(output_path)
    print(f"Diagram successfully saved to {output_path}")

if __name__ == "__main__":
    create_architecture_diagram()
