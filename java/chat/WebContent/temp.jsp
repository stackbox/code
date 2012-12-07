<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@page import="java.util.*"%> 
<%
String say=new String (request.getParameter("say").getBytes("iso-8859-1")); 
ArrayList al_say=new ArrayList(); 
al_say=(ArrayList)application.getAttribute("say"); 
al_say.add(say);
response.sendRedirect("chart.jsp");
%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>

</body>
</html>