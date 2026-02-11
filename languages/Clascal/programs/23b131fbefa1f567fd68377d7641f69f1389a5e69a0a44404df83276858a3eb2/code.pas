program HelloWorld;

type
  TGreeting = object
    message: string;
    procedure SetMessage(msg: string);
    procedure Display;
  end;

procedure TGreeting.SetMessage(msg: string);
begin
  message := msg;
end;

procedure TGreeting.Display;
begin
  writeln(message);
end;

var
  greeting: TGreeting;

begin
  greeting.SetMessage('Hello from Clascal!');
  greeting.Display;
end.
