<%@ page language="java" contentType="text/html; charset=gb2312"
    pageEncoding="gb2312"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%!int Num=0; %>
<%
if(session.isNew()) {
	Num += 1;
	session.setAttribute("Num", Num);
}
%>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>session对象计数</title>
</head>

<body>
<%=session.getAttribute("Num") %>
</body>
</html>
