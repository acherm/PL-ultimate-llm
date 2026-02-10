#include <Button.h>

const int button1Pin = 4;
const int button2Pin = 5;

Button button1 = Button(button1Pin, BUTTON_PULLUP_INTERNAL);
Button button2 = Button(button2Pin, BUTTON_PULLUP_INTERNAL);

void handleButtonPressEvents(Button &btn)
{
  Serial.print("Button on pin ");
  Serial.print(btn.getPin(), DEC);
  Serial.print(" press");
  if (btn.getClickCount() > 1)
  {
    Serial.print(" <multiClick ");
    Serial.print(btn.getClickCount());
    Serial.print(">");
  }
  Serial.println();
}

void handleButtonReleaseEvents(Button &btn)
{
  Serial.print("Button on pin ");
  Serial.print(btn.getPin(), DEC);
  Serial.println(" release");
}

void handleButtonClickEvents(Button &btn)
{
  Serial.print("Button on pin ");
  Serial.print(btn.getPin(), DEC);
  Serial.print(" click");
  if (btn.getClickCount() > 1)
  {
    Serial.print(" <multiClick ");
    Serial.print(btn.getClickCount());
    Serial.print(">");
  }
  Serial.println();
}

void handleButtonHoldEvents(Button &btn)
{
  Serial.print("Button on pin ");
  Serial.print(btn.getPin(), DEC);
  Serial.print(" hold");
  if (btn.getHoldRepeatCount() > 0)
  {
    Serial.print(" <holdRepeat ");
    Serial.print(btn.getHoldRepeatCount());
    Serial.print(">");
  }
  Serial.println();
}

void scanButtons()
{
  button1.scan();
  button2.scan();
}

void setup()
{
  Serial.begin(9600);
  button1.pressHandler(handleButtonPressEvents);
  button1.releaseHandler(handleButtonReleaseEvents);
  button1.clickHandler(handleButtonClickEvents);
  button1.holdHandler(handleButtonHoldEvents, 1000);
  button1.setHoldRepeat(500);
  button1.setMultiClickThreshold(250);

  button2.pressHandler(handleButtonPressEvents);
  button2.releaseHandler(handleButtonReleaseEvents);
  button2.clickHandler(handleButtonClickEvents);
  button2.holdHandler(handleButtonHoldEvents, 1000);
  button2.setHoldRepeat(500);
  button2.setMultiClickThreshold(250);
}

void loop()
{
  scanButtons();
}
