#!/usr/bin/env bash
# Instala o curiosidade-viral como skill do Claude Code (e do Codex) e testa o kit.
# Uso: bash instalar.sh
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
for d in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$d"
  if [ -e "$d/curiosidade-viral" ] && [ ! -L "$d/curiosidade-viral" ]; then echo "  · $d/curiosidade-viral já existe (não mexi)"; continue; fi
  ln -sfn "$AQUI" "$d/curiosidade-viral" && echo "  ✓ skill em $d/curiosidade-viral"
done
command -v node >/dev/null || { echo "Falta Node.js 22+ (https://nodejs.org)"; exit 1; }
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg"; exit 1; }
python3 -c "import numpy" 2>/dev/null || { echo "Falta numpy (música em código): sudo apt install python3-numpy  (Mac: python3 -m pip install numpy)"; exit 1; }
echo "Testando as ferramentas…"
( cd "$AQUI" && python3 -m unittest discover -s testes 2>&1 | tail -2 )
[ -f "$AQUI/preferencias.md" ] || { cp "$AQUI/preferencias.exemplo.md" "$AQUI/preferencias.md"; echo "  ✓ preferencias.md criado (edite o público e o fecho)"; }
echo
echo "Pronto. No Claude Code, dentro desta pasta: \"faz um reel de curiosidade: por que <a coisa> faz <X>?\""
