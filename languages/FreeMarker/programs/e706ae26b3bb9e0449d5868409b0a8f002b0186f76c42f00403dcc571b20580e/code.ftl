<#assign user = "John Doe">
<#assign age = 30>

<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Hello, ${user}!</h1>
    <#if age >= 18>
        <p>You are an adult.</p>
    <#else>
        <p>You are a minor.</p>
    </#if>

    <h2>Favorites</h2>
    <#assign favorites = ["Reading", "Coding", "Hiking"]>
    <ul>
    <#list favorites as item>
        <li>${item}</li>
    </#list>
    </ul>
</body>
</html>
