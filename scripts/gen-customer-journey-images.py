#!/usr/bin/env python3
"""Generate images for the Customer Journey Mapping for Small Business blog post."""

import os
import sys
import base64
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = "/root/projects/monsoftsolutions.com/src/data/blog/customer-journey-mapping-small-business-guide/images"
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


# Hero image — gpt-image-1, 1536x1024, high quality
# Business owner mapping out customer journey on a whiteboard
hero_prompt = (
    "A confident small business owner — a man in his late 30s in smart-casual attire — "
    "stands at a large modern whiteboard in a bright, airy office. "
    "The whiteboard shows a detailed customer journey map with five labeled stages: "
    "Awareness, Consideration, Decision, Purchase, and Loyalty. "
    "Sticky notes, arrows, and icons connect each stage. "
    "The owner is pointing at the 'Consideration' stage with a thoughtful, focused expression. "
    "Modern office with warm lighting, plants, and large windows showing daylight outside. "
    "Photorealistic, professional business setting, optimistic and strategic atmosphere."
)
generate_image(hero_prompt, "hero.png", model="gpt-image-1", size="1536x1024", quality="high")

# Inline 1 — Customer journey map diagram / infographic
inline1_prompt = (
    "A clean, professional customer journey map infographic for a small business. "
    "Flat design style with a blue, teal, and warm orange color palette. "
    "Five horizontal stages displayed as connected banner segments: "
    "1. Awareness (megaphone icon, Google Search / Social Media), "
    "2. Consideration (magnifying glass icon, Website / Reviews / Comparisons), "
    "3. Decision (checkmark icon, Booking / Inquiry / Call), "
    "4. Purchase (shopping bag icon, Service Delivery / Onboarding), "
    "5. Loyalty (heart icon, Follow-up / Reviews / Referrals). "
    "Below each stage: customer emotion (curious, interested, evaluating, satisfied, delighted). "
    "Modern sans-serif typography, white background, professional business infographic style."
)
generate_image(inline1_prompt, "inline-1.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 2 — Customer drop-off / funnel leakage visualization
inline2_prompt = (
    "A modern business analytics dashboard illustration showing a customer funnel with drop-off points. "
    "Clean flat design with blue, red, and green color coding. "
    "A funnel diagram showing: 1000 website visitors → 350 page engagements → 120 inquiries → 45 bookings → 38 repeat customers. "
    "Red warning icons highlight the biggest drop-off gaps between stages. "
    "Green checkmarks show successful conversion points. "
    "Small annotation labels explain why customers drop off at each stage. "
    "Dashboard-style layout, data visualization aesthetic, professional and clear."
)
generate_image(inline2_prompt, "inline-2.png", model="gpt-image-1", size="1024x1024", quality="medium")

# Inline 3 — Business owner reviewing journey analytics / taking action
inline3_prompt = (
    "A diverse team of three small business professionals — one woman and two men — "
    "gathered around a laptop and tablet in a modern, bright coworking space. "
    "The laptop screen shows a customer journey analytics dashboard with colorful graphs and conversion metrics. "
    "They are engaged, pointing at the screen and collaborating on next steps. "
    "One person takes notes on a notepad. Coffee cups on the table. "
    "Photorealistic, natural lighting from windows, collaborative and energetic atmosphere, "
    "professional small business team working together on marketing strategy."
)
generate_image(inline3_prompt, "inline-3.png", model="gpt-image-1", size="1024x1024", quality="medium")

print("\nAll images generated successfully!")
