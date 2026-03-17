<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<%
    for (int i = 1; i <= 100; i++) {
        if (i % 15 == 0)      out.println("FizzBuzz");
        else if (i % 3 == 0)  out.println("Fizz");
        else if (i % 5 == 0)  out.println("Buzz");
        else                  out.println(i);
    }
%>
