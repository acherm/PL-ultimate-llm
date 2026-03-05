package jx.hello;

import jx.zero.*;
import jx.zero.debug.*;

/**
 * Hello World domain for JX operating system.
 * Demonstrates basic component structure and debug output.
 */
public class HelloWorld implements Runnable {

    public HelloWorld() {
    }

    public void run() {
        Debug.out.println("Hello, World!");
        Debug.out.println("Running inside the JX operating system.");
        Debug.out.println("JX is a Java-based component OS from Univ. Erlangen.");
    }
}
