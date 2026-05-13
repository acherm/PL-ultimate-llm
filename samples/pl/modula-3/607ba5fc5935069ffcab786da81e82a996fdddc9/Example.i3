INTERFACE Example;

IMPORT NetObj;

FROM Thread IMPORT Alerted;

EXCEPTION Reject(TEXT);

TYPE
  T = NetObj.T OBJECT METHODS
    setText (name: TEXT): TEXT RAISES {Reject, NetObj.Error, Alerted};
    sayGoodBye () RAISES {NetObj.Error, Alerted};
  END;

END Example.
