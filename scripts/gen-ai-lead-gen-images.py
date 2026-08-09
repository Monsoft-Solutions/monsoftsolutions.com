#!/usr/bin/env python3
"""
Generate images for ai-lead-generation-small-business-guide
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
SLUG = 'ai-lead-generation-small-business-guide'
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
    "A confident small business owner sitting at a modern desk reviewing a laptop screen showing "
    "an AI-powered lead generation dashboard. The screen displays an incoming leads panel with "
    "prospect cards, qualification scores, pipeline stages, and conversion metrics with upward "
    "trend arrows. Sticky notes on the desk with business names suggest real prospect activity. "
    "The office is warm and professional — a local service business or boutique agency feel. "
    "Natural light from a window. A coffee mug nearby. The atmosphere conveys growth, "
    "efficiency, and optimism. No text overlays. Photorealistic style."
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

# ── Inline 1: AI Prospecting Workflow Diagram ────────────────────────────────
generate_with_fallback(
    "A clean flat-design infographic illustrating an AI lead generation workflow for small business. "
    "Flow diagram showing: Target Audience Definition → AI Prospect Search → "
    "Lead Data Enrichment → Automated Outreach Sequence → Lead Qualification → "
    "CRM Entry and Follow-Up. "
    "Icons for each stage: magnifying glass, database, email, chat bubble, star rating, CRM grid. "
    "Modern SaaS illustration style with teal, blue, and white color palette. "
    "No real company logos or brand names. Clean, professional business infographic.",
    'inline-1.png'
)

# ── Inline 2: AI Chatbot Lead Capture on Website ─────────────────────────────
generate_with_fallback(
    "A modern small business website on a desktop screen featuring an AI lead capture chatbot. "
    "The chat widget is open in the bottom right corner showing a friendly conversation: "
    "the AI asks qualifying questions like 'What service are you looking for?' and "
    "'What's the best way to reach you?' A lead capture form is partially visible. "
    "The website behind it looks like a professional local service business or medical spa. "
    "Clean, inviting design. The chatbot avatar is a simple friendly icon. "
    "No real brand UI replicated. Professional product mockup style.",
    'inline-2.png'
)

# ── Inline 3: Qualified Leads in CRM ─────────────────────────────────────────
generate_with_fallback(
    "A business development manager reviewing a clean CRM pipeline dashboard on a monitor. "
    "The screen shows AI-qualified leads organized in Kanban columns: New Lead, Contacted, "
    "Qualified, Proposal Sent, Closed. Each lead card has a score badge (high/medium/low), "
    "contact info fields, and a next-action button. A sidebar shows AI insights: "
    "'Best time to call', 'Similar deals won in 8 days', 'Warm lead — follow up today'. "
    "The person looks focused and strategic. Professional office setting with plants. "
    "No real software UI replicated. Photorealistic style.",
    'inline-3.png'
)

print('\n✅ All images generated.')
