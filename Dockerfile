# =============================================================================
# Dockerfile for monsoftsolutions.com (Static Astro Site)
# Optimized for Dokploy deployment
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Dependencies
# Cache npm dependencies separately for faster rebuilds
# -----------------------------------------------------------------------------
FROM node:22-alpine AS deps

WORKDIR /app

# Copy only package files for dependency caching
COPY package.json package-lock.json* ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# -----------------------------------------------------------------------------
# Stage 2: Build
# Build the static site
# -----------------------------------------------------------------------------
FROM node:22-alpine AS build

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source files
COPY . .

# Build the static site
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 3: Production
# Serve with NGINX (lightweight, fast, secure)
# -----------------------------------------------------------------------------
FROM nginx:alpine AS runtime

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy built static files
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 (Dokploy expects this for static sites)
EXPOSE 80

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
