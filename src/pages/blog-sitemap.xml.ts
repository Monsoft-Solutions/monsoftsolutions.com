/**
 * Blog Sitemap with Image Support
 *
 * Generates an XML sitemap specifically for blog posts with image extensions.
 * Follows Google's sitemap image extension specification:
 * https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps
 */

import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

const SITE_URL = "https://monsoftsolutions.com";

export const GET: APIRoute = async () => {
  // Get all published blog posts
  const posts = await getCollection("blog", ({ data }) => !data.draft);

  // Sort by date (newest first)
  posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  // Generate XML
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset 
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
>
  <!-- Blog Index Page -->
  <url>
    <loc>${SITE_URL}/blog</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- Blog Posts -->
${posts
  .map((post) => {
    const url = `${SITE_URL}/blog/${post.id}`;
    const lastmod = (post.data.updatedDate || post.data.pubDate)
      .toISOString()
      .split("T")[0];

    // Build image tag if heroImage exists
    const imageTag = post.data.heroImage
      ? `
    <image:image>
      <image:loc>${escapeXml(post.data.heroImage)}</image:loc>
      <image:title>${escapeXml(post.data.title)}</image:title>
      ${post.data.heroImageAlt ? `<image:caption>${escapeXml(post.data.heroImageAlt)}</image:caption>` : ""}
    </image:image>`
      : "";

    return `  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>${imageTag}
  </url>`;
  })
  .join("\n")}
</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "public, max-age=3600", // Cache for 1 hour
    },
  });
};

/**
 * Escape special XML characters
 */
function escapeXml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}
