# Simple Moving Average Crossover
# This study plots two simple moving averages and signals when they cross

declare lower;

input fastLength = 9;
input slowLength = 21;

def fastMA = SimpleMovingAvg(close, fastLength);
def slowMA = SimpleMovingAvg(close, slowLength);

plot FastLine = fastMA;
plot SlowLine = slowMA;

FastLine.SetDefaultColor(Color.GREEN);
SlowLine.SetDefaultColor(Color.RED);

# Signal when fast crosses above slow (bullish)
def crossAbove = fastMA crosses above slowMA;
def crossBelow = fastMA crosses below slowMA;

plot BuySignal = if crossAbove then 1 else Double.NaN;
plot SellSignal = if crossBelow then 1 else Double.NaN;

BuySignal.SetPaintingStrategy(PaintingStrategy.BOOLEAN_ARROW_UP);
BuySignal.SetDefaultColor(Color.UPTICK);
SellSignal.SetPaintingStrategy(PaintingStrategy.BOOLEAN_ARROW_DOWN);
SellSignal.SetDefaultColor(Color.DOWNTICK);
