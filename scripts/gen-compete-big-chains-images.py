#!/usr/bin/env python3
"""
Generate images for local-business-compete-big-chains-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: gpt-image-1 medium quality 1024x1024
(nano-banana-pro/Gemini API not available — GOOGLE_API_KEY is invalid for Gemini)
Then uploads to Vercel Blob (vwy1t1uzxwusskun store)
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'local-business-compete-big-chains-guide'
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
            'A confident, smiling small business owner standing in front of their charming local shop '
            'on a sunny Main Street. Behind them, a large chain store is visible further down the street, '
            'but customers are clearly walking into the local shop. The owner holds a tablet showing '
            'customer analytics and a five-star rating. Warm sunlight, community feel, modern yet cozy '
            'storefront with plants and a handwritten sign. Wide landscape composition. Photorealistic, '
            'optimistic, empowering tone. No text overlays.'
        ),
    },
    {
        'file': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean flat-design infographic showing local business competitive advantages over big chains. '
            'Four colored pillars or panels: Personalization (handshake icon), Speed (lightning bolt), '
            'Community (heart with people), and Local Expertise (map pin with star). '
            'Professional business style, warm earth tones mixed with teal and blue accents. '
            'Modern iconography, white background, clear visual hierarchy. No lengthy text needed.'
        ),
    },
    {
        'file': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A professional illustration of a small business technology dashboard on a laptop screen. '
            'The screen shows a simple CRM dashboard with customer names, automated follow-up sequences, '
            'AI chatbot activity, appointment bookings, and Google review ratings. Clean modern UI with '
            'green success indicators. A local business owner is smiling while reviewing the data. '
            'Warm office lighting, desk setting. Tech-empowered small business theme.'
        ),
    },
    {
        'file': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A vibrant local community scene showing multiple small businesses thriving on a neighborhood '
            'street. Customers with shopping bags, a coffee shop with a line out the door, a salon with '
            'a glowing five-star sign in the window, and a contractor with a branded van parked out front. '
            'Warm afternoon light, diverse friendly community. Southwest Florida suburban street with palm '
            'trees visible. Optimistic, community-centered, photorealistic illustration style.'
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
                    print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB) [fallback]')
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
