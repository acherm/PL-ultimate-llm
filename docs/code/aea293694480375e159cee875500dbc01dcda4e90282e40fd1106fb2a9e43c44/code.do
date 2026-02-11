/*******************************************************************************
1_dataprep.do

This do file prepares the data for the analysis.

The code is divided into the following sections:

	1. Load data and define globals
	2. Generate variables
	3. Clean data
	4. Save data

*******************************************************************************/

clear all
set more off

/*******************************************************************************
1. Load data and define globals
*******************************************************************************/

* Define globals
global data "https://www.dropbox.com/s/95x6h23s32a7gff/deleeckereekhout_20170120.dta?dl=1"
global results "../Results"
global figures "../Figures"
global tables "../Tables"

* Load data
use $data, clear

/*******************************************************************************
2. Generate variables
*******************************************************************************/

* Generate year fixed effects
tab year, gen(yd)

* Generate industry fixed effects
tab ffi48, gen(id)

* Generate log sales
gen logsales = log(sale)

* Generate log assets
gen logassets = log(at)

* Generate log capital
gen logcapital = log(ppent)

* Generate log market value
gen logmktval = log(mktval)

* Generate log number of employees
gen logemp = log(emp)

* Generate investment rate
gen invrate = capx/ppent

* Generate cash flow
gen cashflow = (ib+dp)/ppent

* Generate Tobin's Q
gen q = (mktval+dltt-ceq)/at

* Generate leverage
gen leverage = (dlc+dltt)/at

/*******************************************************************************
3. Clean data
*******************************************************************************/

* Drop if missing sales, assets, capital, or cost of goods sold
drop if sale==. | at==. | ppent==. | cogs==.

* Drop if sales, assets, or capital are non-positive
drop if sale<=0 | at<=0 | ppent<=0

* Drop if cost of goods sold is negative
drop if cogs<0

* Drop financials and utilities
drop if ffi48==49 | (ffi48>=44 & ffi48<=48)

* Drop if investment rate is in the top or bottom 1%
sum invrate, d
drop if invrate>r(p99) | invrate<r(p1)

* Drop if cash flow is in the top or bottom 1%
sum cashflow, d
drop if cashflow>r(p99) | cashflow<r(p1)

* Drop if Tobin's Q is in the top or bottom 1%
sum q, d
drop if q>r(p99) | q<r(p1)

* Drop if leverage is in the top or bottom 1%
sum leverage, d
drop if leverage>r(p99) | leverage<r(p1)

/*******************************************************************************
4. Save data
*******************************************************************************/

saveold ../Data/deleeckereekhout_20170120_clean.dta, version(12) replace