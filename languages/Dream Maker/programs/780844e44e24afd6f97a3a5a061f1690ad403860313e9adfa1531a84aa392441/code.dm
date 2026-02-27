proc/Constellation(day)
   //day should be 1 to 365
   switch(day)
      if(355 to 365) return "Capricorn"
      if(326 to 354) return "Sagittarius"
      if(296 to 325) return "Scorpio"
      if(266 to 295) return "Libra"
      if(235 to 265) return "Virgo"
      if(204 to 234) return "Leo"
      if(173 to 203) return "Cancer"
      if(142 to 172) return "Gemini"
      if(111 to 141) return "Taurus"
      if(80  to 110) return "Aries"
      if(51  to  79) return "Pisces"
      if(21  to  50) return "Aquarius"
      if(1   to  20) return "Capricorn"
      else           return "Dan!"
