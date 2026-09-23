import os
from PIL import Image, ImageDraw, ImageFont

def render_scene_frame(scene_num, title, subtitle, narration, accent_color, output_path):
    width, height = 1920, 1080
    image = Image.new("RGBA", (width, height), (6, 17, 33, 255)) # Navy Slate #061121
    draw = ImageDraw.Draw(image)

    # Grid Pattern Background
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(15, 35, 60, 255), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(15, 35, 60, 255), width=1)

    # Fonts
    try:
        font_logo = ImageFont.truetype("arial.ttf", 36)
        font_title = ImageFont.truetype("arial.ttf", 44)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_caption = ImageFont.truetype("arial.ttf", 22)
        font_timer = ImageFont.truetype("arial.ttf", 20)
    except:
        font_logo = font_title = font_subtitle = font_caption = font_timer = ImageFont.load_default()

    # Top Bar Header
    draw.rectangle([40, 30, 1880, 100], fill=(11, 30, 54, 230), outline=(56, 189, 248, 100), width=2)
    draw.text((60, 48), "GeMVerifier V2 — SIH 2026 Project Demonstration Video", fill=(255, 255, 255, 255), font=font_logo)
    
    scene_time = f"SCENE {scene_num:02d} / 12"
    draw.rectangle([1680, 45, 1860, 85], fill=(30, 58, 138, 200), outline=accent_color, width=2)
    draw.text((1700, 53), scene_time, fill=(56, 189, 248, 255), font=font_timer)

    # Main Center Card
    draw.rectangle([120, 140, 1800, 920], fill=(11, 30, 54, 240), outline=accent_color, width=3)
    
    # Card Header
    draw.rectangle([120, 140, 1800, 230], fill=accent_color)
    draw.text((160, 165), title, fill=(255, 255, 255, 255), font=font_title)

    # Content Area
    draw.text((160, 270), subtitle, fill=(56, 189, 248, 255), font=font_subtitle)

    # Inner Visual Mockup Card depending on Scene
    if scene_num == 1: # Problem
        draw.rectangle([200, 350, 1720, 750], fill=(15, 23, 42, 255), outline=(244, 63, 94, 200), width=2)
        draw.text((240, 400), "📁 Tender Document (Notice Inviting Tender)", fill=(255, 255, 255, 255), font=font_subtitle)
        draw.text((240, 460), "📊 Financial Statements (Audited Turnover P&L)", fill=(255, 255, 255, 255), font=font_subtitle)
        draw.text((240, 520), "📜 GST Certificate & PAN Registrations", fill=(255, 255, 255, 255), font=font_subtitle)
        draw.text((240, 580), "🏆 Past Performance & Experience Certificates", fill=(255, 255, 255, 255), font=font_subtitle)
        draw.text((240, 670), "⚠ Manual examination across multiple PDF documents is document-intensive & time-consuming.", fill=(244, 63, 94, 255), font=font_subtitle)
    
    elif scene_num == 2: # Solution Motto
        draw.rectangle([200, 340, 1720, 780], fill=(15, 23, 42, 255), outline=(56, 189, 248, 200), width=2)
        draw.text((250, 390), "“AI understands.”", fill=(255, 255, 255, 255), font=font_title)
        draw.text((250, 470), "“Evidence proves.”", fill=(56, 189, 248, 255), font=font_title)
        draw.text((250, 550), "“The verification engine validates.”", fill=(52, 211, 153, 255), font=font_title)
        draw.text((250, 630), "“The officer decides.”", fill=(251, 191, 36, 255), font=font_title)

    elif scene_num == 7: # Evidence Mapping
        draw.rectangle([200, 360, 1720, 760], fill=(15, 23, 42, 255), outline=(99, 102, 241, 200), width=2)
        draw.text((240, 400), "REQUIREMENT: Minimum Turnover ≥ ₹2 Cr", fill=(251, 191, 36, 255), font=font_subtitle)
        draw.text((240, 470), "SOURCE DOCUMENT: FinancialStatement.pdf", fill=(56, 189, 248, 255), font=font_subtitle)
        draw.text((240, 540), "PAGE MARKER: Page 7 (Table Line 4)", fill=(165, 180, 252, 255), font=font_subtitle)
        draw.text((240, 610), "EXTRACTED VALUE: ₹2.43 Crore", fill=(52, 211, 153, 255), font=font_subtitle)
        draw.text((240, 680), "RULE EVALUATION: 2.43 ≥ 2.0  →  PASS ✓", fill=(52, 211, 153, 255), font=font_title)

    elif scene_num == 8: # Deterministic Verification
        draw.rectangle([200, 360, 1720, 760], fill=(15, 23, 42, 255), outline=(52, 211, 153, 200), width=2)
        draw.text((240, 420), "Target Requirement:  2.00 Crore", fill=(251, 191, 36, 255), font=font_subtitle)
        draw.text((240, 490), "Extracted Evidence:  2.43 Crore", fill=(56, 189, 248, 255), font=font_subtitle)
        draw.text((240, 560), "Backend Rule Check:  2.43 ≥ 2.0  =  TRUE", fill=(52, 211, 153, 255), font=font_subtitle)
        draw.text((240, 650), "RESULT:  PASS ✓", fill=(52, 211, 153, 255), font=font_title)

    elif scene_num == 9: # Outcomes
        draw.rectangle([200, 350, 1720, 770], fill=(15, 23, 42, 255), outline=(56, 189, 248, 200), width=2)
        draw.text((240, 400), "✓  Minimum Turnover Requirement (≥ ₹2 Cr)  --------  PASS", fill=(52, 211, 153, 255), font=font_subtitle)
        draw.text((240, 480), "✓  PAN Card Statutory Verification         --------  PASS", fill=(52, 211, 153, 255), font=font_subtitle)
        draw.text((240, 560), "✕  Past Experience Requirement (5 Yrs Req)  --------  FAIL", fill=(244, 63, 94, 255), font=font_subtitle)
        draw.text((240, 640), "⚠  GST Exemption Evidence Review            --------  REVIEW", fill=(251, 191, 36, 255), font=font_subtitle)

    elif scene_num == 11: # Human in the Loop
        draw.rectangle([200, 350, 1720, 750], fill=(15, 23, 42, 255), outline=(251, 191, 36, 200), width=2)
        draw.text((250, 420), "AI Assistance  ➔  Evidence Mapping  ➔  Deterministic Engine  ➔  OFFICER DECISION", fill=(255, 255, 255, 255), font=font_subtitle)
        draw.text((250, 520), "The Procurement Officer retains 100% final authority.", fill=(251, 191, 36, 255), font=font_title)
        draw.text((250, 600), "AI provides traceable evidence support; it does NOT make autonomous tender awards.", fill=(148, 163, 184, 255), font=font_subtitle)

    else:
        draw.rectangle([200, 350, 1720, 750], fill=(15, 23, 42, 255), outline=(56, 189, 248, 200), width=2)
        draw.text((240, 440), f"GeMVerifier V2 Workflow Execution Stage {scene_num}", fill=(255, 255, 255, 255), font=font_title)
        draw.text((240, 540), "Deterministic Rules • Traceable Evidence Chain • Officer Audit Trail", fill=(56, 189, 248, 255), font=font_subtitle)

    # Subtitle Caption Banner at Bottom
    draw.rectangle([120, 950, 1800, 1030], fill=(3, 7, 18, 230), outline=(56, 189, 248, 150), width=2)
    draw.text((160, 975), f"“{narration}”", fill=(255, 255, 255, 255), font=font_caption)

    image.save(output_path)

