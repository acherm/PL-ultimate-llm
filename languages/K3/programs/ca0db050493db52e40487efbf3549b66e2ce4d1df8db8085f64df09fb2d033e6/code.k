/ K3: Array statistics
data:1 2 3 4 5 6 7 8 9 10
`0:"Count: ",$#data
`0:"Sum:   ",$+/data
`0:"Mean:  ",$(+/data)%#data
`0:"Max:   ",$|/data
`0:"Min:   ",$&/data
