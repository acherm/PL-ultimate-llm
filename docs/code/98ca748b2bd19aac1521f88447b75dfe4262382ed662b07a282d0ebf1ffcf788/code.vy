# @version ^0.3.1

# Simple auction contract

# Auction parameters
beneficiary: public(address)
auctionStart: public(uint256)
auctionEnd: public(uint256)

# Current state of auction
highestBidder: public(address)
highestBid: public(uint256)
pendingReturns: public(HashMap[address, uint256])

# Set to true at the end, disallows any change
ended: public(bool)

# Events that will be fired on changes.
HighestBidIncreased: event({bidder: indexed(address), amount: uint256})
AuctionEnded: event({winner: indexed(address), amount: uint256})


@external
def __init__(_beneficiary: address, _bidding_time: uint256):
    self.beneficiary = _beneficiary
    self.auctionStart = block.timestamp
    self.auctionEnd = self.auctionStart + _bidding_time


@external
@payable
def bid():
    # Check if bidding period is over.
    assert block.timestamp < self.auctionEnd, "Auction already ended"

    # Check if bid is high enough
    assert msg.value > self.highestBid, "There already is a higher bid"

    # Track the previous bidder's refund
    if self.highestBid != 0:
        self.pendingReturns[self.highestBidder] += self.highestBid

    # Track new highest bid
    self.highestBidder = msg.sender
    self.highestBid = msg.value

    log HighestBidIncreased(msg.sender, msg.value)


@external
def withdraw() -> bool:
    pending_amount: uint256 = self.pendingReturns[msg.sender]
    if pending_amount > 0:
        self.pendingReturns[msg.sender] = 0
        send(msg.sender, pending_amount)
    return True


@external
def endAuction():
    # 1. Conditions
    assert block.timestamp >= self.auctionEnd, "Auction not yet ended"
    assert not self.ended, "auctionEnd has already been called"

    # 2. Effects
    self.ended = True
    log AuctionEnded(self.highestBidder, self.highestBid)

    # 3. Interaction
    send(self.beneficiary, self.highestBid)