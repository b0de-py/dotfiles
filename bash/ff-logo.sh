# Função ff_logo para o ~/.bashrc (b0de-py/dotfiles): fastfetch com a
# logo-bode.png em sixel. Carregue e chame no .bashrc:
#   source ~/codes/github/dotfiles/bash/ff-logo.sh && ff_logo
# Usa ~/.config/omarchy/branding/about.png e ~/.config/fastfetch/compact*.jsonc.

# fastfetch com a logo-bode.png (sixel), empilhada na altura das informações.
# Tudo é medido na hora de abrir: cabe inteiro na janela, sem precisar rolar.
ff_logo() {
    local logo=~/.config/omarchy/branding/about.png
    # O foot daqui usa TERM=xterm-256color, então detecta pelo processo pai.
    if [[ ! -f $logo || $(ps -o comm= -p $PPID) != foot ]]; then
        fastfetch
        return
    fi

    # O foot nasce em 80x24 e só depois o Hyprland redimensiona pro tile;
    # espera o tamanho final (até ~0,5 s) antes de medir.
    local size i
    for i in {1..25}; do
        size=$(stty size 2>/dev/null)
        [[ $size != "24 80" ]] && break
        sleep 0.02
    done
    local rows=${size% *} cols=${size#* }

    # Maior variação das informações que cabe com a linha do prompt
    # (linhas medidas com `fastfetch -c <config> --logo none --pipe | wc -l`).
    local config lines
    if (( rows >= 30 )); then
        config=/etc/fastfetch/config.jsonc lines=29
    elif (( rows >= 25 )); then
        config=~/.config/fastfetch/compact.jsonc lines=24
    elif (( rows >= 20 )); then
        config=~/.config/fastfetch/compact-noage.jsonc lines=19
    else
        return
    fi

    # Largura disponível pra logo: o que sobra depois das ~64 das informações.
    local avail=$(( cols - 64 ))
    (( avail > 48 )) && avail=48
    if (( avail < 16 )); then
        fastfetch -c "$config" --logo none
        return
    fi

    # Uma cópia ocupa ~0,23 linha por coluna (imagem 663x357, célula ~7x17 px).
    # Empilha cópias até cobrir a altura e estreita a logo pra caber nela.
    local copies=$(( (lines * 100 + avail * 23 - 1) / (avail * 23) ))
    local logo_cols=$(( lines * 100 / (copies * 23) ))
    (( logo_cols > avail )) && logo_cols=$avail
    local logo_rows=$(( copies * logo_cols * 23 / 100 ))

    local stack=${XDG_CACHE_HOME:-$HOME/.cache}/ff-logo/bode-x$copies.png
    if [[ ! -f $stack || $stack -ot $logo ]]; then
        local imgs=()
        for ((i = 0; i < copies; i++)); do imgs+=("$logo"); done
        mkdir -p "${stack%/*}"
        magick "${imgs[@]}" -append "$stack" 2>/dev/null || stack=$logo
    fi

    fastfetch -c "$config" --logo "$stack" --logo-type sixel --logo-width "$logo_cols" \
        --logo-padding-left 2 --logo-padding-right $(( avail - logo_cols + 3 )) \
        --logo-padding-top $(( (lines - logo_rows) / 2 ))
}
