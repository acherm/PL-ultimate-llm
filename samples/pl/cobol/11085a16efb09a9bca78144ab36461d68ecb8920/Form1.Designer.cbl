       class-id. Form1 as "STARTPROG.Form1" is partial
                 inherits type "System.Windows.Forms.Form".
                 
       environment division.
       configuration section.
       repository.
      
       object.
       working-storage section.
       01 components type "System.ComponentModel.IContainer".
      
      *> Required method for Designer support - do not modify
      *> the contents of this method with the code editor.
       method-id. "InitializeComponent" private.
       procedure division.
           set components to new "System.ComponentModel.Container"()
           set self::"Text" to "Form1"
           set self::"Size" to new "System.Drawing.Size"(400, 400)
           goback.
       end method "InitializeComponent".

      *> Clean up any resources being used.      
       method-id. "Dispose" override protected.
       procedure division using by value disposing as condition-value.
           if disposing then
             if components not = null then
               invoke components::"Dispose"()
             end-if
           end-if
           invoke super::"Dispose"(by value disposing)
           goback.           
       end method "Dispose".

       end object.
       end class Form1.
