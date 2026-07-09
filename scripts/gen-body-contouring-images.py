#!/usr/bin/env python3
"""
Generate images for body-contouring-marketing-med-spa-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback
Uploads to Vercel Blob (vwy1t1uzxwusskun store)
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'body-contouring-marketing-med-spa-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')

IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_image_openai(prompt, model='gpt-image-1', quality='medium', size='1024x1024'):
    """Generate image via OpenAI Images API."""
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'n': 1,
        'size': size,
        'quality': quality,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=180)
        data = json.loads(resp.read())
        img_b64 = data['data'][0]['b64_json']
        return base64.b64decode(img_b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'OpenAI API error {e.code}: {body[:500]}')


def generate_image_gemini(prompt, size='1024x1024'):
    """Generate image via Gemini (nano-banana-pro / imagen-3.0-generate-002)."""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={GEMINI_KEY}'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'instances': [{'prompt': prompt}],
        'parameters': {
            'sampleCount': 1,
            'aspectRatio': '1:1',
        }
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        img_b64 = data['predictions'][0]['bytesBase64Encoded']
        return base64.b64decode(img_b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Gemini API error {e.code}: {body[:500]}')


def upload_to_blob(local_path, blob_path):
    """Upload file to Vercel Blob via REST PUT."""
    with open(local_path, 'rb') as f:
        file_data = f.read()
    url = f'https://blob.vercel-storage.com/{blob_path}'
    headers = {
        'Authorization': f'Bearer {BLOB_TOKEN}',
        'Content-Type': 'image/png',
        'x-content-type': 'image/png',
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
        'fallback': 'gpt-image-1',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A professionally lit medical spa consultation room where a warm, knowledgeable female '
            'practitioner in a white coat shows a female patient body analysis results on a sleek tablet. '
            'The tablet screen displays a personalized body contouring treatment plan with clean charts '
            'and timeline graphics. The patient — mid-30s, stylishly dressed — looks engaged and optimistic. '
            'Luxurious med spa aesthetic: soft warm lighting, sage green and white tones, fresh flowers, '
            'elegant furnishings. The atmosphere is sophisticated, trustworthy, and aspirational. '
            'Wide landscape composition. No text overlays. Photorealistic.'
        ),
    },
    {
        'file': 'inline-1.png',
        'model': 'nano-banana-pro',
        'fallback': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean, modern infographic showing four non-invasive body contouring treatment types in '
            'a 2x2 grid layout. Top left: fat freezing (CoolSculpting) with a snowflake icon and blue tones. '
            'Top right: electromagnetic muscle sculpting (Emsculpt) with a lightning bolt icon and teal tones. '
            'Bottom left: radiofrequency skin tightening with wave icon and warm gold tones. '
            'Bottom right: combination fat and muscle treatment with a combined icon and deep navy. '
            'Medical spa aesthetic: white background, clean iconography, professional typography. '
            'No words or labels — icons and colors convey meaning. Modern, premium, trustworthy design.'
        ),
    },
    {
        'file': 'inline-2.png',
        'model': 'nano-banana-pro',
        'fallback': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A confident, fit woman in her late 30s wearing sleek athletic wear, smiling with genuine '
            'confidence while looking in a modern floor-to-ceiling mirror in a bright, airy wellness studio. '
            'Soft natural light streams through large windows. The background is clean and minimal. '
            'The image conveys body confidence, wellness achievement, and positive self-image. '
            'No medical equipment visible — this is about the result and how it feels. '
            'Warm, uplifting, aspirational. Photorealistic, high quality.'
        ),
    },
    {
        'file': 'inline-3.png',
        'model': 'nano-banana-pro',
        'fallback': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A med spa consultation scene: a professional female practitioner sits across from a patient '
            'at an elegant consultation table. The practitioner holds an open laptop showing a digital '
            'marketing analytics dashboard with clean charts — website traffic, Google Ads performance, '
            'consultation booking rates. Both individuals look engaged and professional. '
            'Clean, modern medical spa office: white walls, warm lighting, tasteful decor. '
            'The mood is collaborative and strategic — a business planning meeting for a premium practice. '
            'Photorealistic, professional, premium aesthetics brand feel.'
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

        print(f'[GEN] {fname} (model={img["model"]}, size={img["size"]})...')

        img_bytes = None

        # Try primary model
        if img['model'] == 'nano-banana-pro':
            try:
                img_bytes = generate_image_gemini(img['prompt'])
                print(f'      ✅ Generated via Gemini/nano-banana-pro ({len(img_bytes)//1024} KB)')
            except Exception as e:
                print(f'      ⚠️  Gemini failed: {e}')
                img_bytes = None

        if img_bytes is None:
            # Use OpenAI (primary or fallback)
            primary_model = img['model'] if img['model'] != 'nano-banana-pro' else img['fallback']
            try:
                # Handle gpt-image-1.5 size — try 1536x1024 only for hero
                size = img['size']
                img_bytes = generate_image_openai(
                    img['prompt'],
                    model=primary_model,
                    quality=img['quality'],
                    size=size,
                )
                print(f'      ✅ Generated via {primary_model} ({len(img_bytes)//1024} KB)')
            except Exception as e:
                print(f'      ⚠️  {primary_model} failed: {e}')
                # Try gpt-image-1 as final fallback
                if primary_model != 'gpt-image-1':
                    fallback_size = '1024x1024' if size == '1536x1024' else size
                    try:
                        img_bytes = generate_image_openai(
                            img['prompt'],
                            model='gpt-image-1',
                            quality='medium',
                            size=fallback_size,
                        )
                        print(f'      ✅ Generated via gpt-image-1 fallback ({len(img_bytes)//1024} KB)')
                    except Exception as e2:
                        print(f'      ❌ All generation methods failed: {e2}')
                        continue

        # Save locally
        with open(local_path, 'wb') as f:
            f.write(img_bytes)
        print(f'      💾 Saved {local_path}')

        # Upload to Vercel Blob
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

    if len(results) == len(IMAGES):
        print('\n✅ All images generated and uploaded successfully!')
    else:
        print(f'\n⚠️  {len(IMAGES) - len(results)} image(s) failed.')
        sys.exit(1)


if __name__ == '__main__':
    main()
