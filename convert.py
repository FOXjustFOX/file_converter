import argparse
import os
import sys
import subprocess
import pandas as pd
import markdown
import mammoth
from markdownify import markdownify as md_convert
from PIL import Image
from docx2pdf import convert as docx_to_pdf_tool
from google import genai

# NEW IMPORT
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# --- HELPER: Safe Print ---
def safe_print(msg):
    """Prints messages without breaking the tqdm progress bar."""
    tqdm.write(msg)

# --- AI ENHANCEMENT ---
def apply_gemini_enhancement(text_content):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        safe_print("❌ Error: GEMINI_API_KEY not found.")
        return text_content 

    safe_print("   ✨ Sending to Gemini...")
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = (
            "You are a professional editor. Enhance the text below. "
            "Fix grammar, improve tone, and format clearly. Return ONLY the text.\n\n"
            f"{text_content}"
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        safe_print(f"   ⚠️ Gemini Error: {e}")
        return text_content

# --- 1. IMAGE LOGIC ---
def convert_image(input_path, output_path, reduce_mode=False, enhance_mode=False):
    try:
        with Image.open(input_path) as img:
            # FIX: Force RGB for JPEGs
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode in ('RGBA', 'LA', 'P'): 
                    img = img.convert('RGB')
            
            if reduce_mode:
                img.save(output_path, optimize=True, quality=60)
            else:
                img.save(output_path)
    except Exception as e:
        safe_print(f"❌ Image Error: {e}")

# --- 2. VIDEO LOGIC ---
def convert_video(input_path, output_path, reduce_mode=False, enhance_mode=False):
    try:
        if subprocess.call(["which", "ffmpeg"], stdout=subprocess.DEVNULL) != 0:
            safe_print("❌ Error: FFmpeg is not installed.")
            return
        
        # We don't print "Processing..." here anymore to keep the bar clean
        cmd = ["ffmpeg", "-i", input_path, "-y"]
        
        if reduce_mode:
            cmd.extend(["-vcodec", "libx264", "-crf", "28", "-preset", "fast"])
        
        cmd.append(output_path)
        
        # Run silently
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except Exception as e:
        safe_print(f"❌ Video Error: {e}")

# --- 3. DOCS LOGIC ---
def convert_docs(input_path, output_path, reduce_mode=False, enhance_mode=False):
    try:
        in_ext = os.path.splitext(input_path)[1].lower()
        out_ext = os.path.splitext(output_path)[1].lower()
        content = ""

        # Extract
        if in_ext in ['.md', '.txt']:
            with open(input_path, 'r', encoding='utf-8') as f: content = f.read()
        elif in_ext == '.docx':
            with open(input_path, "rb") as docx_file:
                content = mammoth.convert_to_html(docx_file).value
                if out_ext == '.md': content = md_convert(content)

        # Enhance
        if enhance_mode and content:
            content = apply_gemini_enhancement(content)

        # Write
        if out_ext == '.html':
            html_content = markdown.markdown(content) if in_ext == '.md' else content
            with open(output_path, 'w', encoding='utf-8') as f: f.write(html_content)
        elif out_ext in ['.md', '.txt']:
            with open(output_path, 'w', encoding='utf-8') as f: f.write(content)
        elif out_ext == '.pdf' and in_ext == '.docx':
            docx_to_pdf_tool(os.path.abspath(input_path), os.path.abspath(output_path))

    except Exception as e:
        safe_print(f"❌ Doc Error: {e}")

# --- 4. DATA LOGIC ---
def convert_data(input_path, output_path, reduce_mode=False, enhance_mode=False):
    try:
        in_ext = os.path.splitext(input_path)[1].lower()
        if in_ext == '.csv': df = pd.read_csv(input_path)
        elif in_ext == '.json': df = pd.read_json(input_path)
        elif in_ext in ['.xlsx', '.xls']: df = pd.read_excel(input_path)
        else: return

        out_ext = os.path.splitext(output_path)[1].lower()
        if out_ext == '.csv': df.to_csv(output_path, index=False)
        elif out_ext == '.json': df.to_json(output_path, orient='records', indent=4)
        elif out_ext == '.xlsx': df.to_excel(output_path, index=False)
    except Exception as e:
        safe_print(f"❌ Data Error: {e}")

# --- DISPATCHER ---
def get_converter(input_ext, output_ext):
    img_exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
    vid_exts = {'.mp4', '.mkv', '.mov', '.avi', '.webm'}
    data_exts = {'.csv', '.json', '.xlsx'}
    doc_exts  = {'.docx', '.pdf', '.md', '.html', '.txt'}

    if input_ext in img_exts and output_ext in img_exts: return convert_image
    if input_ext in vid_exts and output_ext in vid_exts: return convert_video
    if input_ext in data_exts and output_ext in data_exts: return convert_data
    if input_ext in doc_exts and output_ext in doc_exts: return convert_docs
    return None

# --- CLI ENTRY ---
def main():
    parser = argparse.ArgumentParser(description="Universal Converter")
    parser.add_argument("args", nargs="+", help="Files + Output Path")
    parser.add_argument("-t", "--to", help="Target format")
    parser.add_argument("-r", "--reduce", action="store_true", help="Compress file size")
    parser.add_argument("-e", "--enhance", action="store_true", help="AI Enhancement")
    
    args = parser.parse_args()
    
    inputs = args.args[:-1]
    destination = args.args[-1]

    # Handle single file implicit output
    if len(args.args) == 1 and args.to:
        inputs = [args.args[0]]
        destination = os.path.dirname(args.args[0]) or "."
    elif len(inputs) == 0:
        print("Usage: converter <files> <output_folder> [options]")
        return

    # Create output dir if needed
    output_dir = destination
    if not os.path.exists(output_dir) and len(inputs) > 0 and not os.path.splitext(destination)[1]:
        os.makedirs(output_dir)

    target_ext = f".{args.to.lstrip('.')}" if args.to else None
    
    # --- PROGRESS BAR LOOP ---
    # We wrap 'inputs' with tqdm to create the visual bar
    print(f"🚀 Starting conversion of {len(inputs)} files...")
    
    for input_file in tqdm(inputs, unit="file", ncols=80, colour="green"):
        if not os.path.exists(input_file):
            safe_print(f"⚠️  Missing: {input_file}")
            continue
        
        in_ext = os.path.splitext(input_file)[1].lower()
        final_target = target_ext if target_ext else os.path.splitext(destination)[1].lower()
        
        if os.path.isdir(destination):
            base = os.path.splitext(os.path.basename(input_file))[0]
            out_file = os.path.join(destination, base + final_target)
        else:
            out_file = destination

        # Show current file in description
        tqdm.write(f"Processing: {os.path.basename(input_file)}")

        func = get_converter(in_ext, final_target)
        if func:
            func(input_file, out_file, reduce_mode=args.reduce, enhance_mode=args.enhance)
        else:
            safe_print(f"⚠️  No logic for {in_ext} -> {final_target}")

    print("\n✅ All tasks completed.")

if __name__ == "__main__":
    main()