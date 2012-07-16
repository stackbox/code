/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package src;
import static net.mindview.util.Print.print;
/**
 *
 * @author Administrator
 */
public class AutoInc {
    public static void main(String[] args)
    {
        int i = 1;
        print("i++ : " + (i++));
        print("i : " + i);
        print("++i : " + (++i));
        print("i : " + i);
        print("i-- : " + (i--));
        print("i : " + i);
        print("--i : " + (--i));
        print("i : " + i);
        
        
    }
}
