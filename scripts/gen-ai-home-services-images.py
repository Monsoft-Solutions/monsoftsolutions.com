#!/usr/bin/env python3
"""
Generate images for ai-home-services-business-guide
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
SLUG = 'ai-home-services-business-guide'
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
            'generationConfig': {'responseModalities': ['TEXT', 'IMAGE']}
        }).encode()
        req = urllib.request.Request(url, data=payload, headers=headers)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    img_data = base64.b64decode(part['inlineData']['data'])
                    path = IMAGES_DIR / filename
                    path.write_bytes(img_data)
                    print(f'  ✅ nano-banana-pro: {filename} ({len(img_data)//1024}KB)')
                    return True
        print('  nano-banana-pro: no image in response')
        return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  nano-banana-pro HTTP {e.code}: {body[:200]}')
        return False
    except Exception as e:
        print(f'  nano-banana-pro exception: {e}')
        return False


def generate_with_fallback(prompt, filename, size='1024x1024'):
    """Try nano-banana-pro first, fall back to gpt-image-1."""
    print(f'\n→ Generating {filename}...')
    print('  Trying nano-banana-pro...')
    if try_nano_banana(prompt, filename):
        return True
    print('  Falling back to gpt-image-1...')
    data = generate_openai(prompt, model='gpt-image-1', quality='medium', size=size)
    if data:
        path = IMAGES_DIR / filename
        path.write_bytes(data)
        print(f'  ✅ gpt-image-1 fallback: {filename} ({len(data)//1024}KB)')
        return True
    print(f'  ❌ Failed: {filename}')
    return False


# ── Hero image (gpt-image-1.5, high quality, 1536x1024) ─────────────────────
print('\n=== Generating hero image with gpt-image-1.5 ===')
hero_prompt = (
    "A confident home services business owner standing in front of a modern white service van "
    "in a sunny residential neighborhood. He is wearing a clean branded polo shirt and looking "
    "at a tablet displaying a scheduling dashboard with job routes, customer appointments, and "
    "AI-powered recommendations. The dashboard shows color-coded job statuses, a map with stops, "
    "and automated customer notifications. Suburban homes with green lawns in the background, "
    "bright summer daylight. Professional and approachable. No real brand logos visible. "
    "Photorealistic style."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1.5', quality='high', size='1536x1024')
if not hero_data:
    print('gpt-image-1.5 failed, trying gpt-image-1...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    path = IMAGES_DIR / 'hero.png'
    path.write_bytes(hero_data)
    print(f'✅ Hero saved: hero.png ({len(hero_data)//1024}KB)')
else:
    print('❌ Hero generation failed')

# ── Inline 1: AI Scheduling & Dispatch Workflow ──────────────────────────────
generate_with_fallback(
    "A clean flat-design infographic showing an AI-powered home services scheduling workflow. "
    "A horizontal flow with five connected steps and icons: "
    "1) Customer Request (phone/chat icon) → 2) AI Booking (calendar with sparkle) → "
    "3) Smart Dispatch (map pin with route) → 4) Tech on the Job (wrench/tools icon) → "
    "5) Automated Follow-Up (star/review icon). "
    "Color palette: deep navy blue, sky blue, and white. Clean sans-serif labels. "
    "Modern SaaS illustration style. White background. No brand logos.",
    'inline-1.png'
)

# ── Inline 2: Before/After Comparison — Manual vs AI Operations ──────────────
generate_with_fallback(
    "A split-panel comparison illustration for a home services business. "
    "LEFT panel (labeled 'Without AI', red/orange tone): A stressed HVAC technician in a van "
    "surrounded by a paper schedule clipboard, missed calls shown on his phone, handwritten "
    "invoices, and a customer giving a 2-star review on a laptop in the background. "
    "RIGHT panel (labeled 'With AI', green/teal tone): The same technician looking calm and "
    "organized, checking a tablet with a clean digital schedule, automated texts going to "
    "customers, digital invoices being generated, and a 5-star review notification. "
    "Professional business illustration style. No real brand logos or software UI.",
    'inline-2.png'
)

# ── Inline 3: Home Services Tech Stack Overview ───────────────────────────────
generate_with_fallback(
    "A professional home services business owner at a clean desk reviewing a tech stack "
    "overview on a monitor. The screen shows a dashboard with four connected tool categories: "
    "Field Service Management (calendar/dispatch icon), CRM & Automation (person/flow icon), "
    "AI Estimating (calculator/document icon), and Review Generation (star/megaphone icon). "
    "Connecting arrows show how data flows between each tool. The owner looks confident and "
    "organized. Modern home office with natural light. No real software logos visible. "
    "Clean photorealistic style.",
    'inline-3.png'
)

print('\n✅ All images generated.')
