-- Keep only your personal input overrides here. Uncommented settings below
-- replace Omarchy's defaults.

-- See https://wiki.hypr.land/Configuring/Basics/Variables/#input
hl.config({
  input = {
    -- US International (dead keys for accents), Caps Lock as compose.
    kb_layout = "us",
    kb_variant = "intl",
    kb_options = "compose:caps",

    -- Change speed of keyboard repeat.
    repeat_rate = 40,
    repeat_delay = 600,

    -- Start with numlock on by default.
    numlock_by_default = true,

    touchpad = {
      -- Control the speed of your scrolling.
      scroll_factor = 0.4,
    },
  },
})
