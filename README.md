# dotfiles

Configurações pessoais do meu desktop Linux com [Omarchy](https://omarchy.org) + Hyprland. O objetivo é conseguir replicar o setup em outra máquina sem dor de cabeça.

## Estrutura

```
dotfiles/
├── omarchy/
│   ├── branding/
│   │   └── screensaver.txt       # Arte ASCII do screensaver (substitui o logo padrão do Omarchy)
│   └── hypr/
│       ├── bindings.conf         # Atalhos de teclado personalizados
│       ├── hyprland.conf         # Window rules (opacidade por app)
│       ├── hyprlock.conf         # Tela de bloqueio (fonte Fantasque Sans Mono)
│       ├── input.conf            # Teclado (us intl) e touchpad
│       ├── looknfeel.conf        # Aparência geral (rounding, gaps)
│       └── monitors.conf         # Configuração dos monitores
└── waybar/
    ├── config.jsonc              # Configuração da barra
    ├── style.css                 # Estilo da barra
    ├── way_calendar.py           # Widget de calendário com eventos
    ├── weather.py                # Widget de clima com cache
    ├── mediaplayer.py            # Widget de media player
    ├── cpu-detailed.py           # Monitor de CPU por core + consumo
    └── waybar_logging.py         # Sistema de logging compartilhado
```

## Como aplicar em uma nova máquina

### Pré-requisitos

- [Omarchy](https://omarchy.org) instalado
- Dependências Python para o waybar: `pip install pytz`
- `playerctl` para o widget de media: `sudo pacman -S playerctl`

### Omarchy / Hyprland

Copie os arquivos de `omarchy/hypr/` para `~/.config/hypr/`:

```bash
cp omarchy/hypr/*.conf ~/.config/hypr/
```

Copie o screensaver para `~/.config/omarchy/branding/`:

```bash
cp omarchy/branding/screensaver.txt ~/.config/omarchy/branding/screensaver.txt
```

> **Atenção:** o `monitors.conf` tem a configuração específica deste desktop (dois monitores DP-1/DP-2 a 180Hz e 75Hz). Ajuste conforme a saída de `hyprctl monitors` na nova máquina.

### Waybar

Copie os arquivos de `waybar/` para `~/.config/waybar/`:

```bash
cp waybar/* ~/.config/waybar/
```

Reinicie o waybar:

```bash
pkill waybar && waybar &
```

## Detalhes das customizações

### Atalhos (`bindings.conf`)

Principais diferenças em relação ao padrão do Omarchy:

| Atalho | Ação |
|---|---|
| `SUPER + A` | Abre o Walker (launcher de apps) |
| `SUPER + Q` | Fecha a janela ativa |
| `SUPER + SHIFT + A` | Abre Gemini no navegador |
| `SUPER + SHIFT + V` | Abre EVDI (BB) no navegador |
| `SUPER + B` | Abre configurações de Bluetooth |
| `SUPER + N` | Abre mixer de áudio |
| `SUPER + ALT + RETURN` | Abre novo terminal com tmux |

### Input (`input.conf`)

- Layout: `us` com variante `intl` (suporte a acentos)
- `repeat_delay = 600` (delay antes de repetição de tecla)
- Clickfinger do touchpad desabilitado

### Aparência (`looknfeel.conf`)

- Cantos arredondados: `rounding = 8`

### Hyprland (`hyprland.conf`)

Window rules de opacidade para evitar transparência indesejada:

- `vivaldi-stable`
- `teams-for-linux`
- webapp EVDI (BB)
- webapp X (Twitter)

### Tela de bloqueio (`hyprlock.conf`)

- Fonte: `Fantasque Sans Mono`

### Waybar

Veja [waybar/README.md](waybar/README.md) para documentação detalhada dos widgets.
