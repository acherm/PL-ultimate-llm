/**
 * @name Unused variable
 * @description Finds local variables that are never used
 * @kind problem
 * @problem.severity warning
 * @id java/unused-variable
 */

import java

from LocalVariableDecl v
where not exists(VarAccess va | va.getVariable() = v)
select v, "Variable " + v.getName() + " is never used."
