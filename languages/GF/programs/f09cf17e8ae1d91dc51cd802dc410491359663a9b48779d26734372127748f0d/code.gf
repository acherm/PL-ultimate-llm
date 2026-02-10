abstract Hello = {
  cat
    Greeting;
  fun
    Hello : Greeting;
    Goodbye : Greeting;
}

concrete HelloEng of Hello = {
  lincat
    Greeting = Str;
  lin
    Hello = "hello";
    Goodbye = "goodbye";
}