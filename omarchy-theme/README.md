# Omarchy Custom Boot Theme (Bode)

Identidade visual B0DE (logo + amarelo `#ffcc00` sobre preto `#000000`) no bootloader (Limine), na tela de boot/desbloqueio (Plymouth), na tela de login (SDDM) e no terminal (fastfetch) do Omarchy Quattro.

## Arquivos
- `apply_theme.sh`: aplica o tema de boot (logo e fundo preto no Plymouth/SDDM via `omarchy plymouth set`, fundo do console do Plymouth e cores no `/boot/limine.conf`) e regenera o initramfs.
- `bode-boot-theme.hook`: hook de `post-update` que reaplica o tema quando um `omarchy update` volta os arquivos do pacote `omarchy-settings` para o padrão. Só pede sudo se algo tiver sido sobrescrito.
- `logo-bode.png`: a logo usada no boot, no login e no terminal.

## Como instalar em uma máquina nova

1. Aplique o tema de boot (pede a senha de administrador):
   ```bash
   bash ~/codes/github/dotfiles/omarchy-theme/apply_theme.sh
   ```

2. Instale o hook para o tema sobreviver às atualizações:
   ```bash
   omarchy hook install post-update ~/codes/github/dotfiles/omarchy-theme/bode-boot-theme.hook
   ```

3. Reinicie a máquina para ver o novo boot.

> No Quattro os temas do Plymouth e do SDDM ficam em `/usr/share`, que pertence ao pacote `omarchy-settings`. Por isso o `apply_theme.sh` sozinho não basta: sem o hook, a próxima atualização desse pacote traz a logo do Omarchy de volta.

## Logo no terminal

- `omarchy/branding/about.png` (cópia da `logo-bode.png`) vai em `~/.config/omarchy/branding/about.png`; o `about.txt` (arte ASCII B0DE) é a logo que o fastfetch padrão do Omarchy usa fora do foot.
- `bash/ff-logo.sh` define `ff_logo`, que no foot mostra a logo em sixel empilhada na altura do fastfetch e escolhe a config (`fastfetch/compact*.jsonc`) que cabe na janela sem rolar. Veja o README principal para o trecho do `.bashrc`.
