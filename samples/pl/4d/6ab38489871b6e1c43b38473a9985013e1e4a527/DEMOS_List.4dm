//%attributes = {"shared":true}

var $0; $voOUT : Object
var $1; $voIN : Object
var $2; $session : Object

$voIN:=$1
$session:=$2

//テーブル名でコレクションを返却
$voOUT:=New object:C1471
$voOUT[Table name:C256(->[sites:5])]:=\
ds:C1482.sites.all().orderBy("title asc").toCollection()  //"[sites]" テーブルを全件取得し "title" フィールドの昇順でソート

$0:=$voOUT

