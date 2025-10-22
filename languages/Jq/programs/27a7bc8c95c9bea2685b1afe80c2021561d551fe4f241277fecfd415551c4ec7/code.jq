def has($key): has($key) as $x | if $x then $x else false end;

def map_values(f): .[] |= f;

def to_entries: [keys_unsorted[] as $k | {key: $k, value: .[$k]}];

def from_entries:
  map({(.key // .Key // .name // .Name): (if has("value") then .value else .Value end)}) | add;

def with_entries(f): to_entries | map(f) | from_entries;

def reverse: [.[length - 1 - range(0;length)]];

def indices($i): if type == "array" then range(0;length) as $ix | select(.[$ix] == $i) | $ix
            elif type == "string" then explode | indices($i) end;