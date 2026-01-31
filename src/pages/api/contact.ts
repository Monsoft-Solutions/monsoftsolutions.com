/**
 * Contact Form API Endpoint
 * 
 * Receives form submissions and forwards to n8n webhook.
 * The webhook URL is configured via N8N_WEBHOOK_URL environment variable.
 */

import type { APIRoute } from 'astro';

export const prerender = false; // This endpoint needs to be server-rendered

interface ContactFormData {
  name: string;
  email: string;
  company?: string;
  projectType: string;
  message: string;
  budget?: string;
}

export const POST: APIRoute = async ({ request }) => {
  try {
    // Get webhook URL from environment
    const webhookUrl = import.meta.env.N8N_WEBHOOK_URL;
    
    if (!webhookUrl) {
      console.error('N8N_WEBHOOK_URL not configured');
      return new Response(
        JSON.stringify({ 
          success: false, 
          error: 'Server configuration error' 
        }),
        { 
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    // Parse form data
    const formData = await request.formData();
    
    const data: ContactFormData = {
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      company: formData.get('company') as string || undefined,
      projectType: formData.get('project-type') as string,
      message: formData.get('message') as string,
      budget: formData.get('budget') as string || undefined,
    };

    // Validate required fields
    if (!data.name || !data.email || !data.projectType || !data.message) {
      return new Response(
        JSON.stringify({ 
          success: false, 
          error: 'Missing required fields' 
        }),
        { 
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    // Forward to n8n webhook
    const n8nResponse = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...data,
        submittedAt: new Date().toISOString(),
        source: 'monsoftsolutions.com',
      }),
    });

    if (!n8nResponse.ok) {
      console.error('n8n webhook failed:', n8nResponse.status, await n8nResponse.text());
      return new Response(
        JSON.stringify({ 
          success: false, 
          error: 'Failed to submit form' 
        }),
        { 
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    return new Response(
      JSON.stringify({ 
        success: true, 
        message: 'Form submitted successfully' 
      }),
      { 
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );

  } catch (error) {
    console.error('Contact form error:', error);
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: 'An unexpected error occurred' 
      }),
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};
