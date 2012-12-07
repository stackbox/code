<%@ page language="java" contentType="text/html; charset=gb2312"
    pageEncoding="gb2312"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>Insert title here</title>
</head>
<body>
<%@ include file="static.html"%>

<jsp:include page="action.jsp" flush="true">
<jsp:param name="a1" value='<%=request.getParameter(\"name\")%>' />
<jsp:param name="a2" value='<%=request.getParameter(\"password\")%>' />
</jsp:include>




</body>
</html>