<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ page import="java.sql.*" %>
<%@ page import="java.util.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>
<%
try {
Class.forName("com.mysql.jdbc.Driver");
} catch(Exception e){}

String url="jdbc:mysql://localhost:3306/java";
String user="root";
String password="123456";
Connection conn=null;
String sno=request.getParameter("sno");
try {
	conn=DriverManager.getConnection(url,user,password);
	Statement stmt=conn.createStatement();
	String sql="SELECT * FROM stu WHERE sno="+sno;//表名book
	ResultSet rs = stmt.executeQuery(sql);
	
	
	while(rs.next()) {
		String snumber=rs.getString("sno");
		String name=rs.getString("sname");
		int sco=rs.getInt("score");
		out.println("sno:"+snumber+"<br>sname:"+name+"<br>score:"+sco+"<br>");
	}
	
	rs.close();
	stmt.close();
	//stmt.execute(sql);
} catch(Exception e)
{
	out.println("error:"+e.toString());
} finally {
	try {
		if(conn != null) conn.close();
	} catch(Exception e){}
}
%>
</body>
</html>