# dotfiles

Configurações pessoais do meu desktop Linux com [Omarchy](https://omarchy.org) (Quattro) + Hyprland. O objetivo é conseguir replicar o setup em outra máquina sem dor de cabeça.

## Estrutura

```
dotfiles/
├── omarchy/
│   ├── hypr/                     # Config do Hyprland em Lua (vai em ~/.config/hypr/)
│   │   ├── bindings.lua          # Atalhos de teclado personalizados
│   │   ├── hyprland.lua          # Window rules (opacidade por app)
│   │   ├── input.lua             # Teclado (us intl) e touchpad
│   │   ├── looknfeel.lua         # Aparência geral (rounding)
│   │   └── monitors.lua          # Configuração dos monitores
│   ├── shell.json                # Layout da barra do shell do Omarchy
│   ├── shell.toml                # Overrides do shell (fonte da barra)
│   ├── bar/modules/              # Módulos QML da barra
│   │   ├── ai-usage.qml          # Claude + Antigravity (gaveta no hover)
│   │   └── colored-command.qml   # Comando com cor por classe (CPU, clima)
│   ├── plugins/fnzs.tray/        # Clone do tray com a setinha colada no Bluetooth
│   └── branding/                 # Logo B0DE (about.png/about.txt) e screensaver
├── omarchy-theme/                # Tema de boot B0DE (Limine/Plymouth/SDDM) + hook
├── bash/ff-logo.sh               # fastfetch com a logo em sixel ao abrir o terminal
├── fastfetch/                    # Configs compactas do fastfetch (janelas menores)
├── fcitx5/profile                # Layout de teclado us-intl no fcitx5
├── ai-usagebar/                  # Uso do Claude/Antigravity (config + install.sh)
└── waybar/                       # Scripts da barra (calendário, clima, CPU)
```

## Como aplicar em uma nova máquina

### Pré-requisitos

- [Omarchy](https://omarchy.org) Quattro instalado
- Dependências Python dos scripts da barra: `pip install pytz`
- `imagemagick` para empilhar a logo no terminal (já vem no Omarchy)

### Hyprland

```bash
cp omarchy/hypr/*.lua ~/.config/hypr/
```

O `bindings.lua` termina com `pcall(require, "hypr.private")`, que carrega `~/.config/hypr/private.lua` se ele existir. Lá ficam atalhos e window rules pessoais que não vão pra este repo (o repo privado de automações instala esse arquivo). Sem ele, nada quebra.

Depois de copiar, valide:

```bash
hyprctl reload && hyprctl configerrors
```

> **Atenção:** o `monitors.lua` tem a configuração específica deste desktop (DP-1 a 180Hz e DP-2 a 75Hz, ambos 1920x1080 com 10 bits). Ajuste conforme a saída de `hyprctl monitors` na nova máquina.

### Teclado (fcitx5)

```bash
cp fcitx5/profile ~/.config/fcitx5/profile
```

Sem isso o fcitx5 sobe com o layout `us` puro e os acentos (`'` + `a` = `á`) não funcionam, mesmo com o `input.lua` em `us intl`.

### Barra (shell do Omarchy)

```bash
mkdir -p ~/.config/omarchy/bar/modules ~/.config/omarchy/plugins ~/.config/waybar
cp omarchy/shell.json omarchy/shell.toml ~/.config/omarchy/
cp omarchy/bar/modules/*.qml ~/.config/omarchy/bar/modules/
cp -r omarchy/plugins/fnzs.tray ~/.config/omarchy/plugins/
cp waybar/* ~/.config/waybar/
omarchy restart shell
```

- Os scripts continuam em `~/.config/waybar/` (o nome ficou do tempo da Waybar), mas quem chama é o `shell.json`.
- O módulo `habit-tracker` aponta para `~/codes/github/automations/habit-tracker/bar/habits.qml` (repo privado). Sem ele, tire a entrada do `shell.json`.
- Para o `ai-usage`, veja [ai-usagebar/README.md](ai-usagebar/README.md).
- Depois de mexer em módulos QML, use `reload-bar` (alias de `omarchy restart shell`) ou `SUPER + CTRL + SHIFT + /`.

### Logo no terminal e tela de boot

```bash
mkdir -p ~/.config/omarchy/branding ~/.config/fastfetch
cp omarchy/branding/* ~/.config/omarchy/branding/
cp fastfetch/*.jsonc ~/.config/fastfetch/
```

O `~/.bashrc` do Quattro carrega o rc do Omarchy de `/usr/share/omarchy`. Troque a chamada do `fastfetch` pela da logo:

```bash
source "${OMARCHY_PATH:-/usr/share/omarchy}/default/bash/rc"

if [[ -f ~/codes/github/dotfiles/bash/ff-logo.sh ]]; then
    source ~/codes/github/dotfiles/bash/ff-logo.sh && ff_logo
else
    fastfetch
fi

alias reload-bar='omarchy restart shell'
```

Para o boot, o login e o hook que mantém tudo depois dos updates, veja [omarchy-theme/README.md](omarchy-theme/README.md).

### Navegador padrão (Vivaldi)

O upgrade para o Quattro volta o navegador padrão para o Chromium, e o `omarchy default browser` não lista o Vivaldi. Defina direto pelo XDG:

```bash
xdg-settings set default-web-browser vivaldi-stable.desktop
xdg-mime default vivaldi-stable.desktop x-scheme-handler/mailto
```

## Detalhes das customizações

### Atalhos (`bindings.lua`)

Principais diferenças em relação ao padrão do Omarchy:

| Atalho | Ação |
|---|---|
| `SUPER + A` | Abre o launcher de apps |
| `SUPER + Q` | Fecha a janela ativa |
| `SUPER + RETURN` | Terminal sempre no `~` |
| `SUPER + SHIFT + A` | Abre o Gemini como webapp |
| `SUPER + SHIFT + W` | Abre o Typora |
| `SUPER + B` | Painel de Bluetooth do shell |
| `SUPER + N` | Painel de áudio do shell |
| `SUPER + CTRL + SHIFT + /` | Reinicia o shell (barra) |

`SUPER + SPACE` (menu do Omarchy) e `SUPER + W` (fechar janela) ficam livres.

> Atalhos de webapps pessoais ficam no `~/.config/hypr/private.lua`, fora deste repo.

### Input (`input.lua`)

- Layout: `us` com variante `intl` (suporte a acentos) e `compose:caps`
- `repeat_rate = 40`, `repeat_delay = 600`
- NumLock ligado no boot
- Rolagem do touchpad mais lenta (`scroll_factor = 0.4`)

### Aparência (`looknfeel.lua`)

- Cantos arredondados: `rounding = 8`

### Hyprland (`hyprland.lua`)

Window rules de opacidade para evitar transparência indesejada:

- `vivaldi-stable`
- `teams-for-linux`
- webapp X (Twitter)

### Barra

| Lado | Módulos |
|---|---|
| Esquerda | workspaces, mídia |
| Centro | calendário, relógio (`HH:mm:ss`), clima (cor pela temperatura), updates, indicadores |
| Direita | hábitos, uso de IA, tray, Bluetooth, rede, áudio, CPU (cor pela carga/temperatura), monitor, energia |

Veja [waybar/README.md](waybar/README.md) para os scripts de calendário, clima e CPU.

### ai-usagebar

Uso do Claude e do Antigravity na barra. Veja [ai-usagebar/README.md](ai-usagebar/README.md) para instalar (`./ai-usagebar/install.sh`).
