<body>
<%
out.println("rum from jspinclude.jsp");
%>
<br>
a1=
<%=request.getParameter("a1")%>
<br>
a2=
<%=request.getParameter("a2")%>
</body>