def generate_all_scenes():
    out_dir = os.path.join("backend", "static", "video_scenes")
    os.makedirs(out_dir, exist_ok=True)

    scenes_data = [
        (1, "SCENE 1: THE PROBLEM (0:00 - 0:15)", "Document-Intensive Manual Cross-Checking", "Government procurement involves checking multiple eligibility, statutory and tender-specific requirements across large numbers of bidder documents.", (244, 63, 94, 255)),
        (2, "SCENE 2: INTRODUCE OUR SOLUTION (0:15 - 0:30)", "GeMVerifier V2 AI-Assisted Evidence Platform", "GeMVerifier V2 is an AI-assisted bid verification and evidence platform designed to structure this process around traceable evidence and deterministic verification.", (56, 189, 248, 255)),
        (3, "SCENE 3: SYSTEM WORKFLOW (0:30 - 0:45)", "End-to-End Tender Verification Pipeline", "Our workflow begins with the tender and its requirements. The system analyzes requirements, processes bidder documents, extracts relevant information, and applies verification rules.", (16, 185, 129, 255)),
        (4, "SCENE 4: TENDER REQUIREMENTS (0:45 - 1:00)", "Converting Tender Specs to Measurable Tasks", "First, the system converts natural-language tender conditions into structured verification tasks, turning turnover requirements into measurable rules.", (245, 158, 11, 255)),
        (5, "SCENE 5: BIDDER DOCUMENT UPLOAD (1:00 - 1:20)", "Bidder Document Processing & OCR Pipeline", "Next, the bidder submits the required documents. Our document pipeline processes digital PDFs and scanned documents using parsing and OCR.", (56, 189, 248, 255)),
        (6, "SCENE 6: AI EXTRACTION (1:20 - 1:35)", "Extracting Values & Document Evidence Markers", "The system identifies the financial statement, extracts the relevant turnover value of 2.43 crore rupees, and identifies where the evidence appears.", (245, 158, 11, 255)),
        (7, "SCENE 7: EVIDENCE MAPPING (1:35 - 1:55)", "Traceable Evidence Chain Graph", "GeMVerifier V2 maintains a traceable chain from requirement to original document, page, extracted value and verification rule.", (99, 102, 241, 255)),
        (8, "SCENE 8: DETERMINISTIC VERIFICATION (1:55 - 2:10)", "Mathematical Backend Rule Evaluation", "The actual compliance decision is performed by the deterministic verification engine, evaluating two point four three greater than or equal to two, producing PASS.", (52, 211, 153, 255)),
        (9, "SCENE 9: PASS / FAIL / REVIEW OUTCOMES (2:10 - 2:30)", "Explainable Outcome Classifications", "Our system produces three explainable outcomes: PASS when satisfied, FAIL when violated, and REVIEW when evidence requires human verification.", (56, 189, 248, 255)),
        (10, "SCENE 10: OFFICER REVIEW (2:30 - 2:45)", "Deep Evidence Inspection & Audit Trail", "The officer can inspect why a requirement passed, failed or requires review, and directly trace the result back to its supporting evidence.", (245, 158, 11, 255)),
        (11, "SCENE 11: HUMAN-IN-THE-LOOP (2:45 - 2:55)", "Officer Retains 100% Final Authority", "Most importantly, AI does not make the final procurement decision. The system provides evidence support, while qualification remains with the officer.", (251, 191, 36, 255)),
        (12, "SCENE 12: FINAL CLOSING (2:55 - 3:05)", "GeMVerifier V2 — Evidence-Driven Workflow", "GeMVerifier V2 transforms bid verification into an evidence-driven workflow. AI understands. Evidence proves. The verification engine validates. The officer decides.", (56, 189, 248, 255))
    ]

    for num, title, sub, narr, accent in scenes_data:
        file_path = os.path.join(out_dir, f"scene_{num:02d}.png")
        render_scene_frame(num, title, sub, narr, accent, file_path)
        print(f"Rendered Scene {num}: {file_path}")

    print("All 12 1080p Video Scene Frames successfully generated!")

if __name__ == "__main__":
    generate_all_scenes()
