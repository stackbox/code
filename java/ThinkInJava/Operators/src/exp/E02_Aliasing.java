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

class Integral {
    float f;
}

public class E02_Aliasing {
    public static void main(String[] args)
    {
        Integral a = new Integral();
        Integral b = new Integral();
        a.f = 12.0f;
        b.f = 34.0f;
        print("a.f = " + a.f + ",b.f = " + b.f);
        a = b;
        print("a.f = " + a.f + ",b.f = " + b.f);
        a.f = 890.0f;
        print("a.f = " + a.f + ",b.f = " + b.f);


        
    }
}
