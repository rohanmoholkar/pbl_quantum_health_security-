# Install these if you haven't: pip install fpdf pillow
from fpdf import FPDF
from PIL import Image
import os

# --- CONFIGURATION ---
IMAGE_FILENAME = 'dashboard.png'  # RENAME YOUR UPLOADED IMAGE TO THIS
PDF_FILENAME = 'PBL2_Report_Final.pdf'

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PBL-2 Project Report: Quantum-Secured Digital Health', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_image_centered(self, img_path, w=150):
        if os.path.exists(img_path):
            self.image(img_path, x=(210-w)/2, w=w)
            self.ln(10)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f'[Image missing: {img_path}]', 0, 1, 'C')
            self.set_text_color(0, 0, 0)

# --- IMAGE PROCESSING ---
# This chops your single screenshot into 3 parts for the report
if os.path.exists(IMAGE_FILENAME):
    try:
        full_img = Image.open(IMAGE_FILENAME)
        width, height = full_img.size
        
        # Crop 1: QKD (Left Third)
        qkd_crop = full_img.crop((0, 0, width/3, height))
        qkd_crop.save("temp_qkd.png")
        
        # Crop 2: AI (Middle Third)
        ai_crop = full_img.crop((width/3, 0, (width*2)/3, height))
        ai_crop.save("temp_ai.png")
        
        # Crop 3: Crypto (Right Third)
        crypto_crop = full_img.crop(((width*2)/3, 0, width, height))
        crypto_crop.save("temp_crypto.png")
        print("Images processed successfully.")
    except Exception as e:
        print(f"Error processing image: {e}")
else:
    print(f"WARNING: '{IMAGE_FILENAME}' not found. PDF will be generated without images.")

# --- PDF GENERATION ---
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# 1. Title Page
pdf.set_font('Arial', 'B', 24)
pdf.ln(50)
pdf.cell(0, 15, 'Quantum-Secured Digital Health', 0, 1, 'C')
pdf.cell(0, 15, 'Identity System for India', 0, 1, 'C')
pdf.set_font('Arial', '', 16)
pdf.ln(20)
pdf.cell(0, 10, 'PBL-2 Phase: Research & Modeling', 0, 1, 'C')
pdf.ln(40)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Submitted By: Rohan Sanjeev Moholkar', 0, 1, 'C')
pdf.cell(0, 10, 'Enrollment No: 2428010109', 0, 1, 'C')
pdf.cell(0, 10, 'Dept of Information Technology, Manipal University Jaipur', 0, 1, 'C')
pdf.add_page()

# 2. Abstract
pdf.chapter_title("Abstract")
pdf.chapter_body(
    "The rapid digitization of India's healthcare infrastructure has created a centralized target vulnerable "
    "to both classical cyberattacks and future quantum computing threats. This report details the work undertaken "
    "in Phase 2 (PBL-2), focusing on Research & Modeling. We conducted a comparative analysis of Post-Quantum "
    "Cryptography (PQC) algorithms, simulated QKD photon loss to determine maximum secure transmission distances "
    "(approx 100km), and designed an AI-based anomaly detection framework using Isolation Forest algorithms. "
    "The results confirm the technical viability of a quantum-resilient health network for India."
)

# 3. Post-Quantum Cryptography
pdf.chapter_title("1. Post-Quantum Cryptography (PQC) Analysis")
pdf.chapter_body(
    "To secure health data against future quantum attacks, we compared NIST-standardized algorithms. "
    "Our analysis focuses on Lattice-based cryptography due to its efficiency.\n\n"
    "We compared RSA-2048 (Current Standard) against CRYSTALS-Kyber (PQC). "
    "As shown in the graph below, Kyber offers superior security (128-bit) with significantly lower latency, "
    "making it ideal for high-volume hospital networks."
)
pdf.add_image_centered("temp_crypto.png", w=140)

# 4. QKD Feasibility
pdf.chapter_title("2. QKD Feasibility Modeling")
pdf.chapter_body(
    "We simulated the transmission of quantum keys over standard telecom fiber (SMF-28) with an attenuation "
    "of 0.2 dB/km. The simulation calculated the 'Secure Key Rate' as a function of distance.\n\n"
    "Results indicate that QKD is highly effective for Metro scales (0-50km). For Inter-city links (>100km), "
    "Trusted Nodes or repeaters are required to maintain a secure signal."
)
pdf.add_image_centered("temp_qkd.png", w=140)

# 5. AI Defense
pdf.chapter_title("3. AI Anomaly Detection Framework")
pdf.chapter_body(
    "The system uses an Isolation Forest algorithm to detect fraud in real-time. We modeled 'Normal Traffic' "
    "as standard EHR access patterns and 'Attacks' as data exfiltration attempts.\n\n"
    "The simulation below demonstrates the model successfully isolating 17 specific security threats "
    "(Red outliers) from normal hospital traffic (Green clusters), achieving the 'Zero Fraud' objective."
)
pdf.add_image_centered("temp_ai.png", w=140)

# 6. Conclusion
pdf.chapter_title("4. Conclusion & Future Roadmap")
pdf.chapter_body(
    "PBL-2 has successfully validated the theoretical models for the proposed system. We have demonstrated that "
    "Lattice-based PQC and QKD are feasible for India's healthcare infrastructure. \n\n"
    "Future Work (PBL-3): The final phase will focus on the integration of these models into a cohesive prototype "
    "and the refinement of the blockchain consensus mechanism."
)

# Save
try:
    pdf.output(PDF_FILENAME)
    print(f"SUCCESS: PDF generated as '{PDF_FILENAME}'")
except Exception as e:
    print(f"Error saving PDF: {e}")
