⍝ Statistical Functions in APL
⍝ Calculate mean, sum, and standard deviation

      DATA ← 23 45 67 12 89 34 56 78

      ⍝ Calculate the average (mean)
      AVG ← (+/DATA) ÷ ⍴DATA

      ⍝ Display the average
      'Average: ', ⍕AVG

      ⍝ Calculate sum
      SUM ← +/DATA
      'Sum: ', ⍕SUM

      ⍝ Calculate standard deviation
      VARIANCE ← (+/(DATA - AVG)*2) ÷ ⍴DATA
      STDDEV ← VARIANCE * 0.5
      'Standard Deviation: ', ⍕STDDEV