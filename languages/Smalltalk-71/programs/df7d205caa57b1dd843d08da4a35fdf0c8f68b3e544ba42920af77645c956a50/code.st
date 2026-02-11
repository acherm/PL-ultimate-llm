class Integer
  method factorial
    self = 0 ifTrue: [^1].
    self = 1 ifTrue: [^1].
    ^self * (self - 1) factorial
  end
end

5 factorial print