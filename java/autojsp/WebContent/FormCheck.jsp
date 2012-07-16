<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
</head>
<body>
<h2>使用过滤器校验表单数据：</h2>
 <form method="post" action="FormSuccess.jsp">
<table>
  <tr>
<td>姓名：</td>
<td><input name="name" type="text"></td>
  </tr>
  <tr>
<td>年龄：</td>
<td><input name="age" type="text"></td>
  </tr>
  <tr>
    <td></td>
    <td>
          <input name="submit" type="submit" value="提交">
          <input name="reset" type="reset" value="重置">
        </td>
  </tr>
</table>
  </form>
</body>
</html>