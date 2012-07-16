<%@ page language="java" contentType="text/html; charset=gb2312"
    pageEncoding="gb2312"%>
<%@ page import="java.util.*" %>
<%request.setCharacterEncoding("gb2312");%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>showing</title>
</head>
<body>
<%
Enumeration<?> enuxx = request.getParameterNames();
while (enuxx.hasMoreElements()) 
{String parameterName = (String) enuxx.nextElement();
String parameterValue = (String) request.getParameter(parameterName);
out.print("参数名称：" + parameterName + "<BR>");
out.print("参数内容：" + parameterValue + "<BR>");
}
%>
</body>
</html>