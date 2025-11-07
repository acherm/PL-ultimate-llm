; Auto-Join on connect script by Jonathon.
; http://jonathonw.com
;
; This script will automatically join channels listed in the channels.txt file when you connect to a server.
; The channels.txt file should be in the same directory as mIRC.exe.
; Each channel should be on a new line.
;
; Version 1.0 - 2008-01-20

on *:CONNECT: {
  if ($server == irc.efnet.net) {
    var %i = 1, %chan
    while ($read(channels.txt, n, %i)) {
      %chan = $gettok($read(channels.txt, n, %i), 1, 32)
      join %chan
      inc %i
    }
  }
}