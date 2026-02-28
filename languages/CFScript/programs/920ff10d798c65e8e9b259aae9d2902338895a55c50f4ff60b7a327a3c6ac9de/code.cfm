<cfscript>
function fibonacci(n) {
    if (n LTE 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

for (i=0; i LTE 10; i++) {
    writeOutput(fibonacci(i) & " ");
}
</cfscript>
