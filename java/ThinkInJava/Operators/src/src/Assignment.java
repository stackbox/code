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

class Tank {
    int level;
}
public class Assignment {
    public static void main(String[] args)
    {
        Tank t1 = new Tank();
        Tank t2 = new Tank();
        t1.level = 9;
        t2.level = 47;
        
        print("1: t1.level: " + t1.level +", t2.level: " + t2.level);
        t1 = t2;
        print("2: t1.level: " + t1.level +", t2.level: " + t2.level);
        t1.level = 20;
        print("3: t1.level: " + t1.level +", t2.level: " + t2.level);
    }
}
