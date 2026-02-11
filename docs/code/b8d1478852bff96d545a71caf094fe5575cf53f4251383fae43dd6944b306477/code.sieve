require ["fileinto", "reject"];

if header :contains "from" "coyote" {
  fileinto "INBOX.coyote";
} elsif header :contains "subject" "MAKE MONEY FAST" {
  reject "I do not participate in illegal schemes.";
} else {
  keep;
}
