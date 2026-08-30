#!/usr/bin/env python3
"""Generate images for the Men's Aesthetics Marketing blog post."""

import os
import sys
import base64
import requests
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = "/root/projects/monsoftsolutions.com/src/data/blog/mens-aesthetics-marketing-med-spa-guide/images"
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
        timeout=120,
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


# Hero image — gpt-image-1.5, 1536x1024, high quality
hero_prompt = (
    "A professional male patient in his 40s having a consultation with a friendly female aesthetician "
    "at an upscale modern med spa. The setting is elegant and welcoming — clean white and navy blue tones, "
    "soft lighting, potted greenery, and tasteful decor. The aesthetician reviews skincare notes on a tablet "
    "while the male patient appears relaxed and confident. Photorealistic, cinematic lighting, "
    "professional healthcare setting, high-end spa ambiance."
)
generate_image(hero_prompt, "hero.png", model="gpt-image-1", size="1536x1024", quality="high")

# Inline 1 — men's aesthetics market growth infographic
inline1_prompt = (
    "A clean, modern infographic showing the growth of men's aesthetics market. Flat design style with "
    "blue and slate grey color palette. Includes icons and stats: bar chart showing '15% annual growth', "
    "icons for top male treatments (Botox, laser, body contouring, hair restoration, skincare), "
    "a simple upward trend arrow. Professional business infographic style, white background, "
    "modern typography, no text labels needed."
)
generate_image(inline1_prompt, "inline-1.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 2 — male patient reviewing treatment options
inline2_prompt = (
    "A confident professional man in his late 30s sitting across a desk from a med spa consultant, "
    "both looking at a digital tablet displaying before/after treatment photos. The consultation room "
    "is modern and clinical but inviting — neutral tones, soft lighting, medical-grade equipment visible "
    "in background. The man appears comfortable and engaged. Photorealistic, warm professional lighting."
)
generate_image(inline2_prompt, "inline-2.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 3 — marketing strategy diagram for male patients
inline3_prompt = (
    "A clean digital marketing funnel diagram specifically for attracting male aesthetics patients. "
    "Modern flat design with blue, teal, and dark grey colors. Funnel shows 4 stages: "
    "Awareness (social media and search), Consideration (educational content and reviews), "
    "Conversion (consultation booking), Retention (loyalty program and referrals). "
    "Professional business graphic, minimalist style, icons for each stage, white background."
)
generate_image(inline3_prompt, "inline-3.png", model="gpt-image-1", size="1024x1024", quality="medium")

print("\nAll images generated successfully!")
