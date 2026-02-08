VAR S REAL RELATION { SNO CHAR, SNAME CHAR, STATUS INTEGER, CITY CHAR } KEY { SNO };
VAR P REAL RELATION { PNO CHAR, PNAME CHAR, COLOR CHAR, WEIGHT RATIONAL, CITY CHAR } KEY { PNO };
VAR SP REAL RELATION { SNO CHAR, PNO CHAR, QTY INTEGER } KEY { SNO, PNO };

S := RELATION {
  TUPLE { SNO "S1", SNAME "Smith", STATUS 20, CITY "London" },
  TUPLE { SNO "S2", SNAME "Jones", STATUS 10, CITY "Paris" },
  TUPLE { SNO "S3", SNAME "Blake", STATUS 30, CITY "Paris" },
  TUPLE { SNO "S4", SNAME "Clark", STATUS 20, CITY "London" },
  TUPLE { SNO "S5", SNAME "Adams", STATUS 30, CITY "Athens" }
};

P := RELATION {
  TUPLE { PNO "P1", PNAME "Nut", COLOR "Red", WEIGHT 12.0, CITY "London" },
  TUPLE { PNO "P2", PNAME "Bolt", COLOR "Green", WEIGHT 17.0, CITY "Paris" },
  TUPLE { PNO "P3", PNAME "Screw", COLOR "Blue", WEIGHT 17.0, CITY "Oslo" },
  TUPLE { PNO "P4", PNAME "Screw", COLOR "Red", WEIGHT 14.0, CITY "London" },
  TUPLE { PNO "P5", PNAME "Cam", COLOR "Blue", WEIGHT 12.0, CITY "Paris" },
  TUPLE { PNO "P6", PNAME "Cog", COLOR "Red", WEIGHT 19.0, CITY "London" }
};

SP := RELATION {
  TUPLE { SNO "S1", PNO "P1", QTY 300 },
  TUPLE { SNO "S1", PNO "P2", QTY 200 },
  TUPLE { SNO "S1", PNO "P3", QTY 400 },
  TUPLE { SNO "S1", PNO "P4", QTY 200 },
  TUPLE { SNO "S2", PNO "P1", QTY 300 },
  TUPLE { SNO "S2", PNO "P2", QTY 400 },
  TUPLE { SNO "S3", PNO "P2", QTY 200 },
  TUPLE { SNO "S4", PNO "P2", QTY 200 },
  TUPLE { SNO "S4", PNO "P4", QTY 300 }
};

// Suppliers in London
(S WHERE CITY = "London") { SNAME };

// Natural join of suppliers and shipments, projected on supplier name and part number
(S JOIN SP) { SNAME, PNO };

// Suppliers who supply part P2
(SP WHERE PNO = "P2") { SNO } JOIN S { SNO, SNAME };
