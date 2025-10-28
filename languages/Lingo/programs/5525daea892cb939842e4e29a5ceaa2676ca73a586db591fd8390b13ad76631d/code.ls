-- Simon Says game
-- by UW CSE 120 staff

-- This script is a movie script.
-- It keeps track of the game state.

-- properties are global variables for this movie
property sequence -- the sequence of colors to be repeated
property player_sequence -- the sequence of colors the player has clicked
property buttons -- a list of the button sprites
property game_state -- what's happening now?
-- #waiting: waiting for the player to start a game
-- #showing: showing the player the sequence
-- #playing: waiting for the player to repeat the sequence
-- #game_over: the player has made a mistake

on startMovie
  -- initialize all the properties
  sequence = []
  player_sequence = []
  buttons = [sprite 2, sprite 3, sprite 4, sprite 5]
  game_state = #waiting
  
  -- set the text fields
  member("message").text = "Click to start"
  member("score").text = "0"
end

-- add a new random color to the sequence
on new_color
  sequence.add(random(4))
  member("score").text = string(sequence.count)
end

-- start showing the sequence to the player
on show_sequence
  game_state = #showing
  member("message").text = "Watch carefully"
  
  -- tell the first button to light up
  -- it will tell the next one, and so on
  sendSprite(buttons[sequence[1]].spriteNum, #light_up, 1)
end

-- this is called by the last button in the sequence
on sequence_done
  game_state = #playing
  player_sequence = []
  member("message").text = "Your turn"
end

-- this is called by the buttons when the player clicks them
on button_clicked me, button_num
  -- if we're not in the right state, do nothing
  if game_state <> #playing then return
  
  player_sequence.add(button_num)
  
  -- check if this is the right button
  if sequence[player_sequence.count] <> button_num then
    -- wrong button!
    game_state = #game_over
    member("message").text = "Game Over! Click to play again"
    puppetSound("oops")
  else
    -- right button!
    puppetSound("button" & button_num)
    
    -- if the sequence is complete, start the next round
    if player_sequence.count = sequence.count then
      -- wait a second, then start the next round
      startTimer(#next_round, 60, 1)
    end if
  end if
end

on next_round
  new_color()
  show_sequence()
end