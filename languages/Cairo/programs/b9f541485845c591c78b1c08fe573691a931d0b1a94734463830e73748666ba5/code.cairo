#[starknet::contract]
mod SimpleStorage {
    use starknet::ContractAddress;

    #[storage]
    struct Storage {
        stored_data: u256,
    }

    #[abi(embed_v0)]
    impl SimpleStorageImpl of super::ISimpleStorage<ContractState> {
        fn set(ref self: ContractState, value: u256) {
            self.stored_data.write(value);
        }

        fn get(self: @ContractState) -> u256 {
            self.stored_data.read()
        }
    }

    #[generate_trait]
    impl ISimpleStorage<T> of ISimpleStorageTrait<T> {
        fn set(ref self: T, value: u256);
        fn get(self: @T) -> u256;
    }
}