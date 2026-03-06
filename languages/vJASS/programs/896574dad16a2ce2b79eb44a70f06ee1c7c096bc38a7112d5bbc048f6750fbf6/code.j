library StackDemo

    struct Stack
        private integer array data[100]
        private integer size

        static method create takes nothing returns thistype
            local thistype this = thistype.allocate()
            set this.size = 0
            return this
        endmethod

        method push takes integer value returns nothing
            if this.size < 100 then
                set this.data[this.size] = value
                set this.size = this.size + 1
            endif
        endmethod

        method pop takes nothing returns integer
            if this.size > 0 then
                set this.size = this.size - 1
                return this.data[this.size]
            endif
            return 0
        endmethod

        method isEmpty takes nothing returns boolean
            return this.size == 0
        endmethod

        method destroy takes nothing returns nothing
            call this.deallocate()
        endmethod
    endstruct

    function DemoStack takes nothing returns nothing
        local Stack s = Stack.create()
        local integer i = 1
        loop
            exitwhen i > 5
            call s.push(i * 10)
            set i = i + 1
        endloop
        loop
            exitwhen s.isEmpty()
            call BJDebugMsg("Popped: " + I2S(s.pop()))
        endloop
        call s.destroy()
    endfunction

endlibrary
