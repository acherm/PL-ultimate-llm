//! account: alice, 10000000000000 0x1::STC::STC
//! account: joe
//! account: admin, 0x81144d60492982a45ba93fba47cae988, 10000000000000 0x1::STC::STC
//! account: liquidier, 10000000000000 0x1::STC::STC
//! account: exchanger

//! sender: alice
address alice = {{alice}};
module alice::TokenMock {
    // mock MyToken token
    struct MyToken has copy, drop, store { }

    // mock Usdx token
    struct Usdx has copy, drop, store { }
}


//! new-transaction
//! sender: alice
address alice = {{alice}};
script {
    use alice::TokenMock::{Usdx};
    use 0x1::Account;
    use 0x1::Token;
    use 0x1::Math;
    fun init(signer: signer) {
        let precision: u8 = 9; //STC precision is also 9.
        let scaling_factor = Math::pow(10, (precision as u64));
        let usdx_amount: u128 = 50000 * scaling_factor;
        // Resister and mint Usdx
        Token::register_token<Usdx>(&signer, precision);
        Account::do_accept_token<Usdx>(&signer);
        let usdx_token = Token::mint<Usdx>(&signer, usdx_amount);
        Account::deposit_to_self(&signer, usdx_token);
    }
}
// check: EXECUTED

//! new-transaction
//! sender: admin
address alice = {{alice}};
script {
    use alice::TokenMock::{Usdx};
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap;
    use 0x1::STC::STC;
    fun register_token_pair(signer: signer) {
        //token pair register must be swap admin account
        TokenSwap::register_swap_pair<STC, Usdx>(&signer);
        assert(TokenSwap::swap_pair_exists<STC, Usdx>(), 111);
    }
}
// check: EXECUTED


////! new-transaction
////! sender: liquidier
//// mint some Usdx to liquidier
//address alice = {{alice}};
//address liquidier = {{liquidier}};
//script{
//    use alice::TokenMock;
//    use 0x1::Account;
//    use 0x1::Token;
//    fun init_liquidier(signer: signer) {
//        let usdx_amount = 100000000;
//        Account::do_accept_token<TokenMock::Usdx>(&signer);
//        let usdx_token = Token::mint<TokenMock::Usdx>(&signer, usdx_amount);
//        Account::deposit_to_self(&signer, usdx_token);
//        assert(Account::balance<TokenMock::Usdx>(@liquidier) == 100000000, 42);
//    }
//}
//
//// check: EXECUTED


//! new-transaction
//! sender: alice
address alice = {{alice}};
script{
    use 0x1::STC;
    use alice::TokenMock;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap::LiquidityToken;
    use 0x1::Account;

    fun main(signer: signer) {
        Account::do_accept_token<LiquidityToken<STC::STC, TokenMock::Usdx>>(&signer);
        // STC/Usdx = 1:2
        let stc_amount = 10000;
        let usdx_amount = 20000;
        let stc = Account::withdraw<STC::STC>( &signer, stc_amount);
        let usdx = Account::withdraw<TokenMock::Usdx>( &signer, usdx_amount);
        let liquidity_token = TokenSwap::mint<STC::STC, TokenMock::Usdx>(stc, usdx);
        Account::deposit_to_self( &signer, liquidity_token);

        let (x, y) = TokenSwap::get_reserves<STC::STC, TokenMock::Usdx>();
        assert(x == stc_amount, 111);
        assert(y == usdx_amount, 112);
    }
}
// check: EXECUTED

//! new-transaction
//! sender: alice
address alice = {{alice}};
script {
    use 0x1::STC;
    use alice::TokenMock;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwapRouter;
    use 0x1::Account;
    use 0x1::Token;
    fun main(signer: signer) {
//        Account::do_accept_token<TokenMock::Usdx>(&signer);
        let stc_amount = 100000;
        let stc = Account::withdraw<STC::STC>( &signer, stc_amount);
        let amount_out = {
            let (x, y) = TokenSwap::get_reserves<STC::STC, TokenMock::Usdx>();
            TokenSwapRouter::get_amount_out(stc_amount, x, y)
        };
        let (stc_token, usdx_token) = TokenSwap::swap<STC::STC, TokenMock::Usdx>(stc, amount_out, Token::zero<TokenMock::Usdx>(), 0);
        Token::destroy_zero(stc_token);
        Account::deposit_to_self(&signer, usdx_token);
    }
}

// check: EXECUTED

//! new-transaction
//! sender: alice
address alice = {{alice}};
script{
    use 0x1::STC;
    use 0x1::Account;
    use 0x1::Signer;
    use alice::TokenMock;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap;
    use 0x81144d60492982a45ba93fba47cae988::TokenSwap::LiquidityToken;
    // use 0x1::Debug;

    fun main(signer: signer) {
        let liquidity_balance = Account::balance<LiquidityToken<STC::STC, TokenMock::Usdx>>(Signer::address_of( &signer));
        let liquidity = Account::withdraw<LiquidityToken<STC::STC, TokenMock::Usdx>>( &signer, liquidity_balance);
        let (stc, usdx) = TokenSwap::burn<STC::STC, TokenMock::Usdx>(liquidity);
        Account::deposit_to_self(&signer, stc);
        Account::deposit_to_self(&signer, usdx);

        let (x, y) = TokenSwap::get_reserves<STC::STC, TokenMock::Usdx>();
        assert(x == 0, 111);
        assert(y == 0, 112);
    }
}
// check: EXECUTED
