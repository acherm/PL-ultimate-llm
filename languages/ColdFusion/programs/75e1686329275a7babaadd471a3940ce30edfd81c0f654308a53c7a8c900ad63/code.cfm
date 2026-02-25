<cffunction name="fibonacci" returntype="numeric" access="public">
    <cfargument name="n" type="numeric" required="true">
    <cfif arguments.n LTE 1>
        <cfreturn arguments.n>
    </cfif>
    <cfreturn fibonacci(arguments.n - 1) + fibonacci(arguments.n - 2)>
</cffunction>

<cfset result = []>
<cfloop from="0" to="10" index="i">
    <cfset arrayAppend(result, fibonacci(i))>
</cfloop>

<cfoutput>Fibonacci sequence (0-10): #arrayToList(result, ", ")#</cfoutput>
