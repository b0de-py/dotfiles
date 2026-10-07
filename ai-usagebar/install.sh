#!/usr/bin/env bash
# Instala o ai-usagebar (AUR) e a config desta pasta. Não sobrescreve uma config existente.
set -euo pipefail

HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd)
CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}/ai-usagebar

if ! command -v ai-usagebar >/dev/null; then
    yay -S --needed ai-usagebar-bin
fi

mkdir -p "$CONFIG_DIR"
if [ -f "$CONFIG_DIR/config.toml" ]; then
    echo "Já existe $CONFIG_DIR/config.toml; não mexi. Compare com $HERE/config.toml se quiser atualizar."
else
    install -m 600 "$HERE/config.toml" "$CONFIG_DIR/config.toml"
    echo "Config instalada em $CONFIG_DIR/config.toml"
fi

if [ ! -f "$HOME/.claude/.credentials.json" ]; then
    echo "Aviso: login do Claude Code não encontrado. Rode 'claude' e faça login para o módulo do Claude funcionar."
fi
