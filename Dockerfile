# ──────────────────────────── Builder stage ──────────────────────────────── #
FROM python:3.12-slim AS builder

# SDL2 runtime libs needed by Pyxel’s CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Pyxel CLI
RUN pip install --no-cache-dir pyxel

# ── Build-time parameters (override with --build-arg) ─────────────────────── #
ARG APP_DIR=src
ARG STARTUP_SCRIPT=main.py
ARG APP_NAME=game
ARG OUTPUT_DIR=web

WORKDIR /workspace

# Copy sources and build the Web export
COPY src/ src/
RUN pyxel package "src" "src/main.py"      && \
    mv "src.pyxapp" "game.pyxapp"                    && \
    pyxel app2html "game.pyxapp"                            && \
    mkdir -p "web"                                       && \
    mv "game.html" "web/index.html"               && \
    touch "web/.nojekyll"

# ─────────────────────────── Runtime stage ───────────────────────────────── #
FROM nginx:stable-alpine

# Re-declare the ARG so we can use it for COPY
ARG OUTPUT_DIR=web

# Copy the static site produced above into Nginx’s default site dir
COPY --from=builder /workspace/web/ /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
