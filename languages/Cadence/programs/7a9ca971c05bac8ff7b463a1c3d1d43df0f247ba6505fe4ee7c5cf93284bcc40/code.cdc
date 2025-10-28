/*
    Description: The Fungible Token standard's smart contract.
    This contract is a template for a basic fungible token.
    It is not meant to be deployed as-is, but to be imported by other contracts
    that wish to conform to the fungible token standard.
    License: Apache-2.0
*/
pub contract FungibleToken {

    // Event that is emitted when the total supply of a token increases
    pub event TokensInitialized(initialSupply: UFix64)

    // Event that is emitted when tokens are withdrawn from a Vault
    pub event TokensWithdrawn(amount: UFix64, from: Address?)

    // Event that is emitted when tokens are deposited to a Vault
    pub event TokensDeposited(amount: UFix64, to: Address?)

    // The total supply of the token in existence
    pub var totalSupply: UFix64

    // The interface that all Vaults are required to implement
    //
    pub resource interface Provider {

        // withdraw removes tokens from the implementing vault
        // and returns a vault with the removed tokens.
        //
        // The function's access level is public, but it is still constrained
        // by the access level of the variable that the resource is stored in.
        //
        pub fun withdraw(amount: UFix64): @Vault {
            post {
                // `result` is a keyword that refers to the return value of the function
                result.balance == UFix64(amount):
                    "Withdrawal amount must be the same as the balance of the withdrawn Vault"
            }
        }
    }

    // The interface that all Vaults are required to implement
    // in order to receive tokens.
    //
    pub resource interface Receiver {

        // deposit takes a Vault and adds its balance to the implementing vault
        pub fun deposit(from: @Vault) {
            pre {
                // `from` is a keyword that refers to the argument of the function
                from.balance > 0.0:
                    "Deposit balance must be positive"
            }
        }

        // The balance of the account.
        // The access level for this field is public,
        // but it is still constrained by the access level of the variable
        // that the resource is stored in.
        pub var balance: UFix64
    }

    // The interface that provides a read-only view of the Vault's balance
    //
    pub resource interface Balance {
        pub var balance: UFix64
    }

    // A Vault is a resource that stores a fungible token.
    // It is required to implement the Provider, Receiver, and Balance interfaces
    //
    pub resource Vault: Provider, Receiver, Balance {

        // The balance of the Vault
        pub var balance: UFix64

        // initialize the balance at resource creation time
        init(balance: UFix64) {
            self.balance = balance
        }

        // withdraw removes tokens from the vault and returns a new vault
        // with the removed tokens
        pub fun withdraw(amount: UFix64): @Vault {
            self.balance = self.balance - amount
            emit TokensWithdrawn(amount: amount, from: self.owner?.address)
            return <-create Vault(balance: amount)
        }

        // deposit takes a vault and adds its balance to this vault
        pub fun deposit(from: @Vault) {
            self.balance = self.balance + from.balance
            emit TokensDeposited(amount: from.balance, to: self.owner?.address)
            destroy from
        }

        destroy() {
            FungibleToken.totalSupply = FungibleToken.totalSupply - self.balance
        }
    }

    // createEmptyVault creates a new Vault with a balance of zero
    // and returns it to the calling context.
    pub fun createEmptyVault(): @Vault {
        return <-create Vault(balance: 0.0)
    }

    init() {
        self.totalSupply = 0.0
        emit TokensInitialized(initialSupply: self.totalSupply)
    }
}