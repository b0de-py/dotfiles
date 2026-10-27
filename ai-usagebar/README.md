# ai-usagebar

Uso do Claude (e do Google Antigravity) na barra do shell do Omarchy, com o [ai-usagebar](https://github.com/akitaonrails/ai-usagebar).

```
ai-usagebar/
├── config.toml             # Claude e Antigravity ligados, resto desligado
├── install.sh              # instala o pacote do AUR e copia a config
└── antigravity-setup.md    # como o Antigravity foi ligado
```

## Instalação em um PC novo

1. Faça login no Claude Code uma vez (o ai-usagebar lê o OAuth de `~/.claude/.credentials.json`, que se renova sozinho):

   ```bash
   claude
   ```

2. Instale o pacote e a config:

   ```bash
   ./ai-usagebar/install.sh
   ```

   Ele roda `yay -S --needed ai-usagebar-bin` se o `ai-usagebar` não estiver instalado e copia o `config.toml` para `~/.config/ai-usagebar/` (permissão 600). Se a config já existir, não é sobrescrita.

3. A barra já vem pronta no `omarchy/shell.json` deste repo: o módulo `ai-usage` (`omarchy/bar/modules/ai-usage.qml`, copiado para `~/.config/omarchy/bar/modules/`) fica antes do tray, no lado direito.

   - Fechado, mostra só o Claude (`‹ 󰚩 27% · 0h 12m`: uso da sessão e tempo até renovar).
   - Com o mouse em cima, a gaveta abre e mostra o Antigravity, empurrando o resto da barra para o lado.
   - Fica destacado quando o uso passa para `high`/`critical`; o clique abre o `ai-usagebar-tui`.
   - Atualiza a cada 300 s (`interval` no `shell.json`, mínimo de 30 s).

   Se o repo privado de automações estiver instalado, o `habit-tracker` entra antes do `ai-usage`.

## Antigravity

Veja [antigravity-setup.md](antigravity-setup.md). Se o app do Antigravity não estiver aberto, o módulo dele fica sem dados.
