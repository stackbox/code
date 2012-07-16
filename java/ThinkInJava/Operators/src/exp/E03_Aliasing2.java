/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package exp;
import java.util.*;
import static net.mindview.util.Print.*;
/**
 *
 * @author Administrator
 */
public class E03_Aliasing2 {
    static void fun(Integral a)
    {
        a.f = 2222.0f;
    }
    public static void main(String[] args)
    {
        Integral t = new Integral();
        t.f = 0.0f;
        print("t.f = " + t.f);
        fun(t);
        print("t.f = " + t.f);
    }
}
