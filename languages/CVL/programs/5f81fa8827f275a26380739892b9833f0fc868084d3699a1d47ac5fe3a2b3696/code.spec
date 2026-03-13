/*
 * ERC20 token transfer specification in CVL (Certora Verification Language).
 * Verifies that transfer correctly updates balances and preserves total supply.
 */

methods {
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address account) external returns (uint256) envfree;
    function transfer(address to, uint256 amount) external returns (bool);
}

/// Transfer decreases sender balance and increases receiver balance by the same amount
rule transferIntegrity(address sender, address receiver, uint256 amount) {
    env e;
    require e.msg.sender == sender;
    require sender != receiver;

    uint256 senderBefore = balanceOf(sender);
    uint256 receiverBefore = balanceOf(receiver);

    transfer(e, receiver, amount);

    uint256 senderAfter = balanceOf(sender);
    uint256 receiverAfter = balanceOf(receiver);

    assert senderAfter == senderBefore - amount,
        "Sender balance not decreased by transfer amount";
    assert receiverAfter == receiverBefore + amount,
        "Receiver balance not increased by transfer amount";
}

/// Total supply is preserved by transfer operations
rule transferPreservesTotalSupply(address to, uint256 amount) {
    env e;
    uint256 supplyBefore = totalSupply();
    transfer(e, to, amount);
    uint256 supplyAfter = totalSupply();
    assert supplyBefore == supplyAfter,
        "Transfer should not change total supply";
}
