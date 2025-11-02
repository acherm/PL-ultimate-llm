g.addV('person').property(id, 1).property('name', 'marko').property('age', 29).as('marko').
  addV('person').property(id, 2).property('name', 'vadas').property('age', 27).as('vadas').
  addV('software').property(id, 3).property('name', 'lop').property('lang', 'java').as('lop').
  addV('person').property(id, 4).property('name', 'josh').property('age', 32).as('josh').
  addV('software').property(id, 5).property('name', 'ripple').property('lang', 'java').as('ripple').
  addV('person').property(id, 6).property('name', 'peter').property('age', 35).as('peter').
  addE('knows').from('marko').to('vadas').property('weight', 0.5f).
  addE('knows').from('marko').to('josh').property('weight', 1.0f).
  addE('created').from('marko').to('lop').property('weight', 0.4f).
  addE('created').from('josh').to('ripple').property('weight', 1.0f).
  addE('created').from('josh').to('lop').property('weight', 0.4f).
  addE('created').from('peter').to('lop').property('weight', 0.2f)