<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="java.util.*"%>
<%! String username; %>
<% 
//String username=new String (request.getParameter("user").getBytes("iso-8859-1")); 
//张老师 
%>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>
<form action="temp.jsp" type="get">
<p>talk:<input type="text" name="say"></p>
<br>
<input type="submit" name="submit">
<br>
</form>

<%
ArrayList  al_say=new ArrayList();
al_say=(ArrayList)application.getAttribute("say");

//www.deepteach.com 
%>


<%
for(int i=0; i < al_say.size(); i++)
	out.println(al_say.get(i).toString()+ "<br>");
%>
</body>
</html>