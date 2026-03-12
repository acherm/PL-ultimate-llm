<%@ page contentType="text/html;charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>Book List</title>
</head>
<body>
    <h1><g:message code="book.list.label" default="Book List"/></h1>
    <g:if test="${bookList}">
        <ul>
            <g:each in="${bookList}" status="i" var="book">
                <li class="${(i % 2) == 0 ? 'odd' : 'even'}">
                    <g:link action="show" id="${book.id}">
                        ${book.title.encodeAsHTML()}
                    </g:link>
                </li>
            </g:each>
        </ul>
    </g:if>
    <g:else>
        <p>No books found.</p>
    </g:else>
    <div>
        <g:link action="create">
            <g:message code="book.new" default="New Book"/>
        </g:link>
    </div>
</body>
</html>
