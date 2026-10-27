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

## Atualizando um PC do Omarchy 3 para o Quattro

O upgrade para o Quattro (4.x) troca muita coisa de lugar. Antes de começar, saiba o que ele faz com a config antiga:

| O que | O que acontece | Como volta |
|---|---|---|
| `~/.config/hypr/*.conf` | continuam lá, mas são ignorados (o Hyprland agora lê `*.lua`) | [Hyprland](#hyprland) |
| `~/.config/waybar/` | movida para `~/.config/waybar.omarchy-upgrade-to-quattro.<data>.bak` (a Waybar saiu) | [Barra](#barra-shell-do-omarchy); o `calendar_events.txt` vem do `.bak` |
| `~/.local/share/omarchy/` | movida para `.bak`; o Omarchy agora mora em `/usr/share/omarchy` | o `.bashrc` novo já aponta para lá |
| `~/.bashrc` | reescrito pelo padrão do Omarchy (backup em `~/.bashrc.omarchy-upgrade-to-quattro.<data>.bak`) | [`.bashrc`](#bashrc) |
| `~/.config/mimeapps.list` | navegador padrão volta para o Chromium | [Navegador padrão](#navegador-padrão-vivaldi) |
| `~/.config/xdg-terminals.list` | apagado (era o ghostty); o padrão vira o **foot** | nada: a logo em imagem do terminal só funciona no foot |
| `~/.config/walker`, `mako`, `swayosd` | movidos para `.bak`; o shell do Omarchy faz o papel deles | nada |
| tema de boot (Plymouth/SDDM/Limine) | volta para a logo do Omarchy | [omarchy-theme](omarchy-theme/README.md) |
| layout do teclado | o fcitx5 sobe com `us` sem acentos | [Teclado](#teclado-fcitx5) |

Os `.bak` ficam na máquina; nada é apagado. Na ordem:

1. `omarchy update` até chegar no Quattro e reinicie.
2. Atualize os repos: `git -C ~/codes/github/dotfiles pull` e `git -C ~/codes/github/automations pull`.
3. Instale os [pacotes](#pacotes).
4. Aplique cada seção de [Como aplicar](#como-aplicar-em-uma-nova-máquina), de cima para baixo.
5. Recupere os eventos do calendário, que não são versionados:

   ```bash
   cp ~/.config/waybar.omarchy-upgrade-to-quattro.*.bak/calendar_events.txt ~/.config/waybar/
   ```

6. Siga o README do [automations](https://github.com/b0de-py/automations) (repo privado) para a parte pessoal: atalhos do trabalho, clima de casa, hábitos e timers.
7. Reinicie para ver o boot e o login com a logo B0DE.

## Como aplicar em uma nova máquina

### Pré-requisitos

- [Omarchy](https://omarchy.org) Quattro instalado
- Repo clonado em `~/codes/github/dotfiles` (o `.bashrc` e o hook do boot usam esse caminho)

### Pacotes

```bash
omarchy pkg add vivaldi typora python-pytz
omarchy pkg aur add blesh-git
```

- `python-pytz`: timezone do calendário da barra. Não use `pip install pytz`: no Arch o pip do sistema é bloqueado, e os scripts rodam com o `/usr/bin/python3`.
- `blesh-git` (ble.sh 0.4): autocomplete do bash. O pacote `blesh` (0.3.4) é antigo para o bash 5.3 e de vez em quando solta `value too great for base` no terminal.
- `imagemagick` (empilha a logo no terminal) e `foot` já vêm no Omarchy.
- O `ai-usagebar` é instalado pelo [`ai-usagebar/install.sh`](ai-usagebar/README.md).

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

Quem chama a logo ao abrir o terminal é o `ff_logo`, no [`.bashrc`](#bashrc).

Para o boot, o login e o hook que mantém tudo depois dos updates, veja [omarchy-theme/README.md](omarchy-theme/README.md).

A logo em imagem (sixel) só aparece no **foot**, o terminal padrão do Quattro. Em outro terminal, o `ff_logo` mostra o fastfetch normal, com a arte ASCII do `about.txt`.

### `.bashrc`

O `.bashrc` não é versionado inteiro: os outros projetos (automations/ai-tools, r4ul-website, shoppee_orders...) acrescentam o próprio `source` no fim pelo `install.sh` de cada um, e os instaladores do cargo e do nvm também. A base fica assim:

```bash
# 0. Ambiente do Omarchy (OMARCHY_PATH + PATH), necessário até em shells não interativos
[[ -r /usr/share/omarchy/default/bash/env-bootstrap ]] && source /usr/share/omarchy/default/bash/env-bootstrap

# 1. Gatekeeper: Se não for interativo, não faz nada.
[[ $- != *i* ]] && return

# 2. ble.sh (autocomplete) carregado antes do rc do Omarchy, para o starship
#    detectar o ble e usar os hooks dele; o ble-attach fica no fim do arquivo.
if [ -f /usr/share/blesh/ble.sh ]; then
    source /usr/share/blesh/ble.sh --noattach

    # Silencia apenas as reclamações básicas para não sujar o terminal
    ble-bind -f 'emacs-editing-mode' 'nop' 2>/dev/null
    ble-bind -f 'vi-editing-mode' 'nop' 2>/dev/null
fi

# 3. Carrega as funções e o visual padrão do Omarchy (no Quattro mora em /usr/share/omarchy)
if [ -f "${OMARCHY_PATH:-/usr/share/omarchy}/default/bash/rc" ]; then
    source "${OMARCHY_PATH:-/usr/share/omarchy}/default/bash/rc"
fi

# fastfetch com a logo-bode.png (b0de-py/dotfiles/bash/ff-logo.sh)
if [[ -f ~/codes/github/dotfiles/bash/ff-logo.sh ]]; then
    source ~/codes/github/dotfiles/bash/ff-logo.sh && ff_logo
else
    fastfetch
fi

## Aliases

alias reload-bar='omarchy restart shell'

# ... linhas acrescentadas pelos install.sh dos outros projetos ...

# ble.sh: tem que ser a última coisa do .bashrc
[[ ${BLE_VERSION-} ]] && ble-attach
```

- O ble.sh tem que vir **antes** do rc do Omarchy: é o rc que inicializa o starship, e o starship só se conecta ao ble se ele já estiver carregado.
- Se um `install.sh` acrescentar algo depois do `ble-attach`, não tem problema: no ble.sh 0.4 o attach só acontece depois que o `.bashrc` termina. Mas o certo é manter o `ble-attach` como última linha.
- Num PC que veio do Omarchy 3, pegue os `source` dos projetos e as linhas do cargo e do nvm no `~/.bashrc.omarchy-upgrade-to-quattro.*.bak`. Não copie o `.bak` inteiro: ele aponta para o `~/.local/share/omarchy`, que não existe mais.

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
