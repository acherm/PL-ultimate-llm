# Example Cap'n Proto schema definition
# Defines a simple address book structure

@0x85150b117366d14c;

struct Person {
  id @0 :UInt32;
  name @1 :Text;
  email @2 :Text;

  phones @3 :List(PhoneNumber);

  employment :union {
    unemployed @4 :Void;
    employer @5 :Text;
    school @6 :Text;
    selfEmployed @7 :Void;
  }

  struct PhoneNumber {
    number @0 :Text;
    type @1 :Type;

    enum Type {
      mobile @0;
      home @1;
      work @2;
    }
  }
}

struct AddressBook {
  people @0 :List(Person);
}
