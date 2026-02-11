/*##############################################################################
## HPCC SYSTEMS software Copyright (C) 2012 HPCC Systems®.  All rights reserved.
############################################################################## */
// DEDUP vs. SELECTN
//For each person, create a list of the 2 states they lived in the longest
//Assume the data is sorted by person id, then by years in state descending

Rec := RECORD
  UNSIGNED4 PersonID;
  STRING15  FirstName;
  STRING25  LastName;
  STRING2   State;
  UNSIGNED2 YearsInState;
END;

People := DATASET([ {1,'Kevin','Hall','FL',4},
                    {1,'Kevin','Hall','GA',2},
                    {1,'Kevin','Hall','PA',1},
                    {2,'Liz','Smith','AZ',3},
                    {2,'Liz','Smith','CA',2},
                    {3,'John','X','FL',8},
                    {3,'John','X','GA',7},
                    {3,'John','X','NY',6},
                    {3,'John','X','CA',5},
                    {4,'Jane','Doe','CA',10},
                    {4,'Jane','Doe','FL',1} ], Rec);

//Using DEDUP
OUTPUT(DEDUP(People,PersonID,KEEP 2));

//Using SELECTN
OUTPUT(People,CHOOSEN(ROWS(LEFT),2),PersonID);