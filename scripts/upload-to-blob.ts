/**
 * Upload images to Vercel Blob
 *
 * Usage:
 *   npx tsx scripts/upload-to-blob.ts                    # Upload all images
 *   npx tsx scripts/upload-to-blob.ts --blog             # Upload blog images only
 *   npx tsx scripts/upload-to-blob.ts --path ./public    # Upload from specific path
 *
 * Requires: BLOB_READ_WRITE_TOKEN environment variable
 */

import { put } from '@vercel/blob';
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, extname, relative } from 'path';

const BLOB_TOKEN = process.env.BLOB_READ_WRITE_TOKEN;

if (!BLOB_TOKEN) {
  console.error('❌ Missing BLOB_READ_WRITE_TOKEN environment variable');
  process.exit(1);
}

interface UploadResult {
  localPath: string;
  blobPath: string;
  url: string;
}

const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.ico'];

function isImage(filename: string): boolean {
  return IMAGE_EXTENSIONS.includes(extname(filename).toLowerCase());
}

function getAllImages(dir: string, basePath: string = dir): string[] {
  const files: string[] = [];

  try {
    const entries = readdirSync(dir);

    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip node_modules, dist, .git
        if (!['node_modules', 'dist', '.git', '.astro'].includes(entry)) {
          files.push(...getAllImages(fullPath, basePath));
        }
      } else if (isImage(entry)) {
        files.push(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error);
  }

  return files;
}

function getBlobPath(localPath: string, projectRoot: string): string {
  const relativePath = relative(projectRoot, localPath);

  // Blog images: src/data/blog/{post-slug}/images/{file} → blog/{post-slug}/{file}
  const blogMatch = relativePath.match(/src\/data\/blog\/([^/]+)\/images\/(.+)/);
  if (blogMatch) {
    return `blog/${blogMatch[1]}/${blogMatch[2]}`;
  }

  // Public images: public/images/{category}/{file} → {category}/{file}
  const publicMatch = relativePath.match(/public\/images\/(.+)/);
  if (publicMatch) {
    return publicMatch[1];
  }

  // Public root: public/{file} → assets/{file}
  const publicRootMatch = relativePath.match(/public\/(.+)/);
  if (publicRootMatch) {
    return `assets/${publicRootMatch[1]}`;
  }

  // Fallback: use relative path
  return relativePath.replace(/^src\//, '');
}

async function uploadImage(localPath: string, blobPath: string): Promise<UploadResult> {
  const fileBuffer = readFileSync(localPath);
  const contentType = getContentType(localPath);

  const blob = await put(blobPath, fileBuffer, {
    access: 'public',
    contentType,
    token: BLOB_TOKEN,
  });

  return {
    localPath,
    blobPath,
    url: blob.url,
  };
}

function getContentType(filename: string): string {
  const ext = extname(filename).toLowerCase();
  const types: Record<string, string> = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
  };
  return types[ext] || 'application/octet-stream';
}

async function main() {
  const args = process.argv.slice(2);
  const projectRoot = process.cwd();

  let searchPaths: string[] = [];

  if (args.includes('--blog')) {
    searchPaths = [join(projectRoot, 'src/data/blog')];
  } else if (args.includes('--path')) {
    const pathIndex = args.indexOf('--path');
    if (args[pathIndex + 1]) {
      searchPaths = [join(projectRoot, args[pathIndex + 1])];
    }
  } else {
    // Default: all images
    searchPaths = [join(projectRoot, 'public'), join(projectRoot, 'src/data/blog')];
  }

  console.log('🔍 Scanning for images...\n');

  const allImages: string[] = [];
  for (const searchPath of searchPaths) {
    allImages.push(...getAllImages(searchPath));
  }

  console.log(`📁 Found ${allImages.length} images\n`);

  const results: UploadResult[] = [];
  const errors: { path: string; error: string }[] = [];

  for (let i = 0; i < allImages.length; i++) {
    const localPath = allImages[i];
    const blobPath = getBlobPath(localPath, projectRoot);

    process.stdout.write(`[${i + 1}/${allImages.length}] Uploading ${blobPath}...`);

    try {
      const result = await uploadImage(localPath, blobPath);
      results.push(result);
      console.log(' ✅');
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      errors.push({ path: localPath, error: errorMsg });
      console.log(` ❌ ${errorMsg}`);
    }
  }

  // Write manifest
  const manifest: Record<string, string> = {};
  for (const result of results) {
    manifest[result.blobPath] = result.url;
  }

  const manifestPath = join(projectRoot, 'blob-manifest.json');
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log('\n' + '='.repeat(60));
  console.log(`✅ Uploaded: ${results.length}`);
  console.log(`❌ Errors: ${errors.length}`);
  console.log(`📄 Manifest: ${manifestPath}`);
  console.log('='.repeat(60) + '\n');

  // Print URL mapping for easy reference
  console.log('📋 URL Mapping:\n');
  for (const result of results) {
    console.log(`${result.blobPath}`);
    console.log(`  → ${result.url}\n`);
  }

  if (errors.length > 0) {
    console.log('\n⚠️  Errors:');
    for (const err of errors) {
      console.log(`  ${err.path}: ${err.error}`);
    }
  }
}

main().catch(console.error);
