declare function local:list($collection as xs:string, $path as xs:string) {
    let $resources := xmldb:get-child-resources($collection)
    let $collections := xmldb:get-child-collections($collection)
    return
        (
        for $res in $resources
        return
            <resource path="{$path || "/" || $res}">{$res}</resource>
        ,
        for $col in $collections
        return
            <collection path="{$path || "/" || $col}">
            {
                local:list($collection || "/" || $col, $path || "/" || $col)
            }
            </collection>
        )
};

local:list("/db", "")