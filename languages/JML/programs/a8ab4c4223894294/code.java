public class BankAccount {
    private /*@ spec_public @*/ int balance;

    //@ invariant balance >= 0;

    /*@ requires initialBalance >= 0;
      @ ensures balance == initialBalance;
      @*/
    public BankAccount(int initialBalance) {
        this.balance = initialBalance;
    }

    /*@ requires amount >= 0;
      @ ensures balance == \old(balance) + amount;
      @*/
    public void deposit(int amount) {
        balance = balance + amount;
    }

    /*@ requires amount >= 0 && amount <= balance;
      @ ensures balance == \old(balance) - amount;
      @*/
    public void withdraw(int amount) {
        balance = balance - amount;
    }

    /*@ ensures \result == balance;
      @*/
    public /*@ pure @*/ int getBalance() {
        return balance;
    }
}
