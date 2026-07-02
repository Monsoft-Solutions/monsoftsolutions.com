#!/usr/bin/env python3
"""
Generate images for scaling-small-business-operations-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) if available, else gpt-image-1 medium 1024x1024
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
SLUG = 'scaling-small-business-operations-guide'
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
    """Try nano-banana-pro via Gemini API"""
    if not GEMINI_API_KEY:
        raise Exception('No Gemini API key available')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-fast-generate-001:predict?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'instances': [{'prompt': prompt}],
        'parameters': {'sampleCount': 1}
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        img_b64 = data['predictions'][0]['bytesBase64Encoded']
        return base64.b64decode(img_b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Gemini API error {e.code}: {body[:300]}')


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
        'engine': 'openai',
        'model': 'gpt-image-1.5',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A driven small business owner in their mid-thirties stands at a bright modern desk, '
            'reviewing a large monitor showing growth charts, team productivity dashboards, and '
            'an automation workflow diagram with green checkmarks. Stacks of organized folders, '
            'a coffee mug, and a tablet are on the desk. Through a wide window behind them, a '
            'thriving street of small businesses is visible — a bakery, a salon, a contractor van. '
            'Warm morning light, clean professional space. The mood is energized, optimistic, '
            'achievable growth. Wide landscape format. Photorealistic, high-detail. No text overlays.'
        ),
    },
    {
        'file': 'inline-1.png',
        'engine': 'gemini',
        'model': 'nano-banana-pro',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean, professional business infographic illustration showing four stages of small '
            'business scaling: Foundation (gear/process icon), Systems (automation workflow arrows), '
            'Team (people icons), and Growth (upward chart). Each stage in a connected horizontal '
            'flow with soft blue and green color palette. Modern flat design style, white background, '
            'minimal icons, professional business aesthetic. No lengthy text labels needed.'
        ),
    },
    {
        'file': 'inline-2.png',
        'engine': 'gemini',
        'model': 'nano-banana-pro',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A professional photo-realistic illustration of a small business owner delegating tasks '
            'to a small team in a modern light-filled workspace. A whiteboard behind them shows '
            'a simple workflow diagram. Team members at laptops appear engaged and capable. '
            'The owner gestures at a project plan. Warm office environment, collaborative feel, '
            'positive and empowering atmosphere. Diverse team, contemporary business casual attire.'
        ),
    },
    {
        'file': 'inline-3.png',
        'engine': 'gemini',
        'model': 'nano-banana-pro',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean professional business dashboard visualization on a modern computer screen. '
            'Shows key scaling metrics: revenue trend line going up, customer acquisition cost '
            'going down, team capacity bar chart, and automation time-savings counter. '
            'Modern data visualization style with soft green and blue accents on dark background. '
            'Professional SaaS-style UI design. A small business owner is visible reflected in '
            'the screen smiling. No specific brand logos.'
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

        print(f'Generating {fname} ({img["engine"]}: {img.get("model","")}, size={img["size"]})...')

        img_bytes = None

        if img['engine'] == 'gemini':
            # Try nano-banana-pro first
            try:
                img_bytes = generate_image_gemini(img['prompt'])
                print(f'  ✅ Gemini nano-banana-pro success ({len(img_bytes)//1024} KB)')
            except Exception as e:
                print(f'  ⚠️  Gemini failed: {e}')
                print(f'  🔄 Falling back to gpt-image-1...')
                try:
                    img_bytes = generate_image_openai(img['prompt'], model='gpt-image-1', quality='medium', size='1024x1024')
                    print(f'  ✅ gpt-image-1 fallback success ({len(img_bytes)//1024} KB)')
                except Exception as e2:
                    print(f'  ❌ Both failed: {e2}')
                    continue

        elif img['engine'] == 'openai':
            model = img.get('model', 'gpt-image-1')
            quality = img.get('quality', 'high')
            size = img.get('size', '1536x1024')
            try:
                img_bytes = generate_image_openai(img['prompt'], model=model, quality=quality, size=size)
                print(f'  ✅ {model} success ({len(img_bytes)//1024} KB)')
            except Exception as e:
                print(f'  ⚠️  {model} failed: {e}')
                if model != 'gpt-image-1':
                    print(f'  🔄 Falling back to gpt-image-1...')
                    try:
                        img_bytes = generate_image_openai(img['prompt'], model='gpt-image-1', quality=quality, size=size)
                        print(f'  ✅ gpt-image-1 fallback success ({len(img_bytes)//1024} KB)')
                    except Exception as e2:
                        print(f'  ❌ Fallback failed: {e2}')
                        continue
                else:
                    continue

        if img_bytes:
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            print(f'  💾 Saved to {local_path}')

            print(f'  ⬆️  Uploading to Vercel Blob as {blob_path}...')
            try:
                url = upload_to_blob(local_path, blob_path)
                results[fname] = url
                print(f'  ✅ {url}')
            except Exception as e:
                print(f'  ❌ Upload failed: {e}')

        print()

    print('=' * 60)
    print('FINAL BLOB URLs:')
    for fname, url in results.items():
        print(f'  {fname}: {url}')
    print('=' * 60)
    return results


if __name__ == '__main__':
    main()
