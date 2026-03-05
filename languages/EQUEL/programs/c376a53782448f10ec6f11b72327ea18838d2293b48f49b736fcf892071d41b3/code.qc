##  /*
##   * EQUEL example: retrieve employee records from INGRES database
##   */
##  main()
##  {
##      char    ename[20];
##      char    edept[20];
##      int     esalary;

##      ingres "personnel"

##      range of e is employee

        printf("Employees in Engineering:\n");

##      retrieve (ename  = e.name,
##                edept  = e.dept,
##                esalary = e.salary)
##          where e.dept = "Engineering"
##      {
            printf("  Name: %-20s  Salary: %d\n", ename, esalary);
##      }

##      exit
##  }
