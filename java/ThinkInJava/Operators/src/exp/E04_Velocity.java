/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package exp;

/**
 *
 * @author Administrator
 */
public class E04_Velocity {
    public static void main(String[] args)
    {
        if(args.length < 2)
        {
            System.out.println("input error!");
            System.exit(1);
        }
        
        float distance = Float.parseFloat(args[0]);
        float time = Float.parseFloat(args[1]);
        float velocity = distance / time;
        System.out.println("velocity = " + velocity);
    }
}
