let

    Records = [
        [CustomerID = 1, Name = "Bob", Phone = "123-4567"],
        [CustomerID = 2, Name = "Jim", Phone = "987-6543"],
        [CustomerID = 3, Name = "Paul", Phone = "543-9378"]
    ],

    TableFromRecords = Table.FromRecords(Records)

in

    TableFromRecords