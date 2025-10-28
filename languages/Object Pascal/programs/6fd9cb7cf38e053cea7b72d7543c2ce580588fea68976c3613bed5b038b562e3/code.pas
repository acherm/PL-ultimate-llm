program SimpleClassExample;

{$mode objfpc}{$H+}

uses
  Classes;

type
  { TDog }

  TDog = class
  private
    FName: string;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Bark;
    property Name: string read FName write FName;
  end;

{ TDog }

constructor TDog.Create;
begin
  inherited Create;
  Writeln('A dog is born');
  FName := 'Fido';
end;

destructor TDog.Destroy;
begin
  Writeln('A dog has died');
  inherited Destroy;
end;

procedure TDog.Bark;
begin
  Writeln(FName, ' says Woof!');
end;

var
  ADog: TDog;
begin
  ADog := TDog.Create;
  try
    ADog.Bark;
    ADog.Name := 'Rover';
    ADog.Bark;
  finally
    ADog.Free;
  end;
end.