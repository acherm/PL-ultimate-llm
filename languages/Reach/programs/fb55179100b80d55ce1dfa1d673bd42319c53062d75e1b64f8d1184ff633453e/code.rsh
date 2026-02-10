'reach 0.1';

export const main = Reach.App(() => {
  const Alice = Participant('Alice', {
    getParams: Fun([], UInt),
  });
  const Bob = Participant('Bob', {
    acceptWager: Fun([UInt], Null),
  });
  init();

  Alice.only(() => {
    const wager = declassify(interact.getParams());
  });
  Alice.publish(wager);
  commit();

  Bob.only(() => {
    interact.acceptWager(wager);
  });
  Bob.pay(wager);
  commit();

  exit();
});
