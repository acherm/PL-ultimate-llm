CREATE FUNCTION instr(text, text) RETURNS integer AS $$
DECLARE
    haystack ALIAS FOR $1;
    needle ALIAS FOR $2;
    pos integer;
    h_len integer;
    n_len integer;
    i integer;
BEGIN
    pos := 0;
    h_len := length(haystack);
    n_len := length(needle);

    IF h_len < n_len OR n_len = 0 THEN
        RETURN 0;
    END IF;

    i := 1;
    WHILE i <= (h_len - n_len + 1) LOOP
        IF substr(haystack, i, n_len) = needle THEN
            pos := i;
            EXIT;
        END IF;
        i := i + 1;
    END LOOP;

    RETURN pos;
END;
$$ LANGUAGE plpgsql;