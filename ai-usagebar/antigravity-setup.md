# Configuração do Antigravity no ai-usagebar e Waybar

Este documento registra os passos tomados para habilitar o rastreamento de uso do Google Antigravity na barra de status (Waybar), utilizando o `ai-usagebar`.

## 1. Habilitando o provedor no ai-usagebar

O `ai-usagebar` suporta o Antigravity nativamente e consegue ler o uso a partir do servidor local do Antigravity ou da sessão salva do Google.

Edite o arquivo de configuração principal:
`~/.config/ai-usagebar/config.toml`

E adicione o seguinte bloco ao final do arquivo:

```toml
[antigravity]
# Habilitado para mostrar a quota do Google Antigravity.
# O ai-usagebar detectará automaticamente o servidor local do Antigravity.
enabled = true
```

## 2. Adicionando o módulo individual na Waybar

Por padrão, a sua Waybar (`~/.config/waybar/config.jsonc`) estava configurada com um módulo customizado para mostrar **apenas** o uso do Claude (`--vendor anthropic`).

Para mostrar o Antigravity de forma independente, criamos um novo módulo customizado. 

Adicione a definição do módulo em `~/.config/waybar/config.jsonc`:

```json
  "custom/antigravity": {
    "exec": "ai-usagebar --vendor antigravity --icon '󰘧' --format '{session_pct}% · {session_reset}'",
    "return-type": "json",
    "interval": 300,
    "signal": 13,
    "tooltip": true,
    "on-click": "ai-usagebar-tui"
  },
```

E não se esqueça de adicioná-lo à lista de módulos da sua barra (ex: `modules-right`):

```json
  "modules-right": [
    "group/habits",
    "custom/claude",
    "custom/antigravity", // <-- Novo módulo
    "group/tray-expander",
    // ...
  ]
```

## 3. Recarregando a Waybar

Após salvar o arquivo, recarregue as configurações da Waybar para aplicar as mudanças imediatamente:

```bash
killall -SIGUSR2 waybar
```

## Notas sobre quotas do Antigravity

A quota do Antigravity é dividida em famílias de modelos:
- **Gemini**
- **Claude & GPT OSS**

O retorno padrão do módulo na barra será algo como `󰘧 4% · 1%` e o tooltip (ao passar o mouse por cima) mostrará os limites separados por família de modelo. Se estiver marcando 0% em alguma categoria (por exemplo "Claude & GPT OSS" no Antigravity), significa que você ainda não usou modelos daquela família *especificamente através do Antigravity* no ciclo atual. O uso feito diretamente pelo Claude Desktop/Code contabilizará no módulo do Claude.
