<%@ page language="java" contentType="text/html; charset=GB2312"
    pageEncoding="GB2312"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%
String str=request.getParameter("submit");
if(str==null) {
	str="";
}
if (str.equals("yes")){
	response.reset();
	 response.setContentType("application/msword;charset=GB2312");
	 response.setHeader("Content-Disposition", "inline;filename=temp.doc");
	}
%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=GB2312">
<title>Insert title here</title>
</head>
<body>
<p>save as msword</p>
<form method="get" name="form">
<input type="submit" value="yes" name="submit">
</form>

</body>
</html>