Object subclass: #Integer
  methods: [
    factorial [
      self <= 1
        ifTrue: [ ^1 ]
        ifFalse: [ ^self * (self - 1) factorial ]
    ]
  ]

5 factorial print
