# dotfiles

Configurações pessoais do meu desktop Linux com [Omarchy](https://omarchy.org) + Hyprland. O objetivo é conseguir replicar o setup em outra máquina sem dor de cabeça.

## Estrutura

```
dotfiles/
├── omarchy/
│   ├── branding/
│   │   └── screensaver.txt       # Arte ASCII do screensaver (substitui o logo padrão do Omarchy)
│   └── hypr/
│       ├── autostart.conf        # Apps iniciados no login (exec-once)
│       ├── bindings.conf         # Atalhos de teclado personalizados
│       ├── hyprland.conf         # Window rules (opacidade por app)
│       ├── hyprlock.conf         # Tela de bloqueio (fonte Fantasque Sans Mono)
│       ├── input.conf            # Teclado (us intl) e touchpad
│       ├── looknfeel.conf        # Aparência geral (rounding, gaps)
│       └── monitors.conf         # Configuração dos monitores
├── ai-usagebar/               # Uso do Claude/Antigravity na Waybar (config + install.sh)
├── vscode/
│   ├── settings.json             # Settings do usuário do VS Code (YAML, Error Lens, tema)
│   └── extensions.txt            # Extensões instaladas
├── yamllint/
│   └── config                    # Config global do yamllint (~/.config/yamllint/config)
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
touch ~/.config/hypr/private.conf
```

O `hyprland.conf` carrega `~/.config/hypr/private.conf`, onde ficam atalhos e window rules pessoais que não vão pra este repo. O `touch` só garante que o arquivo exista (não apaga um que já esteja lá).

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

### VS Code + YAML

Pré-requisito: `yamllint` instalado (`yay -S yamllint` ou `pip install yamllint`).

```bash
xargs -L1 code --install-extension < vscode/extensions.txt
cp vscode/settings.json ~/.config/Code/User/settings.json
mkdir -p ~/.config/yamllint && cp yamllint/config ~/.config/yamllint/config
```

## Detalhes das customizações

### Atalhos (`bindings.conf`)

Principais diferenças em relação ao padrão do Omarchy:

| Atalho | Ação |
|---|---|
| `SUPER + A` | Abre o Walker (launcher de apps) |
| `SUPER + Q` | Fecha a janela ativa |
| `SUPER + SHIFT + A` | Abre Gemini no navegador |
| `SUPER + B` | Abre configurações de Bluetooth |
| `SUPER + N` | Abre mixer de áudio |
| `SUPER + ALT + RETURN` | Abre novo terminal com tmux |

> Atalhos de webapps pessoais (e-mail, calendário, mensageiro, trabalho) ficam no `~/.config/hypr/private.conf`, fora deste repo.

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
- webapp X (Twitter)

### Tela de bloqueio (`hyprlock.conf`)

- Fonte: `Fantasque Sans Mono`

### Waybar

Veja [waybar/README.md](waybar/README.md) para documentação detalhada dos widgets.

### ai-usagebar

Uso do Claude e do Antigravity na Waybar. Veja [ai-usagebar/README.md](ai-usagebar/README.md) para instalar (`./ai-usagebar/install.sh`).

### VS Code + YAML

Cada peça tem um papel:

| Peça | Papel |
|---|---|
| **Error Lens** (`usernamehw.errorlens`) | Só exibe os diagnósticos inline no código (erro em vermelho, warning em amarelo) |
| **YAML** (`redhat.vscode-yaml`) | Valida sintaxe/schema e formata o arquivo ao salvar |
| **Linter** (`fnando.linter`) | Roda o `yamllint` enquanto você digita |
| **yamllint** (CLI) | Regras de estilo. Usa o `.yamllint` do projeto ou, se não houver, `~/.config/yamllint/config` |

Config global do yamllint (`yamllint/config`), compatível com o ansible-lint:

- `line-length`: máximo 120, como **warning**
- `truthy` (`yes`/`no` em vez de `true`/`false`): **warning**
- `document-start` (`---` no topo) desligado

Ao salvar um YAML, o VS Code formata o recuo, adiciona a linha final e remove espaços sobrando. YAML **inválido** (ex.: item de lista com recuo errado) não é formatado: o erro aparece em vermelho e precisa ser corrigido na mão. Para salvar sem formatar: `Ctrl+K Ctrl+Shift+S`.

> A extensão `yamllint-fix` foi substituída pela `Linter` porque só roda se existir um `.yamllint` na raiz do projeto.
