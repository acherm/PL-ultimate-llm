// Simple counter smart contract in Tolk
// The contract state stores a 64-bit integer counter

fun loadCounter(): int {
    var ds = getContractData().beginParse();
    return ds.loadUint(64);
}

fun saveCounter(counter: int) {
    setContractData(
        beginCell()
            .storeUint(counter, 64)
            .endCell()
    );
}

fun onInternalMessage(myBalance: int, msgValue: int, inMsg: cell) {
    var cs = inMsg.beginParse();
    var flags = cs.loadUint(4);
    if (flags & 1) {
        return;
    }
    var op = cs.loadUint(32);
    if (op == 1) {
        saveCounter(loadCounter() + 1);
    }
}

get fun counter(): int {
    return loadCounter();
}
