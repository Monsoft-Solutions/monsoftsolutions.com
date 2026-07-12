#!/usr/bin/env python3
"""
Generate images for conversion-tracking-small-business-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: gpt-image-1 medium quality 1024x1024
(nano-banana-pro/Gemini API not available — GOOGLE_API_KEY is invalid for Gemini)
Then uploads to Vercel Blob
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'conversion-tracking-small-business-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')

IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_image_openai(prompt, model='gpt-image-1', quality='medium', size='1024x1024'):
    """Generate image via OpenAI"""
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
        resp = urllib.request.urlopen(req, timeout=180)
        data = json.loads(resp.read())
        img_b64 = data['data'][0]['b64_json']
        return base64.b64decode(img_b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'OpenAI API error {e.code}: {body[:400]}')


def upload_to_blob(local_path, blob_path):
    """Upload file to Vercel Blob via REST PUT"""
    with open(local_path, 'rb') as f:
        file_data = f.read()
    content_type = 'image/png'
    url = f'https://blob.vercel-storage.com/{blob_path}'
    headers = {
        'Authorization': f'Bearer {BLOB_TOKEN}',
        'Content-Type': content_type,
        'x-content-type': content_type,
        'x-add-random-suffix': 'false',
        'x-cache-control-max-age': '31536000',
    }
    req = urllib.request.Request(url, data=file_data, headers=headers, method='PUT')
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        return result.get('url', '')
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Blob upload error {e.code}: {body[:400]}')


IMAGES = [
    {
        'file': 'hero.png',
        'model': 'gpt-image-1.5',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A small business owner sitting at a clean modern desk, smiling confidently while reviewing '
            'a laptop screen showing a colorful analytics dashboard. The dashboard displays glowing green '
            'metrics: phone call conversions, form submissions, appointment bookings, and revenue sources. '
            'A coffee mug and notebook sit nearby. Warm office lighting with natural window light. '
            'The owner looks empowered and in control, not confused by data. Professional setting, '
            'photorealistic style, optimistic and approachable tone. Wide landscape format. No text overlays.'
        ),
    },
    {
        'file': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean flat-design infographic diagram showing the website visitor-to-customer journey '
            'for a small business. Five connected steps in a horizontal flow with icons: '
            '1) Website Visitor (person icon with cursor), '
            '2) Browses Pages (browser window icon), '
            '3) Takes Action (arrow clicking button), '
            '4) Conversion Event (checkmark in circle — phone call, form submit, or booking), '
            '5) New Customer (handshake icon with dollar sign). '
            'Connected by arrows. Modern flat design, teal and blue color palette, white background, '
            'professional business infographic style. No lengthy text, just minimal labels.'
        ),
    },
    {
        'file': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean illustration of a Google Analytics 4 style dashboard displayed on a modern laptop screen. '
            'The screen shows a conversions report with a bar chart comparing traffic sources: '
            'Organic Search, Google Ads, Direct, Social Media — each bar colored differently. '
            'A highlighted section shows "Top Conversions" with icons for phone calls, contact forms, '
            'and appointment bookings, each with green upward trend arrows. '
            'Clean data visualization, professional dark-on-light UI design, office desk setting. '
            'No real brand logos — fictional UI elements only. Realistic but slightly stylized.'
        ),
    },
    {
        'file': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A side-by-side comparison illustration showing two small business scenarios. '
            'LEFT side labeled "Without Tracking" — a frustrated business owner looking at a blank screen '
            'with a question mark, stacks of receipts, and a thought bubble showing "Which ad worked?". '
            'RIGHT side labeled "With Tracking" — the same owner smiling at a clear pie chart showing '
            'exactly which channel brought in the most calls and bookings. Clean flat cartoon style, '
            'warm teal and orange color scheme, white background. Empowering, clear visual contrast.'
        ),
    },
]


def main():
    print(f'Generating {len(IMAGES)} images for {SLUG}...\n')
    results = {}

    for img in IMAGES:
        fname = img['file']
        local_path = IMAGES_DIR / fname
        blob_path = f'blog/{SLUG}/{fname}'

        print(f'[1/2] Generating {fname} (model={img["model"]}, quality={img["quality"]}, size={img["size"]})...')
        try:
            img_bytes = generate_image_openai(
                img['prompt'],
                model=img['model'],
                quality=img['quality'],
                size=img['size']
            )
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB)')
        except Exception as e:
            print(f'      ❌ Generation failed: {e}')
            # Fallback to gpt-image-1 if gpt-image-1.5 fails
            if img['model'] == 'gpt-image-1.5':
                print(f'      🔄 Retrying with gpt-image-1...')
                try:
                    img_bytes = generate_image_openai(img['prompt'], model='gpt-image-1', quality=img['quality'], size=img['size'])
                    with open(local_path, 'wb') as f:
                        f.write(img_bytes)
                    size_kb = len(img_bytes) / 1024
                    print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB) [fallback gpt-image-1]')
                except Exception as e2:
                    print(f'      ❌ Fallback also failed: {e2}')
                    continue
            else:
                continue

        print(f'[2/2] Uploading to Vercel Blob as {blob_path}...')
        try:
            url = upload_to_blob(local_path, blob_path)
            results[fname] = url
            print(f'      ✅ {url}')
        except Exception as e:
            print(f'      ❌ Upload failed: {e}')

        print()

    print('=' * 60)
    print('FINAL BLOB URLs:')
    for fname, url in results.items():
        print(f'  {fname}: {url}')
    print('=' * 60)


if __name__ == '__main__':
    main()
