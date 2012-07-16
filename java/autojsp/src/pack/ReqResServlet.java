package pack;

import java.io.*;
import java.io.IOException;
import javax.servlet.Servlet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class ReqResServlet
 */
public class ReqResServlet extends HttpServlet implements Servlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ReqResServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		
		request.setCharacterEncoding("gb2312");
		response.setContentType("text/html;charset=gb2312");
		
		PrintWriter out = response.getWriter();
		out.println("<h3><br>客户使用的协议是:");
		out.println("request.getProtocol()");
		out.println("<br>客户提交信息的方式：");
		out.println(request.getMethod());
		out.println("<br>获取HTTP头文件中Host的值：");
		out.println(request.getHeader("Host"));
		out.println("<br>获取客户机的名称：");
		out.println(request.getRemoteHost()); 
		out.println("<br>获取客户的IP地址：");
		out.println(request.getRemoteAddr());
		out.println("<br>获取服务器的名称：");
		out.println(request.getServerName());
		out.println("<br>获取服务器的端口号：");
		out.println(request.getServerPort()); 
		out.println("</h3>"); 
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request,response);
	}

}
