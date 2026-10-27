-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- See current bindings and descriptions:
--   omarchy menu keybindings --print

-- Applications that differ from Omarchy's defaults.
hl.unbind("SUPER + RETURN") -- was: Terminal in the focused terminal's directory
o.bind("SUPER + RETURN", "Terminal", { launch = "xdg-terminal-exec --dir=" .. os.getenv("HOME") })
hl.unbind("SUPER + SHIFT + W") -- was: Omawrite
o.bind("SUPER + SHIFT + W", "Typora", { launch = "typora --enable-wayland-ime" })

-- Web apps
hl.unbind("SUPER + SHIFT + A") -- was: ChatGPT
o.bind("SUPER + SHIFT + A", "Gemini", { webapp = "https://gemini.google.com" })

-- Misc: open the shell's Bluetooth/Audio panels (replace bluetui/wiremix).
o.bind("SUPER + B", "Bluetooth", "omarchy-shell shell toggle omarchy.bluetooth")
o.bind("SUPER + N", "Audio", "omarchy-shell shell toggle omarchy.audio")

-- Launcher on SUPER + A, close window on SUPER + Q.
hl.unbind("SUPER + SPACE") -- was: Omarchy menu
hl.unbind("SUPER + W") -- was: Close window
o.bind("SUPER + A", "Launch apps", "omarchy-menu toggle apps")
o.bind("SUPER + Q", "Close window", hl.dsp.window.close())

-- Restart the Omarchy shell (bar, notifications, menus) after editing bar modules.
o.bind("SUPER + CTRL + SHIFT + SLASH", "Restart shell", "omarchy restart shell")

-- Machine-specific/private bindings (not versioned), see dotfiles-private.
pcall(require, "hypr.private")
