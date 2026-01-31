// @ts-check
import { defineConfig, envField } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://monsoftsolutions.com',
  env: {
    schema: {
      // n8n webhook URL for contact form - public and client-accessible
      N8N_WEBHOOK_URL: envField.string({
        context: 'client',
        access: 'public',
        optional: false,
      }),
    },
  },
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
          item.changefreq = 'daily';
        }
        // Services pages get high priority
        if (item.url.includes('/services')) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        }
        // About and contact
        if (item.url.includes('/about') || item.url.includes('/contact')) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
    server: {
      allowedHosts: ['localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok.io']
    }
  }
});
