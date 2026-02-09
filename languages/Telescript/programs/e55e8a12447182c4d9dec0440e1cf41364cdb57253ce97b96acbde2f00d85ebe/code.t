CatalogEntry: class = (
  public
     see initialize
     see adjustPrice
     product: String;
     price: Integer; // cents
  property
     lock: Resource;
);
initialize: op (product: String; price: Integer) = {
  ^();
  lock = Resource()
};
adjustPrice: op (percentage: Integer) throws ReferenceProtected = {
  use lock   {
    price = price + (price*percentage).quotient(100)
  }
};
Warehouse: class (Place, EventProcess) = (
  public
    see initialize
    see live
    see getCatalog
  property
    catalog: Dictionary[String, CatalogEntry];
);
initialize: op (catalog: owned Dictionary[String, CatalogEntry]) = {
  ^()
};
live: sponsored op (cause: Exception|Nil) = {
  loop {
    // await the first day of the month
    time: = Time();
    calendarTime: = time.asCalendarTime();
    calendarTime.month = calendarTime.month + 1;
    calendarTime.day = 1;
    *.wait(calendarTime.asTime().interval(time));
    // reduce all prices by 5%
    for product: String in catalog {
      try { catalog[product].adjustPrice(-5) }
      catch KeyInvalid { }
    };
  // make known the price reductions
  *.signalEvent(PriceReduction(), 'occupants)
  }
};
