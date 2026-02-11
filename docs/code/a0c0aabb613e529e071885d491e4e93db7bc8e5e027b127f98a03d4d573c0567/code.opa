Server.start(Server.http,
  {title: "Hello",
   page: function() {
     <h1>Hello, world!</h1>
   }
  }
)