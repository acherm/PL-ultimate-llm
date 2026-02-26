/**
 * @name Classes that extend Thread
 * @description Finds all classes that directly extend java.lang.Thread
 * @kind problem
 * @problem.severity recommendation
 * @id java/extends-thread
 */

import java

from Class c
where c.getASupertype().hasQualifiedName("java.lang", "Thread")
select c, "This class directly extends Thread instead of implementing Runnable."
