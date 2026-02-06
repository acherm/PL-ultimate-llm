\Fibonacci sequence generator
int N, F0, F1, F2;
[Text(0, "Enter how many Fibonacci numbers to display: ");
N:= IntIn(0);
F0:= 0;  F1:= 1;
IntOut(0, F0);  CrLf(0);
IntOut(0, F1);  CrLf(0);
for N:= N-2 downto 1 do
    [F2:= F0 + F1;
    IntOut(0, F2);  CrLf(0);
    F0:= F1;
    F1:= F2;
    ];
]
