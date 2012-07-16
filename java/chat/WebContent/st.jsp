<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@page import="java.util.*"%> 
<% 
ArrayList al_say=new ArrayList();
ArrayList user=new ArrayList();
//创建ArrayList数组www.itstudy.cn 
application.setAttribute("say",al_say);
application.setAttribute("user", user);
response.sendRedirect("startup.jsp"); 
%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>

</body>
</html>