#!/usr/bin/env python3
"""
Generate images for ai-customer-support-automation-small-business-guide
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
SLUG = 'ai-customer-support-automation-small-business-guide'
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
    "A friendly small business customer support team member at a modern desk, smiling while "
    "working on a laptop. The screen shows a clean AI-powered helpdesk dashboard with resolved "
    "ticket counts, automated response metrics, and a satisfaction score gauge showing high ratings. "
    "Floating UI elements around the screen show chat bubbles, email icons, and a checkmark "
    "indicating resolved cases. Warm, professional office setting with natural light. "
    "The atmosphere conveys efficiency, calm, and human-tech partnership. "
    "No text overlays. Photorealistic style."
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

# ── Inline 1: AI Helpdesk Workflow / Ticket Routing ──────────────────────────
generate_with_fallback(
    "Clean flat-design infographic showing an AI customer support workflow. "
    "Flow diagram: customer message arrives → AI classifies and tags ticket → "
    "simple queries answered automatically by AI knowledge base → "
    "complex issues routed to human agent with full context. "
    "Icons for chat, email, and phone channels at the top. "
    "Color-coded priority levels (green low, yellow medium, red urgent). "
    "Modern SaaS dashboard aesthetic, no real brand logos. "
    "Blue and teal color palette. Professional business illustration.",
    'inline-1.png'
)

# ── Inline 2: AI Knowledge Base / Self-Service Portal ────────────────────────
generate_with_fallback(
    "A customer on a smartphone browsing a clean, modern self-service help center portal. "
    "The screen shows a search bar with suggested FAQ articles appearing instantly as they type. "
    "An AI assistant chat bubble appears in the corner offering help. "
    "The interface looks professional and easy to navigate — clear categories, "
    "article thumbnails, and a satisfaction rating widget. "
    "Bright, welcoming design. No real brand UI replicated. Photorealistic product mockup.",
    'inline-2.png'
)

# ── Inline 3: Support Metrics / CSAT Dashboard ───────────────────────────────
generate_with_fallback(
    "A business owner reviewing a customer support analytics dashboard on a desktop monitor. "
    "The dashboard shows key metrics: average response time (reduced from hours to minutes), "
    "ticket deflection rate (showing 60% of tickets resolved by AI), customer satisfaction "
    "score (4.8 stars), and a trend line showing improvement over time. "
    "Clean, modern data visualization with bar charts and line graphs. "
    "The business owner looks pleased and confident. Professional office setting. "
    "No real software UI replicated. Photorealistic style.",
    'inline-3.png'
)

print('\n✅ All images generated.')
