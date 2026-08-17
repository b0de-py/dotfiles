# Omarchy Custom Boot Theme (Bode)

Este diretório contém os arquivos necessários para aplicar a identidade visual customizada (cores e logo) no bootloader (Limine) e na tela de decodificação (Plymouth) do Omarchy Linux.

## Arquivos
- `apply_theme.sh`: Script que injeta as novas cores hexadecimais no Limine e substitui a logo original do Plymouth.
- `logo-bode.png`: A imagem da logo que será utilizada na tela de boot.

## Como instalar em uma máquina nova

1. Dê permissão de execução para o script (necessário apenas na primeira vez após o clone):
   ```bash
   chmod +x apply_theme.sh
   ```

2. Execute o script (ele pedirá sua senha de administrador):
   ```bash
   bash apply_theme.sh
   ```

3. O script irá automaticamente:
   - Fazer o backup da logo antiga do Omarchy.
   - Substituir pela logo `logo-bode.png` (presente nesta mesma pasta).
   - Aplicar a paleta de cores (Amarelo `#ffcc00` e Fundo Preto `#000000`) no `/boot/limine.conf`.
   - Atualizar a imagem initramfs do Kernel (`mkinitcpio -P`).

4. Reinicie a máquina para visualizar a nova tela de boot.
