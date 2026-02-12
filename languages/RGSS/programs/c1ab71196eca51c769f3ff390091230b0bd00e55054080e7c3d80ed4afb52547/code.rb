class Window_Custom < Window_Base
  def initialize
    super(0, 0, 320, 128)
    self.contents = Bitmap.new(width - 32, height - 32)
    self.contents.font.color = system_color
    self.contents.draw_text(4, 0, 200, 32, "Hello, RPG Maker!")
  end

  def refresh
    self.contents.clear
    self.contents.font.color = normal_color
    self.contents.draw_text(4, 32, 200, 32, "Gold: #{$game_party.gold}")
  end
end
