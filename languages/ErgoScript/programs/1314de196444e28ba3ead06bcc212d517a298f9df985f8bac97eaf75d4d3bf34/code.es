{
  // Simple token issuance contract
  // This script allows spending if the correct token amount is present

  val tokenId = SELF.tokens(0)._1
  val tokenAmount = SELF.tokens(0)._2

  val validAmount = tokenAmount >= 1000L
  val validRecipient = OUTPUTS(0).propositionBytes == fromBase58("9f5ZKbECVTm25JTRQHDHGM5ehC8tUw5g1fCBQ4aaE")

  sigmaProp(validAmount && validRecipient)
}
