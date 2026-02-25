( var i = 0; (1..100).do({ i = i + 1;

  case
{(i%15==0)} {"FizzBuzz".postln}
       {(i%3==0)}  {"Fizz".postln}
       {(i%5==0)} {"Buzz".postln}
       {i.postln};

}) )
