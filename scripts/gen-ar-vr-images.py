#!/usr/bin/env python3
"""
Generate images for ar-vr-small-business-guide
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
SLUG = 'ar-vr-small-business-guide'
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
            'A small business owner wearing a sleek AR headset while standing in their modern retail store. '
            'Through the AR lenses, holographic product information and customer data float around the store. '
            'Other customers use their smartphones to see augmented reality product try-ons on a nearby display. '
            'Warm, well-lit retail environment with wooden shelves and plants. The scene feels innovative yet '
            'approachable — not sci-fi, but practical near-future retail. Wide landscape composition, '
            'photorealistic, optimistic tone. No text overlays.'
        ),
    },
    {
        'file': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A professional flat-design infographic showing four AR/VR use cases for small businesses. '
            'Four panels with icons: Virtual Try-On (person looking in AR mirror), Virtual Tours '
            '(house with VR goggles icon), Staff Training (VR headset with graduation cap), and '
            'Product Visualization (3D product floating above a phone). '
            'Modern business color palette — teal, deep blue, white, with orange accents. '
            'Clean iconography, professional layout, no lengthy text needed.'
        ),
    },
    {
        'file': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A customer in a stylish retail boutique using a smartphone to see an AR product try-on. '
            'On the phone screen, they can see themselves wearing sunglasses virtually before buying. '
            'The store is modern and inviting, with other products visible on well-lit shelves. '
            'Another customer nearby watches with curiosity and smiles. '
            'Warm retail lighting, photorealistic, contemporary shopping experience. '
            'The technology feels accessible and fun, not intimidating.'
        ),
    },
    {
        'file': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A medical spa or aesthetic practice reception area where a patient uses a tablet '
            'showing a before-and-after AR simulation of a treatment result on their own face. '
            'The interface shows a clear split view — current photo on the left, simulated result '
            'on the right. A friendly practitioner stands alongside, explaining the options. '
            'Clean, modern, luxurious med-spa aesthetic with soft lighting, white walls, and greenery. '
            'Photorealistic, trustworthy, professional medical setting.'
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

        print(f'[GEN] Generating {fname} (model={img["model"]}, quality={img["quality"]}, size={img["size"]})...')
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

        print(f'[UP]  Uploading to Vercel Blob as {blob_path}...')
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
