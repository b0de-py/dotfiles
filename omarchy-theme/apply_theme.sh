#!/bin/bash
set -Eeuo pipefail

# Aplica o tema de boot B0DE no Omarchy Quattro: logo e fundo preto no Plymouth
# (boot/desbloqueio) e no SDDM (login), e cores amarelo/preto no Limine.
# Rode como seu usuário; ele pede sudo onde precisa.

SCRIPT_DIR=$(dirname "$(realpath "$0")")
LOGO=$SCRIPT_DIR/logo-bode.png
LIMINE_CONF=/boot/limine.conf
THEME=/usr/share/plymouth/themes/omarchy
# Mesma referência usada pelo bode-boot-theme.hook para saber se o tema foi sobrescrito.
APPLIED=${XDG_STATE_HOME:-$HOME/.local/state}/bode-boot-theme/logo.png

echo "Validando pré-requisitos..."
for file in "$LOGO" "$LIMINE_CONF" "$THEME/omarchy.plymouth"; do
    if ! sudo test -f "$file"; then
        echo "Erro: $file não encontrado. Abortando." >&2
        exit 1
    fi
done

echo "Aplicando logo e fundo preto no Plymouth e no SDDM..."
omarchy-plymouth-set 000000 ffcc00 "$LOGO"
install -D -m 644 "$THEME/logo.png" "$APPLIED"

# Fundo das mensagens de texto do boot (Esc no Plymouth); o omarchy-plymouth-set não mexe nele.
sudo sed -i 's/^ConsoleLogBackgroundColor=.*/ConsoleLogBackgroundColor=0x000000/' "$THEME/omarchy.plymouth"

echo "Aplicando as cores do Limine (amarelo: ffcc00 e fundo preto: 000000)..."
sudo sed -i -E \
    -e 's/^(interface_branding_color|interface_help_color|interface_help_color_bright|term_foreground|term_foreground_bright):.*/\1: ffcc00/' \
    -e 's/^(term_background|term_background_bright|backdrop):.*/\1: 000000/' \
    -e 's/^(term_palette|term_palette_bright):.*/\1: 000000;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00;ffcc00/' \
    "$LIMINE_CONF"

echo "Registrando a configuração do Limine (limine-enroll-config)..."
sudo limine-enroll-config

echo "Atualizando as imagens de boot (initramfs)..."
if command -v limine-mkinitcpio >/dev/null; then
    sudo limine-mkinitcpio
else
    sudo mkinitcpio -P
fi

echo "Pronto! Reinicie para ver o novo boot."
echo "Para reaplicar sozinho depois de cada 'omarchy update':"
echo "  omarchy hook install post-update $SCRIPT_DIR/bode-boot-theme.hook"
