package pack;

import java.io.*;
import javax.servlet.http.*;
import java.io.IOException;
import javax.servlet.Servlet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class SessionServlet
 */
public class SessionServlet extends HttpServlet implements Servlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public SessionServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doPost(request,response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		
		response.setContentType("text/html;charset=gb2312");
		PrintWriter out = response.getWriter();
		out.println("<html><head>");
		out.println("<title>HttpSession Servlet" +"</title>");
		out.println("</head><body>");
		
		HttpSession session = request.getSession();
		
		Boolean isLogin = (Boolean)session.getAttribute("isLogin");
		
		if(isLogin == null) {
			isLogin = Boolean.FALSE;
		}
		String user = request.getParameter("user");
		String password = request.getParameter("pass");
		
		if (isLogin.booleanValue()) {
			// 从会话对象中读取数据
			user = (String) session.getAttribute("user");
			out.println("<h2>欢迎您，" + user + "！</h2>");
		} else if ((user != null) && (password != null)) {
				// 在会话对象中保存数据
			session.setAttribute("user", user);
			session.setAttribute("isLogin", Boolean.TRUE);
			out.println("<h2>欢迎您，" + user + "！</h2>");
				} 
		else {
		out.println("<h2>请在下面输入登录信息</h2>");
		out.println("<form method=\"post\" action=\"SessionServlet\">");
		out.println("<table>");
		out.println("<tr>");
		out.println("<td>用户名：</td>");
		out.println("<td><input name=\"user\" type=\"text\"></td>");
		out.println("</tr>");
		out.println("<tr>");
		out.println("<td>密码：</td>");
		out.println("<td><input name=\"pass\" type=\"password\"></td>");
		out.println("</tr>");
		out.println("<tr>");
		out.println("<td></td>");
		out.println("<td><input name=\"ok\" type=\"submit\" value=\"确定\"></td>");
		out.println("</tr>");
		out.println("</table>");
		out.println("</form>");
		out.println("</body>");
		out.println("</html>");
		}

		
	}

}
