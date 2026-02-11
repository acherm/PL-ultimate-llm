<!--- Hello World in Lucee --->
<cfset greeting = "Hello, World!">
<cfoutput>#greeting#</cfoutput>

<!--- Function example --->
<cffunction name="fibonacci" returntype="numeric">
    <cfargument name="n" type="numeric" required="true">
    <cfif arguments.n LTE 1>
        <cfreturn arguments.n>
    <cfelse>
        <cfreturn fibonacci(arguments.n - 1) + fibonacci(arguments.n - 2)>
    </cfif>
</cffunction>

<!--- Calculate Fibonacci --->
<cfset result = fibonacci(10)>
<cfoutput>Fibonacci(10) = #result#</cfoutput>