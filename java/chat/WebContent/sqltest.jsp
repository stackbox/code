<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="java.sql.*" %>
<%@ page import="java.util.*" %>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
</head>
<body>

<form action="select.jsp" action="post">
<p>查询<input type="text" name="sno"></p>
<input type="submit" value="submit">
</form>

<form action="addnew.jsp" action="post">
<p>add new sno:<input type="text" name="sno">
<p>sname:<input type="text" name="sname"></p>
<p>score:<input type="text" name="score"></p>
<input type="submit" value="add new">
</form>

</body>
</html>