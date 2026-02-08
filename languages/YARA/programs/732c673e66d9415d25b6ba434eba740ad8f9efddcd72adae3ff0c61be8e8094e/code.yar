rule ExampleMalware
{
    meta:
        description = "Detects example malware pattern"
        author = "Security Researcher"
        date = "2024-01-01"

    strings:
        $mz = "MZ"
        $string1 = "malicious" nocase
        $string2 = "backdoor" nocase
        $hex_string = { 6A 40 68 00 30 00 00 }

    condition:
        $mz at 0 and (
            $string1 or $string2 or $hex_string
        ) and filesize < 5MB
}
