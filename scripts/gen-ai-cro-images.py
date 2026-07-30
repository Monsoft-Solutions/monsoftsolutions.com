#!/usr/bin/env python3
"""
Generate images for ai-conversion-rate-optimization-small-business
Hero: gpt-image-1 high quality 1536x1024 (gpt-image-1.5 alias)
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
SLUG = 'ai-conversion-rate-optimization-small-business'
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
    """Try nano-banana-pro (Gemini imagen); return True on success."""
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
print('\n=== Generating hero (gpt-image-1, high, 1536x1024) ===')
hero_prompt = (
    "A focused small business owner — a professional woman in her late 30s — seated at a "
    "clean, modern desk looking at a large monitor. The monitor displays a website "
    "conversion optimization dashboard: at the top, a conversion rate gauge showing an "
    "improvement from 1.8 percent to 4.2 percent with a green upward arrow. Below that, a "
    "heatmap overlay of a webpage showing hot spots where visitors click, and a side panel "
    "with A/B test results comparing two headline variants. The workspace has warm, natural "
    "window light, a laptop to the side, and a clean professional aesthetic. No text visible "
    "in the real-world environment. Photorealistic, aspirational business photography."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    save_image(hero_data, 'hero.png')
else:
    print('  Hero generation failed')

# ---- INLINE 1 ----
print('\n=== Generating inline-1 (nano-banana-pro / gpt-image-1 fallback) ===')
inline1_prompt = (
    "A clean infographic titled 'The CRO Funnel' showing website visitor drop-off stages. "
    "Top of funnel: 1,000 Website Visitors (large blue block). "
    "Stage 2: 350 View a Key Page (medium teal block). "
    "Stage 3: 120 Engage with CTA (smaller green block). "
    "Stage 4: 45 Start the Form (even smaller block). "
    "Stage 5: 22 Complete and Submit (small gold block). "
    "Stage 6: 14 Become Leads (bottom, smallest block). "
    "Each stage has a small icon and label. Beside each drop-off point, a small red 'leak' "
    "icon shows where visitors leave, with a short label like 'Unclear value prop' or "
    "'Too many form fields'. Modern flat design, blue-to-teal gradient color scheme, white "
    "background. Professional B2B infographic style."
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
    "A split-screen A/B test comparison showing two versions of a small business service "
    "page on a desktop browser mockup. Left side labeled 'Version A (Control)': generic "
    "headline 'Welcome to Our Services', a plain gray CTA button that says 'Learn More', "
    "no social proof. Right side labeled 'Version B (Winner +52% Lift)': bold, specific "
    "headline 'Get More Customers With AI Automation', a bright orange CTA button saying "
    "'Get Your Free Strategy Call', and three small star-rating testimonial snippets below "
    "the button. A green banner at the top of Version B reads '+52% More Conversions'. "
    "Clean SaaS UI mockup style, modern web design aesthetic, professional B2B visual."
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
    "A 30-day CRO quick-start roadmap infographic for small business owners. "
    "Four horizontal week bands stacked vertically: "
    "Week 1 (blue) — 'Audit Your Baseline': icons for heatmaps, session recording, and "
    "Google Analytics. Key tasks listed beside each icon. "
    "Week 2 (teal) — 'Fix the Quick Wins': icons for CTA buttons, simplified contact form, "
    "and page speed meter. "
    "Week 3 (green) — 'Launch Your First A/B Test': icons for split-test diagram and "
    "analytics graph. "
    "Week 4 (dark navy) — 'Analyze and Scale': icons for upward trend chart and checklist. "
    "Clean, professional timeline layout on a white background. Modern B2B infographic "
    "aesthetic with subtle drop shadows on each week band."
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
