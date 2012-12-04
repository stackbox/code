/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author nonassoc
 */
public class Josephus {
	static int getLast(int m,int n) {
		int s=0,i;
		for(i=2; i <= m; i++)
			s = (s+n)%i;
		return  s;
	}
	public static void main(String[] args) {
		System.out.println(getLast(500,3));
	}
}
