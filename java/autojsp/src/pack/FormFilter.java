package pack;

import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.*;

/**
 * Servlet Filter implementation class FormFilter
 */
public class FormFilter implements Filter {

    /**
     * Default constructor. 
     */
    public FormFilter() {
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see Filter#destroy()
	 */
	public void destroy() {
		// TODO Auto-generated method stub
	}

	/**
	 * @see Filter#doFilter(ServletRequest, ServletResponse, FilterChain)
	 */
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		// TODO Auto-generated method stub
		// place your code here

		// pass the request along the filter chain
		
		
		String name=request.getParameter("name");
		String strAge=request.getParameter("age");
		int age;
		RequestDispatcher dispatcher =request.getRequestDispatcher("FormFail.jsp");
		
		if(name==null || strAge==null) {
			dispatcher.forward(request, response);
			return;
		}
		
		try {
			age = Integer.parseInt(strAge);
			if(age > 100 || age <0) {
				dispatcher.forward(request, response);
				return;
			}
		} catch (Exception e) {
			dispatcher.forward(request, response);
			return;
		}
		
		chain.doFilter(request, response);
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		// TODO Auto-generated method stub
	}

}
