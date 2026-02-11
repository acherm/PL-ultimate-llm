module Basic::Tutorial

// A simple Rascal module

// Define a function that takes a string and returns its length
int length(str s) = size(s);

// Define a function that takes a string and returns its reverse
str reverse(str s) = s[ size(s)-1.. 0 ];

// Define a function that takes a string and returns its uppercase version
str uppercase(str s) = toUpper(s);

// Define a function that takes a string and returns its lowercase version
str lowercase(str s) = toLower(s);

// Define a function that takes a string and returns its first character
str first(str s) = s[0];

// Define a function that takes a string and returns its last character
str last(str s) = s[size(s)-1];

// Define a function that takes a string and returns its substring from index 1 to 3
str substring(str s) = s[1..3];

// Define a function that takes a string and returns its concatenation with another string
str concat(str s1, str s2) = s1 + s2;

// Define a function that takes a string and returns its repetition 3 times
str repeat(str s) = s + s + s;

// Define a function that takes a string and returns its split into substrings separated by commas
list[str] split(str s) = split(s, ",");

// Define a function that takes a list of strings and returns its join into a single string separated by commas
str join(list[str] ss) = join(ss, ",");

// Define a function that takes a string and returns its trim
str trim(str s) = trim(s);

// Define a function that takes a string and returns its replace of all occurrences of a substring with another substring
str replace(str s, str old, str new) = replace(s, old, new);

// Define a function that takes a string and returns its match against a regular expression
bool match(str s, str regex) = s =~ regex;

// Define a function that takes a string and returns its search for a substring
int search(str s, str substr) = search(s, substr);

// Define a function that takes a string and returns its index of a substring
int index(str s, str substr) = index(s, substr);

// Define a function that takes a string and returns its last index of a substring
int lastindex(str s, str substr) = lastindex(s, substr);

// Define a function that takes a string and returns its contains a substring
bool contains(str s, str substr) = contains(s, substr);

// Define a function that takes a string and returns its starts with a substring
bool startsWith(str s, str substr) = startsWith(s, substr);

// Define a function that takes a string and returns its ends with a substring
bool endsWith(str s, str substr) = endsWith(s, substr);

// Define a function that takes a string and returns its equals to another string
bool equals(str s1, str s2) = s1 == s2;

// Define a function that takes a string and returns its not equals to another string
bool notEquals(str s1, str s2) = s1!= s2;

// Define a function that takes a string and returns its less than another string
bool lessThan(str s1, str s2) = s1 < s2;

// Define a function that takes a string and returns its less than or equals to another string
bool lessThanOrEqual(str s1, str s2) = s1 <= s2;

// Define a function that takes a string and returns its greater than another string
bool greaterThan(str s1, str s2) = s1 > s2;

// Define a function that takes a string and returns its greater than or equals to another string
bool greaterThanOrEqual(str s1, str s2) = s1 >= s2;

// Define a function that takes a string and returns its hash code
int hashCode(str s) = hashCode(s);

// Define a function that takes a string and returns its to integer
int toInt(str s) = toInt(s);

// Define a function that takes a string and returns its to float
real toFloat(str s) = toFloat(s);

// Define a function that takes a string and returns its to boolean
bool toBool(str s) = toBool(s);

// Define a function that takes a string and returns its to date
datetime toDateTime(str s) = toDateTime(s);

// Define a function that takes a string and returns its to time
datetime toTime(str s) = toTime(s);

// Define a function that takes a string and returns its to timestamp
datetime toTimestamp(str s) = toTimestamp(s);

// Define a function that takes a string and returns its to duration
reltime toDuration(str s) = toDuration(s);

// Define a function that takes a string and returns its to interval
reltime toInterval(str s) = toInterval(s);

// Define a function that takes a string and returns its to period
reltime toPeriod(str s) = toPeriod(s);

// Define a function that takes a string and returns its to range
range toRange(str s) = toRange(s);

// Define a function that takes a string and returns its to set
set[str] toSet(str s) = toSet(s);

// Define a function that takes a string and returns its to list
list[str] toList(str s) = toList(s);

// Define a function that takes a string and returns its to map
map[str,str] toMap(str s) = toMap(s);

// Define a function that takes a string and returns its to tuple
tuple[str,str] toTuple(str s) = toTuple(s);

// Define a function that takes a string and returns its to relation
rel[str,str] toRelation(str s) = toRelation(s);

// Define a function that takes a string and returns its to graph
graph[str,str] toGraph(str s) = toGraph(s);

// Define a function that takes a string and returns its to tree
node[str] toTree(str s) = toTree(s);

// Define a function that takes a string and returns its to XML
xml toXML(str s) = toXML(s);

// Define a function that takes a string and returns its to JSON
json toJSON(str s) = toJSON(s);

