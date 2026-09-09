# Vercel frontend and custom domain

Import shah-bakhsh/BalNLP with Root Directory frontend, framework Next.js, Node 24, npm ci and npm run build. Set NEXT_PUBLIC_API_URL to the actual Render API origin plus /api/v1. Leave BALNLP_STATIC_EXPORT unset for standard Vercel Next.js hosting. Set FRONTEND_URL on Render to the exact production frontend origin. No HF tokens belong in frontend environment variables.

Add the supplied custom domain in Vercel Project Settings > Domains. Use the DNS records Vercel reports for that specific domain; do not invent records before ownership and DNS are checked. Verify DNS and TLS, then update Render FRONTEND_URL to the chosen canonical HTTPS domain. A domain does not change backend memory capacity.
