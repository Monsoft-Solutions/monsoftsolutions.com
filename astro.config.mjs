// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://monsoftsolutions.com',
  integrations: [
    sitemap({
      // Crawl frequency hints for search engines
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      // Customize priority per page
      serialize(item) {
        // Homepage gets highest priority
        if (item.url === 'https://monsoftsolutions.com/') {
          item.priority = 1.0;
          // @ts-expect-error - changefreq accepts string literals
          item.changefreq = 'daily';
        }
        // Services pages get high priority
        if (item.url.includes('/services')) {
          item.priority = 0.9;
          // @ts-expect-error - changefreq accepts string literals
          item.changefreq = 'weekly';
        }
        // About and contact
        if (item.url.includes('/about') || item.url.includes('/contact')) {
          item.priority = 0.8;
          // @ts-expect-error - changefreq accepts string literals
          item.changefreq = 'monthly';
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
    server: {
      allowedHosts: ['localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok.io'],
    },
  },
});