// Define a function that takes a string and returns its to CSV
csv toCSV(str s) = toCSV(s);

// Define a function that takes a string and returns its to TSV
list[str] toTSV(str s) = toTSV(s);

// Define a function that takes a string and returns its to properties
map[str,str] toProperties(str s) = toProperties(s);

// Define a function that takes a string and returns its to YAML
yaml toYAML(str s) = toYAML(s);

// Define a function that takes a string and returns its to INI
map[str,map[str,str]] toINI(str s) = toINI(s);

// Define a function that takes a string and returns its to TOML
map[str,map[str,str]] toTOML(str s) = toTOML(s);

// Define a function that takes a string and returns its to JSON5
json toJSON5(str s) = toJSON5(s);

// Define a function that takes a string and returns its to BSON
bson toBSON(str s) = toBSON(s);

// Define a function that takes a string and returns its to MessagePack
msgpack toMessagePack(str s) = toMessagePack(s);

// Define a function that takes a string and returns its to Protocol Buffers
protobuf toProtocolBuffers(str s) = toProtocolBuffers(s);

// Define a function that takes a string and returns its to Thrift
thrift toThrift(str s) = toThrift(s);

// Define a function that takes a string and returns its to Avro
avro toAvro(str s) = toAvro(s);

// Define a function that takes a string and returns its to ORC
orc toORC(str s) = toORC(s);

// Define a function that takes a string and returns its to Parquet
parquet toParquet(str s) = toParquet(s);

// Define a function that takes a string and returns its to Arrow
arrow toArrow(str s) = toArrow(s);

// Define a function that takes a string and returns its to Feather
feather toFeather(str s) = toFeather(s);

// Define a function that takes a string and returns its to IPC
ipc toIPC(str s) = toIPC(s);

// Define a function that takes a string and returns its to Cap'n Proto
capnproto toCapnProto(str s) = toCapnProto(s);

// Define a function that takes a string and returns its to FlatBuffers
flatbuffers toFlatBuffers(str s) = toFlatBuffers(s);

// Define a function that takes a string and returns its to CBOR
cbor toCBOR(str s) = toCBOR(s);

// Define a function that takes a string and returns its to Smile
smile toSmile(str s) = toSmile(s);

// Define a function that takes a string and returns its to UBJSON
ubjson toUBJSON(str s) = toUBJSON(s);

// Define a function that takes a string and returns its to BSON
bson toBSON(str s) = toBSON(s);

// Define a function that takes a string and returns its to JSONP
jsonp toJSONP(str s) = toJSONP(s);

// Define a function that takes a string and returns its to NDJSON
ndjson toNDJSON(str s) = toNDJSON(s);

// Define a function that takes a string and returns its to GeoJSON
geojson toGeoJSON(str s) = toGeoJSON(s);

// Define a function that takes a string and returns its to TopoJSON
topojson toTopoJSON(str s) = toTopoJSON(s);

// Define a function that takes a string and returns its to KML
kml toKML(str s) = toKML(s);

// Define a function that takes a string and returns its to KMZ
kmz toKMZ(str s) = toKMZ(s);

// Define a function that takes a string and returns its to GPX
gpx toGPX(str s) = toGPX(s);

// Define a function that takes a string and returns its to GeoRSS
georss toGeoRSS(str s) = toGeoRSS(s);

// Define a function that takes a string and returns its to GML
gml toGML(str s) = toGML(s);

// Define a function that takes a string and returns its to WKT
wkt toWKT(str s) = toWKT(s);

// Define a function that takes a string and returns its to WKB
wkb toWKB(str s) = toWKB(s);

// Define a function that takes a string and returns its to EWKT
ewkt toEWKT(str s) = toEWKT(s);

// Define a function that takes a string and returns its to EWKB
ewkb toEWKB(str s) = toEWKB(s);

// Define a function that takes a string and returns its to GeoHash
geohash toGeoHash(str s) = toGeoHash(s);

// Define a function that takes a string and returns its to S2
s2 toS2(str s) = toS2(s);

// Define a function that takes a string and returns its to H3
h3 toH3(str s) = toH3(s);

// Define a function that takes a string and returns its to MVT
mvt toMVT(str s) = toMVT(s);

// Define a function that takes a string and returns its to PBF
pbf toPBF(str s) = toPBF(s);

// Define a function that takes a string and returns its to LAS
las toLAS(str s) = toLAS(s);

// Define a function that takes a string and returns its to LAZ
laz toLAZ(str s) = toLAZ(s);

// Define a function that takes a string and returns its to ZLAS
zlas toZLAS(str s) = toZLAS(s);

// Define a function that takes a string and returns its to PLAS
plas toPLAS(str s) = toPLAS(s);

// Define a function that takes a string and returns its to E57
