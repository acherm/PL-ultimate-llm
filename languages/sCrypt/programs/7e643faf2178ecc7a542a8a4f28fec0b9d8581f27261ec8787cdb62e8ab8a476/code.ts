import { SmartContract, method, prop, assert } from 'scrypt-ts'

export class Counter extends SmartContract {
    @prop()
    count: bigint

    constructor(count: bigint) {
        super(...arguments)
        this.count = count
    }

    @method()
    public increment() {
        this.count++
        assert(this.buildStateOutput())
    }
}
