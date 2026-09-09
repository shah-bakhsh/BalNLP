# Render first, Railway fallback

Status: DEPLOYMENT_READY_RESOURCE_LIMITED. This is not a verified public inference deployment.

The root render.yaml defines a free Docker API; the frontend is deployed on Vercel. Set NEXT_PUBLIC_API_URL to the API HTTPS URL plus /api/v1, and FRONTEND_URL to the frontend HTTPS origin. The backend binds 0.0.0.0 and reads PORT. No tokens are committed; public checkpoints download anonymously. HF_HOME controls cache location. Ephemeral hosts lose cached models after replacement. No disk or paid compute is provisioned.

GET /health reports process liveness. GET /ready returns 503 when the memory budget prevents loading, and 200 for an eligible idle lazy-loading service. Readiness does not claim successful inference. GET /api/v1/models reports structured configured/loaded/disabled/resource_limited/blocked status. GET /api/v1/diagnostics reports process RSS, peak RSS, configured/cgroup limit, and memory mode.

Render Free has 512 MB RAM. Railway Free has 0.5 GB RAM and its Trial has 1 GB (provider documentation checked September 8, 2026). The published approximately 1.1 GB checkpoints cannot run safely within these budgets, even one at a time. The conservative loading guard requires at least 2048 MiB of declared/container budget; this is a safety floor, not a guarantee that all inputs fit. See memory-pos.json for a real local measurement. Do not lower this guard to make a health-only deployment appear to support inference.

Sources: https://render.com/docs/compute-plans and https://docs.railway.com/pricing/plans

## Portable Docker and Railway

Use backend/Dockerfile with repository-root build context. Railway configuration is in railway.json. Keep BALNLP_MEMORY_MODE=low, BALNLP_WARMUP=false, ENABLE_MORPH=false, and one worker. Set FRONTEND_URL and HF_HOME through the provider. Linux container memory limits are automatically detected. No architecture change is needed between providers. Do not enable paid resources without explicit owner approval.

## Capacity verification

Run python -m scripts.memory_probe --task pos on an adequately sized host. It records before load, after load, after real Balochi inference, and after unload. Test other checkpoints sequentially only after checking available memory. Then start the API, call /health, /ready and /api/v1/models, submit a real request, and verify the public frontend, JSON and CoNLL-U exports. Model loading is lazy by default. Low mode unloads each model after inference. Balanced/performance modes retain weights and require separate memory testing.

BalMorph now uses the recovered verified notebook adapter and is enabled by default. All four models passed real local API inference. Free-host memory limits still apply; this does not imply public deployment.

The optional combined static-site Docker example remains under deploy/huggingface for portability only; Render/Railway are the selected targets. Docker image build requires a running daemon. A selected application source license is still needed before labeling the repository open source.


## Live hosting attempt

Source publication succeeded. Render service srv-dagf47e7bikc73atl9eg is live on the free plan. The connected Render creation tool uses native Python, with the same CPU dependency installation and Uvicorn command as the portable Dockerfile. Docker remains the reproducible Blueprint/Railway path.

Verified public /health and /api/v1/models (200), /ready (503), and a real POST /api/v1/analyze (503 RESOURCE_LIMITED). CORS matches the Vercel production alias. The process remained healthy; it did not attempt an oversized model load.

The Vercel deployment exists but currently requires Vercel login, and its connector cannot access the project team. Public frontend verification remains blocked on team/protection settings. No domain has been supplied yet.
