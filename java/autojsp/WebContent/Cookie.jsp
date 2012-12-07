<%@ page language="java" contentType="text/html; charset=gb2312"
    pageEncoding="gb2312"%>
<%@ page import="javax.servlet.http.Cookie,java.util.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>cookie</title>
</head>
<body>
<%
Cookie[] cookies=request.getCookies();
Cookie cookie_response=null;
if(cookies==null)
	out.print("there is no cookie" + "<br>");
else {
	try {
		if (cookies.length == 0)
			{System.out.println("客户端禁止写入cookie");
			} else {
				for(int i=0; i <cookies.length; i++) {
					Cookie temp = cookies[i];
					if(temp.getName().equals("cookietest")) {
						cookie_response=temp;
						break;
					}
				}
			}
	}
	catch(Exception e) {
		System.out.println(e);
	}
}

out.println("nowtime:" + new java.util.Date() + "<br>");

if(cookie_response != null) {
	out.println(cookie_response.getName() + "last time:" + cookie_response.getValue());
	cookie_response.setValue(new Date().toString());
} else {
	out.print("first time ");
	cookie_response=new Cookie("cookietest", new java.util.Date().toString());
	out.println("create cookie");	
}

response.addCookie(cookie_response);
response.setContentType("text/html");
response.flushBuffer();

%>
</body>
</html>