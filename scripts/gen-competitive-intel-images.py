#!/usr/bin/env python3
"""
Generate images for ai-competitive-intelligence-small-business-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with fallback to gpt-image-1 medium 1024x1024
Then uploads to Vercel Blob (vwy1t1uzxwusskun store)
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'ai-competitive-intelligence-small-business-guide'
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


def generate_image_gemini(prompt):
    """Generate image via Gemini nano-banana-pro (gemini-3-pro-image-preview)"""
    if not GEMINI_KEY:
        raise Exception('No Gemini API key available')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={GEMINI_KEY}'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']}
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        parts = data['candidates'][0]['content']['parts']
        for part in parts:
            if 'inlineData' in part:
                img_bytes = part['inlineData']['data']
                # Check if it's base64 or raw bytes
                if isinstance(img_bytes, str):
                    return base64.b64decode(img_bytes)
                return img_bytes
        raise Exception('No image in Gemini response')
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Gemini API error {e.code}: {body[:400]}')


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
        'use_gemini': False,
        'prompt': (
            'A confident small business owner sitting at a sleek modern desk, reviewing a competitive '
            'intelligence dashboard on a large widescreen monitor. The screen displays colorful competitor '
            'comparison charts, market share graphs, ranking trends, and AI-powered insights. The office '
            'is bright and professional with warm natural light coming through a window, a potted plant '
            'in the background, and a clean minimalist workspace. The owner looks focused and strategic, '
            'leaning forward with interest. Business casual attire. Photorealistic, professional, empowering tone. '
            'No text overlays on the image.'
        ),
    },
    {
        'file': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'use_gemini': True,
        'prompt': (
            'A clean professional infographic illustration showing five competitive intelligence monitoring '
            'areas for small businesses. Five distinct colored sections with icons: SEO & Content (magnifying '
            'glass with chart), Social Media (speech bubble with analytics), Customer Reviews (star rating '
            'gauge), Advertising (megaphone with targeting icon), and Pricing (price tag with comparison '
            'arrows). Modern flat design, business blue and teal color palette with orange accents. '
            'White background, clear visual hierarchy, minimalist icons. Infographic style, no text needed.'
        ),
    },
    {
        'file': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'use_gemini': True,
        'prompt': (
            'A professional illustration of a laptop screen showing an AI-powered competitive intelligence '
            'dashboard. The interface displays competitor comparison tables, keyword ranking charts with '
            'green and red trend arrows, social media performance metrics, and review sentiment scores. '
            'Clean modern SaaS UI design, dark mode interface with colorful data visualizations. '
            'A small business owner\'s hand is visible on the keyboard, engaged with the data. '
            'Tech-forward, data-driven aesthetic. No specific brand logos visible.'
        ),
    },
    {
        'file': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'use_gemini': True,
        'prompt': (
            'A small business owner sitting at a coffee shop table, working on a tablet showing a '
            'competitor analysis report. The screen shows a SWOT-style framework with checkmarks, '
            'market gap opportunities highlighted in green, and competitor weakness areas marked. '
            'A coffee cup and notebook with strategic notes are on the table. The background shows '
            'a modern urban coffee shop with soft bokeh. Thoughtful, strategic pose — the owner is '
            'taking notes. Warm natural lighting, photorealistic, entrepreneurial vibe.'
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

        # Try Gemini for inline images first
        if img.get('use_gemini') and GEMINI_KEY:
            print(f'[1/2] Generating {fname} via nano-banana-pro (Gemini)...')
            try:
                img_bytes = generate_image_gemini(img['prompt'])
                with open(local_path, 'wb') as f:
                    f.write(img_bytes)
                size_kb = len(img_bytes) / 1024
                print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB) [nano-banana-pro]')
                # Upload and continue
                print(f'[2/2] Uploading to Vercel Blob as {blob_path}...')
                url = upload_to_blob(local_path, blob_path)
                results[fname] = url
                print(f'      ✅ {url}')
                print()
                continue
            except Exception as e:
                print(f'      ⚠️ nano-banana-pro failed: {e}')
                print(f'      🔄 Falling back to gpt-image-1...')

        # OpenAI generation (hero or fallback)
        model = img['model']
        quality = img['quality']
        size = img['size']
        print(f'[1/2] Generating {fname} (model={model}, quality={quality}, size={size})...')
        try:
            img_bytes = generate_image_openai(img['prompt'], model=model, quality=quality, size=size)
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB)')
        except Exception as e:
            print(f'      ❌ Generation failed: {e}')
            # Fallback to gpt-image-1 if gpt-image-1.5 fails
            if model == 'gpt-image-1.5':
                print(f'      🔄 Retrying with gpt-image-1...')
                try:
                    img_bytes = generate_image_openai(img['prompt'], model='gpt-image-1', quality=quality, size=size)
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

    # Save manifest
    manifest_path = IMAGES_DIR / 'blob-manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\nManifest saved to {manifest_path}')


if __name__ == '__main__':
    main()
