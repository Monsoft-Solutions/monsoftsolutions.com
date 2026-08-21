#!/usr/bin/env python3
"""Generate images for the Snowbird Season Prep for Local Businesses blog post."""

import os
import sys
import base64
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = "/root/projects/monsoftsolutions.com/src/data/blog/snowbird-season-prep-local-business-guide/images"
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


# Hero image — gpt-image-1, 1536x1024, high quality
# Warm Florida coastal business scene welcoming snowbird customers
hero_prompt = (
    "A warm, inviting scene of a thriving local small business on a sunny Southwest Florida street. "
    "A cheerful business owner stands outside their shop — perhaps a boutique, restaurant, or salon — "
    "greeting arriving winter visitors with a welcoming smile. Palm trees line the sunny street, "
    "blue skies overhead, a 'Welcome Back' sign visible in the window. The atmosphere feels vibrant, "
    "prosperous, and ready for the busy season. Photorealistic, golden-hour warm lighting, "
    "Florida coastal town aesthetic, optimistic and energetic mood."
)
generate_image(hero_prompt, "hero.png", model="gpt-image-1", size="1536x1024", quality="high")

# Inline 1 — Seasonal prep checklist / timeline graphic
inline1_prompt = (
    "A clean, modern infographic showing an 8-week business preparation timeline for a busy season. "
    "Flat design style with warm teal, coral, and sandy beige color palette. "
    "Timeline flows from left to right with milestone icons: "
    "Week 1 (audit & assessment), Week 2-3 (marketing planning), Week 4-5 (website & digital updates), "
    "Week 6-7 (automation setup), Week 8 (launch campaigns). "
    "Checkboxes, calendar icons, and progress indicators. "
    "Professional business infographic style, white background, modern sans-serif typography."
)
generate_image(inline1_prompt, "inline-1.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 2 — Business owner reviewing seasonal marketing dashboard
inline2_prompt = (
    "A local small business owner — a woman in her 40s in business-casual attire — sits at a bright, "
    "modern desk reviewing a marketing analytics dashboard on a large monitor. "
    "The dashboard shows seasonal booking trends, customer acquisition graphs, and campaign performance. "
    "The office has warm Florida sunlight streaming through windows, plants, and professional decor. "
    "She looks confident and prepared. Photorealistic, bright natural lighting, productive workspace atmosphere."
)
generate_image(inline2_prompt, "inline-2.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 3 — Partnership / community marketing visual
inline3_prompt = (
    "A clean, modern diagram showing a local business partnership network for seasonal marketing. "
    "Flat design with warm blue, teal, and gold color palette. "
    "Hub-and-spoke layout with a central 'Local Business' icon surrounded by connected partners: "
    "hotel/resort, real estate agent, golf club, restaurant, boutique shop, and tourism board. "
    "Partnership arrows show referral flows between nodes. "
    "Professional business graphic, minimalist style, white background, icons for each partner type."
)
generate_image(inline3_prompt, "inline-3.png", model="gpt-image-1", size="1024x1024", quality="medium")

print("\nAll images generated successfully!")
