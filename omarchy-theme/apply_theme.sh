#!/bin/bash
set -Eeuo pipefail

# Pega o diretório exato de onde o script está sendo executado no seu dotfiles
SCRIPT_DIR=$(dirname "$(realpath "$0")")

LIMINE_CONF="$HOME/.local/share/omarchy/default/limine/limine.conf"

echo "Validando pré-requisitos..."
if [ ! -f "$LIMINE_CONF" ]; then
    echo "Erro: Arquivo $LIMINE_CONF não encontrado. Abortando." >&2
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/logo-bode.png" ]; then
    echo "Erro: Imagem $SCRIPT_DIR/logo-bode.png não encontrada. Abortando." >&2
    exit 1
fi

if [ ! -d "/usr/share/plymouth/themes/omarchy" ]; then
    echo "Erro: Diretório do tema Plymouth (/usr/share/plymouth/themes/omarchy) não encontrado. Abortando." >&2
    exit 1
fi

echo "Aplicando as novas cores do Limine (amarelo: ffcc00 e fundo preto: 000000)..."
sed -i 's/interface_branding_color:.*/interface_branding_color: ffcc00/' "$LIMINE_CONF"
sed -i 's/interface_help_color:.*/interface_help_color: ffcc00/' "$LIMINE_CONF"
sed -i 's/interface_help_color_bright:.*/interface_help_color_bright: ffcc00/' "$LIMINE_CONF"
sed -i 's/term_background:.*/term_background: 000000/' "$LIMINE_CONF"
sed -i 's/backdrop:.*/backdrop: 000000/' "$LIMINE_CONF"
sed -i 's/term_foreground:.*/term_foreground: ffcc00/' "$LIMINE_CONF"
sed -i 's/term_foreground_bright:.*/term_foreground_bright: ffcc00/' "$LIMINE_CONF"
sed -i 's/term_background_bright:.*/term_background_bright: 000000/' "$LIMINE_CONF"

# Cores da paleta do terminal (preto e amarelo para tela de senha LUKS)
sed -i 's/^term_palette:.*$/term_palette: 000000;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00/' "$LIMINE_CONF"
sed -i 's/^term_palette_bright:.*$/term_palette_bright: 000000;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00/' "$LIMINE_CONF"

echo "Enferrando configuração do Limine no boot (limine-enroll-config)..."
sudo limine-enroll-config

echo "Fazendo backup da imagem original e injetando a sua logo do repositório..."
if [ ! -f "/usr/share/plymouth/themes/omarchy/logo.png.bak" ]; then
    sudo cp /usr/share/plymouth/themes/omarchy/logo.png /usr/share/plymouth/themes/omarchy/logo.png.bak
fi

# Pega a imagem 'logo-bode.png' que está na mesma pasta que este script
sudo cp "$SCRIPT_DIR/logo-bode.png" /usr/share/plymouth/themes/omarchy/logo.png

echo "Atualizando as imagens de boot (initramfs)..."
sudo mkinitcpio -P

echo "Pronto! Bootloader e Plymouth personalizados aplicados com sucesso."
