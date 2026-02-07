MODULE Counter;

TYPE
	Counter* = OBJECT
	VAR
		value: LONGINT;

	PROCEDURE &Init*;
	BEGIN
		value := 0
	END Init;

	PROCEDURE Increment*;
	BEGIN {EXCLUSIVE}
		INC(value)
	END Increment;

	PROCEDURE GetValue*(): LONGINT;
	BEGIN {EXCLUSIVE}
		RETURN value
	END GetValue;

	END Counter;

BEGIN
END Counter.
