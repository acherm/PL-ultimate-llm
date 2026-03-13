-- HUD painting example in GLua (Garry's Mod Lua)
-- Displays player health and armor on screen

hook.Add("HUDPaint", "DrawHealthHUD", function()
    local ply = LocalPlayer()
    if not IsValid(ply) then return end

    local hp  = ply:Health()
    local arm = ply:Armor()

    -- Background panel
    draw.RoundedBox(4, 10, 10, 200, 30, Color(0, 0, 0, 150))
    draw.RoundedBox(4, 10, 46, 200, 30, Color(0, 0, 0, 150))

    -- Health bar
    local hpWidth = math.Clamp(hp, 0, 100) * 2
    draw.RoundedBox(4, 10, 10, hpWidth, 30, Color(200, 50, 50, 200))
    draw.SimpleText("HP: " .. hp, "DermaDefaultBold", 20, 25,
        Color(255, 255, 255), TEXT_ALIGN_LEFT, TEXT_ALIGN_CENTER)

    -- Armor bar
    local arWidth = math.Clamp(arm, 0, 100) * 2
    draw.RoundedBox(4, 10, 46, arWidth, 30, Color(50, 100, 200, 200))
    draw.SimpleText("AR: " .. arm, "DermaDefaultBold", 20, 61,
        Color(255, 255, 255), TEXT_ALIGN_LEFT, TEXT_ALIGN_CENTER)
end)
