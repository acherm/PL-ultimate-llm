meta:
  id: gif_header
  file-extension: gif
  endian: le
seq:
  - id: magic
    contents: 'GIF'
  - id: version
    type: str
    size: 3
    encoding: ASCII
  - id: screen_width
    type: u2
  - id: screen_height
    type: u2
  - id: flags
    type: u1
  - id: bg_color_index
    type: u1
  - id: pixel_aspect_ratio
    type: u1
