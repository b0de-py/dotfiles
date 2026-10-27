-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
-- List current monitors and supported resolutions with: hyprctl monitors all

-- 1080p monitors, no HiDPI scaling.
hl.env("GDK_SCALE", "1")

hl.monitor({ output = "DP-1", mode = "1920x1080@180", position = "0x0", scale = 1, bitdepth = 10 })
hl.monitor({ output = "DP-2", mode = "1920x1080@74.99", position = "1920x0", scale = 1, bitdepth = 10 })

-- Fallback for any other monitor that gets plugged in.
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })
