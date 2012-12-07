<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
</head>
<body>
<h2>您提交的数据：</h2>
<form>
<table>
  <tr>
<td>姓名：</td>
<td>
  <input name="name" type="text" value=<%=request.getParameter("name")%> readonly="true">
</td>
  </tr>
  <tr>
<td>年龄：</td>
<td>
  <input name="age" type="text" value=<%=request.getParameter("age")%> readonly="true">
</td>
  </tr>
</table>
  </form>
  
  <h2><font color="#0000EE">输入数据没能通过过滤器的校验！</font></h2>
  
</body>
</html>