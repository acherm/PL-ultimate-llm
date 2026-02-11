RULE Expression: expr
   Alternative
      left:Expression '+' right:Term    { $$ = $left + $right; }
   END Alternative
   Alternative
      left:Expression '-' right:Term    { $$ = $left - $right; }
   END Alternative
   Alternative
      term:Term                          { $$ = $term; }
   END Alternative
END RULE;

RULE Term: term
   Alternative
      left:Term '*' right:Factor        { $$ = $left * $right; }
   END Alternative
   Alternative
      left:Term '/' right:Factor        { $$ = $left / $right; }
   END Alternative
   Alternative
      factor:Factor                     { $$ = $factor; }
   END Alternative
END RULE;

RULE Factor: factor
   Alternative
      '(' expr:Expression ')'           { $$ = $expr; }
   END Alternative
   Alternative
      num:Number                        { $$ = $num; }
   END Alternative
END RULE;
