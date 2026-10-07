# ai-usagebar

Uso do Claude (e do Google Antigravity) na Waybar, com o [ai-usagebar](https://github.com/akitaonrails/ai-usagebar).

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

3. A Waybar já vem pronta no `waybar/config.jsonc` deste repo: os módulos `custom/claude` e `custom/antigravity` ficam no começo do `modules-right`, e o `#custom-claude` está no `waybar/style.css`. Os dois usam `"signal": 13` e abrem o `ai-usagebar-tui` no clique.

   Se o repo privado de automações estiver instalado, o `group/habits` entra antes do `custom/claude`.

## Antigravity

Veja [antigravity-setup.md](antigravity-setup.md). Se o app do Antigravity não estiver aberto, o módulo dele fica sem dados.
