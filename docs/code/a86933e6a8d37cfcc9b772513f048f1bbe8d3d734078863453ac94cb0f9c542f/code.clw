MEMBER('StringBuilder')

    INCLUDE('StringBuilder.inc'),ONCE

    MAP
    END

StringBuilder.Construct     PROCEDURE()
        CODE
        SELF.Text &= NEW CHAR[1]
        SELF.Text = ''

StringBuilder.Destruct      PROCEDURE()
        CODE
        DISPOSE(SELF.Text)

StringBuilder.Append        PROCEDURE(STRING pText)
NewSize     LONG
        CODE
        IF pText <> ''
            NewSize = LEN(CLIP(SELF.Text)) + LEN(CLIP(pText)) + 1
            IF SIZE(SELF.Text) < NewSize
                RESIZE(SELF.Text, NewSize)
            END
            SELF.Text = CLIP(SELF.Text) & CLIP(pText)
        END

StringBuilder.ToString      PROCEDURE()
        CODE
        RETURN SELF.Text