---
title: BalNLP
emoji: 🌿
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# BalNLP

A Balochi language workspace using Shah Bakhsh's BalPOS, BalNER v2 and BalParser checkpoints. BalMorph v2 awaits its matching original inference definition; unavailable morphology is explicitly reported.

This Docker Space serves the prebuilt website and FastAPI together. It needs at least 16 GB RAM for a comfortable deployment budget. Models load on demand and are released after each analysis. Startup time depends on the model download and hosting service.

Set `FRONTEND_URL` to the Space's actual HTTPS origin. No database is used and submitted text is not persistently stored. The service accepts one analysis at a time. Model predictions are research outputs and may contain errors.
