#!/usr/bin/env python3
"""Generate images for the AI Writing Tools for Small Business blog post."""

import os
import sys
import base64
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = "/root/projects/monsoftsolutions.com/src/data/blog/ai-writing-tools-small-business-guide/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt, filename, model="gpt-image-1", size="1024x1024", quality="medium"):
    print(f"Generating {filename} with {model} ({size}, {quality})...")

    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "output_format": "png",
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
        timeout=180,
    )

    if response.status_code != 200:
        print(f"ERROR {response.status_code}: {response.text}", file=sys.stderr)
        return False

    data = response.json()
    image_b64 = data["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_b64)

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    size_kb = len(image_bytes) / 1024
    print(f"  Saved {filepath} ({size_kb:.0f} KB)")
    return True


def generate_with_fallback(prompt, filename, preferred_model, fallback_model, size, quality):
    """Try preferred model first, fall back to fallback_model on failure."""
    success = generate_image(prompt, filename, model=preferred_model, size=size, quality=quality)
    if not success:
        print(f"  Retrying with fallback model {fallback_model}...")
        success = generate_image(prompt, filename, model=fallback_model, size=size, quality=quality)
    return success


# Hero image — try gpt-image-1.5, fall back to gpt-image-1 (high, 1536x1024)
hero_prompt = (
    "A bright, modern small business owner — a confident woman in her 30s in smart casual attire — "
    "sits at a clean white desk in a well-lit home office. She's smiling at a laptop screen showing "
    "an AI writing interface generating marketing copy. Floating above the screen are glowing text "
    "snippets: blog posts, email subject lines, social media captions, product descriptions. "
    "A coffee mug and notepad sit beside the laptop. The room feels productive and creative — "
    "warm daylight from a window, a plant on the shelf, a tidy workspace. "
    "Photorealistic, warm natural lighting, modern minimalist aesthetic, optimistic and empowering mood. "
    "No visible text or logos."
)
generate_with_fallback(
    hero_prompt, "hero.png",
    preferred_model="gpt-image-1.5",
    fallback_model="gpt-image-1",
    size="1536x1024",
    quality="high"
)

# Inline 1 — AI writing tool categories diagram
inline1_prompt = (
    "A clean, modern flat-design infographic showing 6 categories of AI writing tools arranged "
    "in a hexagonal grid layout. Each hexagon represents a category with a simple icon and label: "
    "Blog & SEO Content (document icon), Marketing Copy (megaphone icon), Email Campaigns (envelope icon), "
    "Social Media (speech bubble icon), Product Descriptions (tag icon), and Brand Voice (fingerprint icon). "
    "Color palette: deep navy blue, electric teal, warm gold, and white. "
    "Central title reads 'AI Writing Tools'. "
    "Minimalist professional infographic style, white background, modern sans-serif typography. "
    "No photos, pure graphic design."
)
generate_with_fallback(
    inline1_prompt, "inline-1.png",
    preferred_model="gpt-image-1",
    fallback_model="gpt-image-1",
    size="1024x1024",
    quality="medium"
)

# Inline 2 — Brand voice training visual
inline2_prompt = (
    "A split-screen illustration showing 'Before AI' vs 'After AI' for small business content creation. "
    "Left side (Before): a stressed business owner surrounded by crumpled paper, sticky notes, and a "
    "blank document, looking overwhelmed. Right side (After): the same person relaxed and confident, "
    "AI-generated text flowing seamlessly onto their screen, calendar showing scheduled posts. "
    "Flat design illustration style, teal and gold color palette, friendly and professional aesthetic. "
    "Label panels clearly with 'Without AI' and 'With AI'. "
    "Clean minimalist design, no photographs, modern graphic style."
)
generate_with_fallback(
    inline2_prompt, "inline-2.png",
    preferred_model="gpt-image-1",
    fallback_model="gpt-image-1",
    size="1024x1024",
    quality="medium"
)

# Inline 3 — ROI time savings visual
inline3_prompt = (
    "A clean bar chart infographic comparing weekly content creation time: 'Traditional Writing' bar "
    "shows 12 hours in dark gray, 'With AI Writing Tools' bar shows 3 hours in vibrant teal. "
    "Below the chart, three benefit callout boxes: '75% Time Saved', '3x More Content', "
    "'Consistent Brand Voice'. "
    "Modern financial/business infographic style, white background, navy and teal color palette. "
    "Subtitle reads 'Small Business Content Creation: Time Investment'. "
    "Professional data visualization, no photographs, flat design."
)
generate_with_fallback(
    inline3_prompt, "inline-3.png",
    preferred_model="gpt-image-1",
    fallback_model="gpt-image-1",
    size="1024x1024",
    quality="medium"
)

print("\nAll images generated successfully!")
