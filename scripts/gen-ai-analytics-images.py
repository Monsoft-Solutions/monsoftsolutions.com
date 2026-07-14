#!/usr/bin/env python3
"""
Generate images for ai-analytics-small-business-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
SLUG = 'ai-analytics-small-business-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_openai(prompt, model='gpt-image-1', quality='medium', size='1024x1024'):
    """Generate image via OpenAI images API."""
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'n': 1,
        'size': size,
        'quality': quality
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            b64 = data['data'][0]['b64_json']
            return base64.b64decode(b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  OpenAI error {e.code}: {body[:300]}')
        return None
    except Exception as e:
        print(f'  OpenAI exception: {e}')
        return None


def try_nano_banana(prompt, filename):
    """Try nano-banana-pro (Gemini); return True on success."""
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not gemini_key:
        print('  No Gemini key available')
        return False
    try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key={gemini_key}'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']}
        }).encode()
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    img_bytes = base64.b64decode(part['inlineData']['data'])
                    path = IMAGES_DIR / filename
                    path.write_bytes(img_bytes)
                    print(f'  ✓ nano-banana-pro saved {filename} ({len(img_bytes):,} bytes)')
                    return True
        print('  nano-banana-pro: no image in response')
        return False
    except Exception as e:
        print(f'  nano-banana-pro failed: {e}')
        return False


def save_image(data, filename):
    path = IMAGES_DIR / filename
    path.write_bytes(data)
    print(f'  ✓ Saved {filename} ({len(data):,} bytes)')


# ---- HERO ----
print('\n=== Generating hero (gpt-image-1.5, high, 1536x1024) ===')
hero_prompt = (
    "A focused small business owner — a confident man in his 40s — sitting at a modern desk "
    "in a clean, well-lit office. He's looking at a large monitor displaying a colorful AI "
    "business analytics dashboard with revenue trend lines, customer acquisition charts, and "
    "a natural language query box showing 'Which services grew the most this quarter?' with "
    "an AI-generated plain-English answer card visible below. A laptop, coffee cup, and "
    "notebook are on the desk. The workspace has warm natural light from a window. "
    "Professional, aspirational, clean photography aesthetic. No distracting text in the "
    "real-world environment. Photorealistic style."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    save_image(hero_data, 'hero.png')
else:
    print('  Hero generation failed')

# ---- INLINE 1 ----
print('\n=== Generating inline-1 (nano-banana-pro / gpt-image-1 fallback) ===')
inline1_prompt = (
    "A clean, professional infographic showing five types of small business data flowing into "
    "an AI analytics hub in the center. Five labeled icons branch outward: "
    "1) a dollar sign for Revenue & Sales Data, "
    "2) a funnel for Customer Acquisition Data, "
    "3) a heart/star for Customer Retention Data, "
    "4) a gear for Operational Data, "
    "5) a megaphone for Marketing Performance Data. "
    "Center hub is labeled 'AI Analytics' with a brain/circuit icon. "
    "Clean, modern flat design style. Blue and teal color palette on white background. "
    "Professional B2B infographic aesthetic."
)
if not try_nano_banana(inline1_prompt, 'inline-1.png'):
    print('  Falling back to gpt-image-1...')
    inline1_data = generate_openai(inline1_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline1_data:
        save_image(inline1_data, 'inline-1.png')
    else:
        print('  inline-1 generation failed')

# ---- INLINE 2 ----
print('\n=== Generating inline-2 (nano-banana-pro / gpt-image-1 fallback) ===')
inline2_prompt = (
    "A realistic screenshot-style image of a small business analytics dashboard on a laptop "
    "screen. The dashboard shows four key metric cards at the top: Monthly Revenue (with "
    "upward trend arrow), New Leads This Week, Customer Retention Rate, and Top Service by "
    "Revenue. Below the cards are two charts: a bar chart comparing this month vs last month "
    "revenue, and a pie chart showing lead sources (Google 45%, Referrals 30%, Social 25%). "
    "Clean, modern SaaS UI design. Blue and white color scheme. Professional data "
    "visualization aesthetic."
)
if not try_nano_banana(inline2_prompt, 'inline-2.png'):
    print('  Falling back to gpt-image-1...')
    inline2_data = generate_openai(inline2_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline2_data:
        save_image(inline2_data, 'inline-2.png')
    else:
        print('  inline-2 generation failed')

# ---- INLINE 3 ----
print('\n=== Generating inline-3 (nano-banana-pro / gpt-image-1 fallback) ===')
inline3_prompt = (
    "A 30-day calendar-style roadmap infographic for small business analytics setup. "
    "Four weeks shown as colored horizontal bands: "
    "Week 1 (blue) labeled 'Define & Collect' with icons for questions and data export, "
    "Week 2 (teal) labeled 'Connect & Visualize' with dashboard icons, "
    "Week 3 (green) labeled 'Automate & Alert' with bell/alert icons, "
    "Week 4 (dark blue) labeled 'Act & Iterate' with checkmark and growth icons. "
    "Clean, modern timeline design. Professional business infographic aesthetic on white "
    "background with subtle shadow. Each week has 2-3 small milestone icons."
)
if not try_nano_banana(inline3_prompt, 'inline-3.png'):
    print('  Falling back to gpt-image-1...')
    inline3_data = generate_openai(inline3_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline3_data:
        save_image(inline3_data, 'inline-3.png')
    else:
        print('  inline-3 generation failed')

print('\n=== All images done ===')
for f in sorted(IMAGES_DIR.glob('*.png')):
    print(f'  {f.name}: {f.stat().st_size:,} bytes')
