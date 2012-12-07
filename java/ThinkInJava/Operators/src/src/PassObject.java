
 * and open the template in the editor.
 */
package src;
import static net.mindview.util.Print.*;

/**
 *
 * @author Administrator
 */
class Letter {
    char c;
}

public class PassObject {
    static void f(Letter y) {
        y.c = 'z';
    }
    public static void main(String[] args) {
        Letter x = new Letter();
        x.c = 'a';
        print("1: x.c: " + x.c);
        f(x);
        print("2: x.c: " + x.c);
    }
}
