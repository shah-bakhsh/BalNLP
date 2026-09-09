# Vercel frontend and custom domain

Import shah-bakhsh/BalNLP with Root Directory frontend, framework Next.js, Node 24, npm ci and npm run build. Set NEXT_PUBLIC_API_URL to the actual Render API origin plus /api/v1. Leave BALNLP_STATIC_EXPORT unset for standard Vercel Next.js hosting. Set FRONTEND_URL on Render to the exact production frontend origin. No HF tokens belong in frontend environment variables.

Add the supplied custom domain in Vercel Project Settings > Domains. Use the DNS records Vercel reports for that specific domain; do not invent records before ownership and DNS are checked. Verify DNS and TLS, then update Render FRONTEND_URL to the chosen canonical HTTPS domain. A domain does not change backend memory capacity.


## Created deployment

Production alias: https://balnlp-shah-bakhshs-projects.vercel.app
Project: https://vercel.com/shah-bakhshs-projects/balnlp
Deployment: dpl_DNcxUUV16WzNzazYNTV6pjCPzMgm

This deployment was uploaded through the Vercel connector. Automatic GitHub linking is not verified. The connector's read/status tools currently cannot access the team, and the public alias redirects to Vercel login. Reconnect the appropriate team and configure public production access in Deployment Protection before publishing the domain.

The deployment uses NEXT_PUBLIC_API_URL=https://balnlp-api.onrender.com/api/v1. Render FRONTEND_URL matches the production alias. Public readiness and analysis currently return 503 RESOURCE_LIMITED, as expected for the free plan.
