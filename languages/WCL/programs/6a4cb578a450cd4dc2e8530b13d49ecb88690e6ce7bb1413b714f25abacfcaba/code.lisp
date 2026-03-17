;;; (C) Copyright 1990 - 2014 by Wade L. Hennessey. All rights reserved.

(defun beta (tree env)
  (unless (null tree)
    (typecase tree
      (seq (beta-seq tree env))
      (scope-control-transfer (beta-scope-control-transfer tree env))
      (unwind-protect (beta-unwind-protect tree env))
      (var-ref (beta-var-ref tree env))
      (var-def (beta-var-def tree env))
      (mvalues (beta-values tree env))
      (if (beta-if tree env))
      (switch (beta-switch tree env))
      (function-call (beta-function-call tree env))
      (control-point (beta-control-point tree env))
      (t tree))))
