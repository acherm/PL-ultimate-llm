INPUT customer_file
  USING customer_id
  READ customer_name, customer_balance

REPORT customer_report
  TITLE "Customer Balance Report"
  HEADING "Customer Listing"

  DETAIL
    PRINT customer_id, customer_name, customer_balance

  TOTAL
    SUM customer_balance GIVING total_balance
    PRINT "Total Balance:", total_balance

END REPORT