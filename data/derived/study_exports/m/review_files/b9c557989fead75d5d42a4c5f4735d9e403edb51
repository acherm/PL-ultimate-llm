(* Mathematica Package *)

(* Created by the Wolfram Workbench Jul 28, 2006 *)

(*
Created on 2006/07/28

Imported from
Z:\sites\chris.chiasson.name\Engineering_Optimization\pr3\Big_Rewrite.nb
*)

BeginPackage["EngineeringOptimization`",{"Utilities`FilterOptions`"}]

(* Exported symbols added here with SymbolName::usage *) 

FindMinimum::fdbh="The first unimodal line search hit its MaxDisplacement bound 
and did not find any points with a lower function value than the origin of the 
line search. The algorithm will move on to the second search.";
FindMinimum::fibh="The first unimodal line search hit its MaxIterations bound 
and did not find any points with a lower function value than the origin of the 
line search. The algorithm will move on to the second search.";
FindMinimum::fdbl="The first unimodal line search hit its MaxDisplacement bound,
 but did find at least one point with a lower function value than the origin
 of the line search. The point with the lowest value will be returned.";
FindMinimum::fibl="The first unimodal line search hit its MaxIterations bound,
 but did find at least one point with a lower function value than the origin
 of the line search. The point with the lowest value will be returned.";
FindMinimum::sdbh="The second unimodal line search hit its MaxDisplacement bound
 and did not find any points with a lower function value than the origin of the 
 line search. The algorithm will return the origin.";
FindMinimum::sibh="The second unimodal line search hit its MaxIterations bound 
and did not find any points with a lower function value than the origin of the 
line search. The algorithm will return the origin.";
FindMinimum::sdbl="The second unimodal line search hit its MaxDisplacement bound
, but did find at least one point with a lower function value than the origin
 of the line search. The point with the lowest value will be returned.";
FindMinimum::sibl="The second unimodal line search hit its MaxIterations bound,
 but did find at least one point with a lower function value than the origin
 of the line search. The point with the lowest value will be returned.";
General::badopts="Received bad options: `1`.";

Begin["`Private`"]
(* Implementation of the package *)

Off[NMinimize::"bdmtd",FindMinimum::"bdmtd"];
oldAttributesFindMinimum=Attributes[FindMinimum];
Unprotect[NMinimize,FindMinimum];
Update/@{NMinimize,FindMinimum};
Attributes[FindMinimum]={};

(*replacements*)
ruleSet=Rule->Set;

ruleDelayedSetDelayed=RuleDelayed->SetDelayed;

rulesSets={ruleSet,ruleDelayedSetDelayed};

(*vector means column vector*)
nonComplexNumberPatternObject=Map[Blank,Integer|Real|Rational];

unThreadableNonComplexNumberPatternObject={{nonComplexNumberPatternObject}}

multipleNonComplexNumberPatternObject={nonComplexNumberPatternObject..};

vectorNonComplexNumberPatternObject={{nonComplexNumberPatternObject}..};

matrixNonComplexNumberPatternObject={multipleNonComplexNumberPatternObject..};

constraintPatternObject=(Less|LessEqual|Greater|GreaterEqual|Equal)[__];

multipleConstraintPatternObject=(And|List)[constraintPatternObject..];

guessPseudoPatternObject={_,_?NumericQ};

multipleGuessPseudoPatternObject={guessPseudoPatternObject..};

guessRangePseudoPatternObject={_,_?NumericQ,_?NumericQ};

multipleGuessRangePseudoPatternObject={guessRangePseudoPatternObject..};

multipleExpressionPatternObject={Blank[]..};

vectorExpressionPatternObject={{Blank[]}..};

ruleHeadPatternObject=(Rule|RuleDelayed);

rulePatternObject=ruleHeadPatternObject[_,_];
(*rulePatternObject can't be limited to strings and symbols if you want to
handle general expressions as "variables"*)

methodRulePatternObject=ReplacePart[rulePatternObject,Method,1];

commonOptionsPatternObject=ReplacePart[rulePatternObject,DeleteCases[
	Alternatives@@Intersection@@Map[Options[#][[All,1]]&,
		{FindMinimum,NMinimize}],MaxIterations],1];

multipleRulePatternObject={rulePatternObject..};

sequenceRulePatternObject=rulePatternObject..;

multipleNullRulePatternObject={rulePatternObject...};

(*ruleStringLhsPatternObject=ruleHeadPatternObject[_String,_];

sequenceRuleStringLhsPatternObject=ruleStringLhsPatternObject..;*)

nonComplexNumberRulePatternObject=Rule[_,nonComplexNumberPatternObject];

multipleNonComplexNumberRulePatternObject={nonComplexNumberRulePatternObject..};

aLMMethodString="AugmentedLagrangeMultiplier";

aLMMethodRulePatternObject=
Method->aLMMethodString|{aLMMethodString,sequenceRulePatternObject};

vMMethodString="VariableMetric";

vMMethodRulePatternObject=
Method->vMMethodString|{vMMethodString,sequenceRulePatternObject};

sDMethodString="SteepestDescent";

sDMethodRulePatternObject=
Method->sDMethodString|{sDMethodString,sequenceRulePatternObject};

fRMethodString="FletcherReeves";

fRMethodRulePatternObject=
Method->fRMethodString|{fRMethodString,sequenceRulePatternObject};

fMCommonConvergenceTestPatternObject=
	{multipleNonComplexNumberRulePatternObject,
		vectorNonComplexNumberPatternObject,___}..;
	
vMMKernelConvergenceTestPatternObject=
	{multipleNonComplexNumberRulePatternObject,
		vectorNonComplexNumberPatternObject,
		matrixNonComplexNumberPatternObject}..;

multipleSymbolPatternObject={__Symbol};

(*may be unneeded now*)
multipleOptionPseudoPatternObject={__?OptionQ};

uMethodString="Unimodal";

unTrueFalseSymbol=Except[True|False,_Symbol];

boundMinimumConvergenceTestPatternObject={nonComplexNumberPatternObject,
	nonComplexNumberPatternObject,
	nonComplexNumberPatternObject,
	nonComplexNumberPatternObject,
	nonComplexNumberPatternObject,
	nonComplexNumberPatternObject}..;

(*argument debugging*)

defineBadArgs[symbol_Symbol]:=Module[{args},symbol[args__]:=(Message[
	General::badargs,symbol,HoldForm[symbol[args]]];Abort[])];

defineDebugArgs[symbol_Symbol]:=Module[{args,debugString,debugSymbol,result,
	rules},rules={debugString->"debug`"<>SymbolName[symbol]};
	AppendTo[rules,debugSymbol->ToExpression[debugString/.rules]];
	result=ReleaseHold[Hold[symbol[args__]:=Dialog[DialogProlog:>Print[
		debugString],DialogSymbols:>{debugSymbol=Hold[symbol[args]]}]]/.rules];
	If[MatchQ[{result},{$Failed}],Abort[],result]];

ruleNumeric[workingPrecision:(_?NumericQ|MachinePrecision):MachinePrecision]:=
	Module[{rule},rule:rulePatternObject:>rule[[0]][rule[[1]],N[rule[[2]],
		workingPrecision]]]

defineBadArgs@ruleNumeric;

ruleLhsUnion[rules___]:=
	Sequence@@Module[{encounteredLhses=Alternatives[],Lhs,rule,ruleParser},
	ruleParser[Pattern[rule,ruleHeadPatternObject[Lhs_,_]]]:=
		If[MatchQ[Lhs,encounteredLhses],
			Unevaluated[Sequence[]],
			AppendTo[encounteredLhses,Lhs];rule];
	ruleParser/@{rules}];

defineBadArgs@ruleLhsUnion;

(*options are not optional for monitorRules - lol - if options are not passed, 
there is no reason to call this function - it only serves to execute delayed
monitoring expressions*)

Options@parseOptions={excludedOptions->{}};

parseOptions[argumentOptionList:multipleNullRulePatternObject,
	optionSymbolList:multipleSymbolPatternObject,opts___?OptionQ]:=
	Module[{option,excludedOptionsAlternatives=Alternatives@@Flatten@
		{ReplaceAll[excludedOptions/.{opts},Options@parseOptions]}},
		Sequence@@DeleteCases[Join[argumentOptionList,Sequence@@@
			(Options/@optionSymbolList)],option:excludedOptionsAlternatives]];

defineBadArgs@parseOptions;

monitorRules[variables:multipleExpressionPatternObject,
spotRules:multipleNonComplexNumberRulePatternObject,monitor_,opts__?OptionQ]:=
	CompoundExpression[Block[variables,Set@@@spotRules;monitor/.{opts}],
		spotRules];

defineBadArgs@monitorRules;

Options@optionsListValidQ={excludedOptions->{}};

optionsListValidQ[optionsCheckSymbol_Symbol,
	optionPossibleList:multipleNullRulePatternObject,opts___?OptionQ]:=
	Module[{option,excludedOptionsAlternatives=
		Alternatives@@Flatten@{ReplaceAll[excludedOptions/.{opts},
			Options@optionsListValidQ]}},
		If[MatchQ[optionPossibleList[[All,1]],
				{Alternatives@@
					DeleteCases[Options[optionsCheckSymbol][[All,1]],
						option:excludedOptionsAlternatives]...
					}
				],
			True,
			Message[optionsCheckSymbol::"badopts",
				optionPossibleList[[All,1]]
				];
			Abort[]
			]
		];

defineBadArgs@optionsListValidQ;

frameMinimum[function_,variable_,
	functionStart:nonComplexNumberPatternObject,
	solutionStart:nonComplexNumberPatternObject,
	functionIntermediate:nonComplexNumberPatternObject,
	solutionIntermediate:nonComplexNumberPatternObject,
	functionEnd:nonComplexNumberPatternObject,
	solutionEnd:nonComplexNumberPatternObject,
	growthFactor:nonComplexNumberPatternObject,
	solutionStartBound:nonComplexNumberPatternObject,
	solutionEndBound:nonComplexNumberPatternObject,opts__?OptionQ]:=
	Module[{displacements,solutionTemp1=(1+growthFactor)*solutionEnd-
		growthFactor*solutionStart,solutionTemp2},
		displacements=Abs[{solutionTemp1,solutionEndBound}-
			solutionStartBound];
		solutionTemp2=First@Pick[{solutionTemp1,solutionEndBound},
			displacements,Min@displacements];
		{functionIntermediate,solutionIntermediate,functionEnd,solutionEnd,
			function/.monitorRules[{variable},{variable->
				solutionTemp2},EvaluationMonitor,opts],solutionTemp2}];

defineBadArgs@frameMinimum;

(*frameMinimumStopTest must have Or Applied to List rather than wrapping the
arguments directly in Or because all three Stop conditions must be assigned*)

frameMinimumStopTest[functionStart:nonComplexNumberPatternObject,
	solutionStart:nonComplexNumberPatternObject,
	functionIntermediate:nonComplexNumberPatternObject,
	solutionIntermediate:nonComplexNumberPatternObject,
	functionEnd:nonComplexNumberPatternObject,
	solutionEnd:nonComplexNumberPatternObject,
	solutionEndBound:nonComplexNumberPatternObject,
	frameBound_Symbol,
	domainBound_Symbol,iteration_Integer,
	maxIterations_Integer,iterationBound_Symbol]:=
	If[Or@@{If[functionEnd>functionIntermediate,frameBound=True,False],
		If[solutionEnd===solutionEndBound,domainBound=True,False],
		If[iteration>=maxIterations,iterationBound=True,False]},True,False];

frameMinimumStopTest[blah___]:=Dialog[
	DialogProlog:>Print["debug`frameMinimumStopTest"],
	DialogSymbols:>{debug`frameMinimumStopTest={blah}}];

defineBadArgs@frameMinimumStopTest;

frameMinimumBoundMessages[domainBound_Symbol,dbtag_Symbol,
	iterationBound_Symbol,ibtag_Symbol]:=Block[{Message,MessageName},
		{If[domainBound,Message@MessageName[FindMinimum,SymbolName@dbtag]],
		If[iterationBound,Message@MessageName[FindMinimum,SymbolName@ibtag]]}];	
	
defineBadArgs@frameMinimumBoundMessages;

noValueFalse[symbol:unTrueFalseSymbol]:=If[!ValueQ@symbol,symbol=False];

noValueFalse[symbol_Symbol]:=symbol;

defineBadArgs@noValueFalse;

selectMinimum[variable_Symbol,
	frame:multipleNonComplexNumberPatternObject]:=Module[{
		partitionedFrame=Partition[frame, 2],
		partitionedFrameFunctionValues},
		partitionedFrameFunctionValues=partitionedFrame[[All,1]];
		MapAt[{variable->#}&,First@Sort@Pick[partitionedFrame,
			partitionedFrameFunctionValues,
			Min@partitionedFrameFunctionValues],2]];

defineBadArgs@selectMinimum;

frameMinimumNarrow[function_,variable_,
	functionStart:nonComplexNumberPatternObject,
	solutionStart:nonComplexNumberPatternObject,
	functionIntermediate1:nonComplexNumberPatternObject,
	solutionIntermediate1:nonComplexNumberPatternObject,
	functionIntermediate2:nonComplexNumberPatternObject,
	solutionIntermediate2:nonComplexNumberPatternObject,
	functionEnd:nonComplexNumberPatternObject,
	solutionEnd:nonComplexNumberPatternObject,
	shrinkFactor:nonComplexNumberPatternObject,
	opts__?OptionQ]:=Module[{solutionIntermediateNew},If[
		functionIntermediate1>functionIntermediate2,
		solutionIntermediateNew=shrinkFactor*solutionIntermediate1+
			(1-shrinkFactor)*solutionEnd;
		{functionIntermediate1,solutionIntermediate1,functionIntermediate2,
			solutionIntermediate2,function/.monitorRules[{variable},{variable->
				solutionIntermediateNew},EvaluationMonitor,opts],
			solutionIntermediateNew,functionEnd,solutionEnd},
		solutionIntermediateNew=(1-shrinkFactor)*solutionStart+
			shrinkFactor*solutionIntermediate2;
		{functionStart,solutionStart,function/.monitorRules[{variable},
			{variable->solutionIntermediateNew},EvaluationMonitor,opts],
			solutionIntermediateNew,functionIntermediate1,solutionIntermediate1,
			functionIntermediate2,solutionIntermediate2}]];

defineBadArgs@frameMinimumNarrow;

(*The file loaded here defines a function, cubicCriticalDomainLocations, which
is a function of four points y1,x1,y2,x2,y3,x3,y4,x4 (function value before
domain value). The outputs are a list of two critical (in the calculus senese)
domain locations (x values) obtained from a cubic polynomial fit through the
four given points. The reason the file is loaded this way is that the
function was (time consumingly) generated from other Mathematica input and would
otherwise be prone to copy/paste error*)

Get[StringReplace[Context[],{"`"->"","Private"->""}]<>
	"/cubicCriticalDomainLocations.m"];

defineBadArgs@cubicCriticalDomainLocations;

(*reFindMinimum is used to call FindMinimum from itself, often because the frame
search needs to go in a negative direction. Since the algorithm does not work
when moving the frame in a negative directory, reFindMinimum aliases the
independant variable using Block so that the search frame will always move in
the positive direction. Since Block is used, reports from StepMonitor and
EvaluationMonitor give the correct coordinates (including those from controling
routines like ALMFindMinimum) even though the FindMinimum
routine is working with the negative of the independant variable. It also
handles the oddball case of the displacement limit being equal to zero.*)

(*given the value of maxDisplacement and MaxIterations on an initial call, it
may be possible to work out precisely how many iterations are possible for each
run - and instead of passing extra information, use the length of
MaxDisplacement to normalize however many iterations are left - we'll see*)

reFindMinimum[function_,variable_,
	origin:nonComplexNumberPatternObject,
	maxDisplacement:multipleNonComplexNumberPatternObject,
	{methodOptions___?OptionQ},{opts___?OptionQ}]:=
	Module[{num,
		reverseNeeded=If[Negative[maxDisplacement[[1]]],True,False],
		variableReverse},
		If[reverseNeeded,Block[{variable=-variableReverse},Block[{FindMinimum},
			FindMinimum[function,{variableReverse,-origin},opts,Method->
				{uMethodString,"MaxDisplacement"->-maxDisplacement,
				methodOptions}]]]/.{Rule[variableReverse,num:
					nonComplexNumberPatternObject]->Rule[variable,-num]},
			Block[{FindMinimum},FindMinimum[function,{variable,-origin},opts,
				Method->{uMethodString,"MaxDisplacement"->maxDisplacement,
				methodOptions}]]]];

defineBadArgs@reFindMinimum;

Options@FindMinimum`Unimodal={"MaxDisplacement"->{100,-100},"GrowthFactor"->
	GoldenRatio,"ShrinkFactor"->2-GoldenRatio,"MaxNarrowingIterations"->12};

FindMinimum[function_,variableStart:guessPseudoPatternObject,
	opts1___?OptionQ,Method->uMethodString|
		{uMethodString,methodOptions__?OptionQ},
	opts2___?OptionQ]/;optionsListValidQ[FindMinimum,{opts1,opts2},
		excludedOptions->Method]&&optionsListValidQ[FindMinimum`Unimodal,
		{methodOptions}]:=
	Module[{boundDivisor=3,boundForward,boundOrigin,
		case,criticalDomainLocations,domainBound,frameBound,frame,
		functionOrigin,growthFactor,iterationBound,iterations,lowerList,
		maxDisplacementList,maxIterations,options,recursable,sewingTag,
		shrinkFactor,solutionIntermediate,variable=variableStart[[1]],
		workingPrecision},First@Sort@Reap[
		options=parseOptions[{methodOptions,opts1,opts2},
			{FindMinimum`Unimodal,FindMinimum}];
		workingPrecision=WorkingPrecision/.{options};
		boundOrigin=N[variableStart[[2]],workingPrecision];
		maxDisplacementList=Flatten@{N["MaxDisplacement"/.{options}
			,workingPrecision]};
		recursable=If[Length[maxDisplacementList]>=2,True,False];
		Which[Negative[maxDisplacementList[[1]]],
			Sow[reFindMinimum[function,variable,boundOrigin,maxDisplacementList,
				{methodOptions},{opts1,opts2}],sewingTag],
(*the combination of the first condition and these two proceeding conditions
 means that maxDisplacementList[[1]] would need to be == 0 for execution*)
			NonPositive[maxDisplacementList[[1]]]&&recursable,
			Sow[reFindMinimum[function,variable,boundOrigin,
				Drop[maxDisplacementList,1],{methodOptions},{opts1,opts2}],
				sewingTag],
			NonPositive[maxDisplacementList[[1]]]&&Not@recursable,
			Sow[selectMinimum[variable,{functionOrigin,boundOrigin}],
				sewingTag],
			True,
			maxIterations=MaxIterations/.{options};
			growthFactor=N["GrowthFactor"/.{options},workingPrecision];
			shrinkFactor=N["ShrinkFactor"/.{options},workingPrecision];
			boundForward=maxDisplacementList[[1]]+boundOrigin;
			iterations=0;
			++iterations;
			functionOrigin=function/.monitorRules[{variable},{variable->
				boundOrigin},EvaluationMonitor,options];
(*first frame*)
			solutionIntermediate=boundOrigin+maxDisplacementList[[1]]
				/boundDivisor;
			frame={functionOrigin,boundOrigin,functionOrigin,boundOrigin,
				function/.monitorRules[{variable},{variable->
				solutionIntermediate},EvaluationMonitor,options],
				solutionIntermediate};
(*attempt to frame the minimum*)
			frame=NestWhile[Apply[frameMinimum[function,variable,##,
				growthFactor,boundOrigin,boundForward,options]&,#]&,frame,
				Apply[Not@frameMinimumStopTest[##,boundForward,frameBound,
					domainBound,++iterations,IntegerPart[maxIterations/3],
					iterationBound]&,#]&];
			lowerList=(#<functionOrigin&)/@frame[[{1,3,5}]];
			noValueFalse/@{frameBound,domainBound,iterationBound};
(*was the minimum framed? if not, attempt contengencies*)
			Which[Not@frameBound&&Not[Or@@lowerList]&&recursable,
				frameMinimumBoundMessages[domainBound,fdbh,iterationBound,fibh];
				Sow[reFindMinimum[function,variable,boundOrigin,
					Drop[maxDisplacementList,1],{methodOptions},{opts1,opts2}]
					,sewingTag],
				Not@frameBound&&Not[Or@@lowerList]&&Not@recursable,
				frameMinimumBoundMessages[domainBound,sdbh,iterationBound,sibh];
				Sow[selectMinimum[variable,{functionOrigin,boundOrigin}],
					sewingTag],
				Not@frameBound&&Or@@lowerList,
				frameMinimumBoundMessages[domainBound,fdbl,iterationBound,fibl];
				Sow[selectMinimum[variable,frame],sewingTag],
				frameBound,		
(*the framebound&&Not@@lowerlist is a necessary but insufficient condition for
 the unimodal minimum to be in the other direction*)
				If[Not[Or@@lowerList]&&recursable,
					Sow[reFindMinimum[function,variable,boundOrigin,
						Drop[maxDisplacementList,1],
						{methodOptions},{opts1,opts2}]
					,sewingTag]];
(*if the minimum was framed, narrow the frame*)
				frame=Flatten@{frame[[{1,2}]],Map[{function/.monitorRules[
					{variable},{variable->#},EvaluationMonitor,options],#}&,
					{{1-shrinkFactor,shrinkFactor},{shrinkFactor,
						1-shrinkFactor}}.frame[[{2,6}]]],frame[[{5,6}]]};
				frame=FixedPoint[Apply[frameMinimumNarrow[function,variable,##,
					shrinkFactor,options]&,#]&,frame,
					Min["MaxNarrowingIterations"/.{options},maxIterations
						-iterations-2]];
(*fit a polynomail to the frame and see if any critical points are inside*)
				Block[{Message},
					criticalDomainLocations=Cases[
						cubicCriticalDomainLocations@@
							Rationalize[frame,0],
						case:nonComplexNumberPatternObject/;
							Function[Less[#1,case,#2]]@@Sort[{frame[[2]],
								frame[[8]]}]
						]
					];
(*if so, add them to the frame*)
				frame=Flatten@{frame,Map[{function/.monitorRules[{variable},
					{variable->#},EvaluationMonitor,options],#}&,
					criticalDomainLocations]};
(*choose the minimum point in the frame*)
				Sow[selectMinimum[variable,frame],sewingTag]]]
		,sewingTag][[2,1]]];
		
lineSearchRules[solutionRules:multipleNonComplexNumberRulePatternObject,
	searchDirection:multipleNonComplexNumberPatternObject,displacement_Symbol]:=
	MapThread[Function[{variableRule,searchDirectionComponent},
		MapAt[#+searchDirectionComponent*displacement&,variableRule,2]],
		{solutionRules,searchDirection}]

defineBadArgs@lineSearchRules;

singleElementScalar[singleElement:unThreadableNonComplexNumberPatternObject]:=
	First@First@singleElement;

defineBadArgs@singleElementScalar;

(*theta is the parameter that scales the hessian or inverse hessian update
between the Davidon Fletcher Powell (DFP) and Broyden Fletcher Goldfarb Shanno
(BFGS) methods on an interval of zero (DFP) to one (BFGS)*)
(*gamma,sigma, and tau are temporary variables that make the formulas
easier to write and probably faster to calculate*)
(*the p (displacementVector) and y (gradientChange) comments in the margin
 indicate the names of the variables as they appear in Garret N. Vanderplaats'
 Numerical Optimization Techniques for Engineering Design*)

unprotectedSymbols[variables:multipleExpressionPatternObject]:=
	Module[{symbol},
		Union@Reap[variables/.
			symbol_Symbol/;
				FreeQ[Attributes@symbol,Protected]:>
					Sow[symbol]
			][[2,1]]
		];

defineBadArgs@unprotectedSymbols;

vMMKernel[function_,variables:multipleExpressionPatternObject,
	solutionRules:multipleNonComplexNumberRulePatternObject,
	gradientSymbolic:vectorExpressionPatternObject,
	gradientNumeric:vectorNonComplexNumberPatternObject,
	inverseHessianApproximation:matrixNonComplexNumberPatternObject,
	opts___?OptionQ]:=Module[{displacement,displacementRule,displacementVector,
		findMinimumOptions,gradientChange,gradientNumericNew,
		inverseHessianApproximationNew,searchDirection,solutionRulesNew,gamma,
		sigma,tau,theta="Theta"/.{opts}},
		searchDirection=-inverseHessianApproximation.gradientNumeric;
		solutionRulesNew=lineSearchRules[solutionRules,
			Sequence@@@searchDirection,displacement];
		findMinimumOptions=ruleLhsUnion@FilterOptions[FindMinimum,
			Sequence@@Cases[{opts},Except[vMMethodRulePatternObject,
				commonOptionsPatternObject]]];
		displacementRule=(Block[Evaluate[unprotectedSymbols@variables],
			solutionRulesNew/.rulesSets;
			Block[{FindMinimum},FindMinimum[function,
				{displacement,0},findMinimumOptions]]])[[2]];
		If[(displacement/.displacementRule)===0.,
			gradientNumericNew=gradientNumeric;
				solutionRulesNew=solutionRules,
			solutionRulesNew=solutionRulesNew/.displacementRule;
				gradientNumericNew=gradientSymbolic/.solutionRulesNew;
(*p*)			displacementVector=Map[List,solutionRulesNew[[All,2]]
					-solutionRules[[All,2]]];
(*y*)			gradientChange=gradientNumericNew-gradientNumeric;
				sigma=Transpose[displacementVector].gradientChange
					//singleElementScalar;
				tau=Transpose[gradientChange].inverseHessianApproximation.
					gradientChange//singleElementScalar;
				gamma=inverseHessianApproximation.gradientChange;
				inverseHessianApproximationNew=inverseHessianApproximation+
					(sigma+theta*tau)/sigma^2*
						displacementVector.Transpose[displacementVector]+
					(theta-1)/tau*gamma.Transpose[gamma]-
					theta/sigma*(gamma.Transpose[displacementVector]+
						displacementVector.Transpose[gamma])];		
		{solutionRulesNew,gradientNumericNew,inverseHessianApproximationNew}];

defineBadArgs@vMMKernel;

(*I want this convergence to generate a message if solutionRules indexes
 a part of {arguments} that doesn't exist, so I am not putting a condition
 here on solutionRules - Chris Chiasson 2006-08-01*)
 
fMCommonConvergenceTest[variables:multipleExpressionPatternObject,
	arguments:fMCommonConvergenceTestPatternObject]:=
	Module[{solutionRules,solution},
		solutionRules[solution_Integer]:={arguments}[[solution,1]];
		SameQ[variables/.solutionRules[1],variables/.solutionRules[2]]];

defineBadArgs@fMCommonConvergenceTest;

fMSubMethodDefaultOption=Method->{uMethodString,
		"MaxDisplacement"->{12,-12},"MaxNarrowingIterations"->8};

Options@FindMinimum`VariableMetric={"Theta"->1,fMSubMethodDefaultOption};

FindMinimum[function_,variableStarts:multipleGuessPseudoPatternObject,
	opts1___?OptionQ,Method->vMMethodString|
		{vMMethodString,methodOptions__?OptionQ},
	opts2___?OptionQ]/;optionsListValidQ[FindMinimum,{opts1,opts2},
		excludedOptions->Method]&&optionsListValidQ[FindMinimum`VariableMetric,
		{methodOptions}]:=
	Module[{gradient,options,solutionRules,variables=variableStarts[[All,1]]},
		options=parseOptions[{methodOptions,opts1,opts2},
			{FindMinimum`VariableMetric,FindMinimum}];
		gradient=List/@D[function,{variables,1}];
		solutionRules=Rule@@@variableStarts;
		solutionRules=NestWhile[Apply[vMMKernel[function,variables,#1,gradient,
			#2,#3,options]&,#]&,
			{solutionRules,gradient/.solutionRules,
				IdentityMatrix[Length[variableStarts]]},
			Not@fMCommonConvergenceTest[variables,##]&,2,
			MaxIterations/.{options}][[1]];
		{function/.solutionRules,solutionRules}];

sDKernel[function_,variables:multipleExpressionPatternObject,
	solutionRules:multipleNonComplexNumberRulePatternObject,
	gradientSymbolic:vectorExpressionPatternObject,
	gradientNumeric:vectorNonComplexNumberPatternObject,
	opts___?OptionQ]:=Module[{displacement,displacementRule,displacementVector,
		findMinimumOptions,gradientChange,gradientNumericNew,
		searchDirection,solutionRulesNew},
		searchDirection=-gradientNumeric;
		solutionRulesNew=lineSearchRules[solutionRules,
			Sequence@@@searchDirection,displacement];
		findMinimumOptions=ruleLhsUnion@FilterOptions[FindMinimum,
			Sequence@@Cases[{opts},Except[sDMethodRulePatternObject,
				commonOptionsPatternObject]]];
		displacementRule=Block[Evaluate[unprotectedSymbols@variables],
			solutionRulesNew/.rulesSets;
			Block[{FindMinimum},FindMinimum[function,
				{displacement,0},findMinimumOptions]]][[2]];
		solutionRulesNew=solutionRulesNew/.displacementRule;
		gradientNumericNew=gradientSymbolic/.solutionRulesNew;
		{solutionRulesNew,gradientNumericNew}];

defineBadArgs@sDKernel;

Options@FindMinimum`SteepestDescent={fMSubMethodDefaultOption};

FindMinimum[function_,
	variableStarts:multipleGuessPseudoPatternObject,
	opts1___?OptionQ,
	Method->sDMethodString|{sDMethodString,methodOptions__?OptionQ},
	opts2___?OptionQ]/;
		optionsListValidQ[FindMinimum,{opts1,opts2},excludedOptions->Method]&&
			optionsListValidQ[FindMinimum`SteepestDescent,{methodOptions}]:=
	Module[{gradient,options,solutionRules,variables=variableStarts[[All,1]]},
		options=parseOptions[{methodOptions,opts1,opts2},
			{FindMinimum`SteepestDescent,FindMinimum}];
		gradient=List/@D[function,{variables,1}];
		solutionRules=Rule@@@variableStarts;
		solutionRules=NestWhile[Apply[sDKernel[function,variables,#1,gradient,
			#2,options]&,#]&,
			{solutionRules,gradient/.solutionRules},
			Not@fMCommonConvergenceTest[variables,##]&,2,
			MaxIterations/.{options}][[1]];
		{function/.solutionRules,solutionRules}
		];

fRKernel[function_,variables:multipleExpressionPatternObject,
	solutionRules:multipleNonComplexNumberRulePatternObject,
	gradientSymbolic:vectorExpressionPatternObject,
	gradientNumeric:vectorNonComplexNumberPatternObject,
	searchDirectionOld:vectorNonComplexNumberPatternObject,
	beta:nonComplexNumberPatternObject,
	opts___?OptionQ]:=Module[{betaNew,displacement,displacementRule,
		displacementVector,findMinimumOptions,gradientChange,gradientNumericNew,
		searchDirection,solutionRulesNew},
		searchDirection=-gradientNumeric+beta*searchDirectionOld;
		solutionRulesNew=lineSearchRules[solutionRules,
			Sequence@@@searchDirection,displacement];
		findMinimumOptions=ruleLhsUnion@FilterOptions[FindMinimum,
			Sequence@@Cases[{opts},Except[fRMethodRulePatternObject,
				commonOptionsPatternObject]]];
		displacementRule=Block[Evaluate[unprotectedSymbols@variables],
			solutionRulesNew/.rulesSets;
			Block[{FindMinimum},FindMinimum[function,
				{displacement,0},findMinimumOptions]]][[2]];
		solutionRulesNew=solutionRulesNew/.displacementRule;
		gradientNumericNew=gradientSymbolic/.solutionRulesNew;
		betaNew=Transpose[gradientNumericNew].gradientNumericNew/
			Transpose[gradientNumeric].gradientNumeric//singleElementScalar;
		{solutionRulesNew,gradientNumericNew,searchDirection,betaNew}];

defineDebugArgs@fRKernel;

(*http://www.library.cornell.edu/nr/bookcpdf/c10-6.pdf*)

Options@FindMinimum`FletcherReeves={fMSubMethodDefaultOption};

FindMinimum[function_,
	variableStarts:multipleGuessPseudoPatternObject,
	opts1___?OptionQ,
	Method->fRMethodString|{fRMethodString,methodOptions__?OptionQ},
	opts2___?OptionQ]/;
		optionsListValidQ[FindMinimum,{opts1,opts2},excludedOptions->Method]&&
			optionsListValidQ[FindMinimum`FletcherReeves,{methodOptions}]:=
	Module[{gradient,options,solutionRules,variables=variableStarts[[All,1]]},
		options=parseOptions[{methodOptions,opts1,opts2},
			{FindMinimum`FletcherReeves,FindMinimum}];
		gradient=List/@D[function,{variables,1}];
		solutionRules=Rule@@@variableStarts;
		solutionRules=NestWhile[Apply[fRKernel[function,variables,#1,gradient,
			##2,options]&,#]&,
			{solutionRules,
				gradient/.solutionRules,
				Table[{0},{Length@variables}],
				0},
			Not@fMCommonConvergenceTest[variables,##]&,2,
			MaxIterations/.{options}][[1]];
		{function/.solutionRules,solutionRules}
		];

aLMKernel[function_,variables:multipleExpressionPatternObject,
	solutionRules:multipleNonComplexNumberRulePatternObject,
	penalties:multipleExpressionPatternObject,
	penaltyMultiplierRule:Rule[penaltyMultiplier_Symbol,
		nonComplexNumberPatternObject],
	penaltyMultiplierGrowthFactor:nonComplexNumberPatternObject,
	lagrangeMultiplierRules:multipleNonComplexNumberRulePatternObject,
	lagrangeMultiplierUpdates:multipleExpressionPatternObject,opts___?OptionQ]:=
	Module[{case,constraintRateMultiplierRule=
		constraintRateMultiplierContainer->(ReplaceAll[#,solutionRules]&),
		findMinimumOptions=ruleLhsUnion@FilterOptions[FindMinimum,
			Sequence@@Cases[{opts},Except[aLMMethodRulePatternObject,
				commonOptionsPatternObject]]],
		lagrangeMultiplierNewRules=MapThread[
			Function[{rule,update},MapAt[#+update&,rule,2]],
				{lagrangeMultiplierRules,lagrangeMultiplierUpdates
					/.constraintRateMultiplierContainer->Identity
					/.penaltyMultiplierRule
					/.lagrangeMultiplierRules
					/.solutionRules}],
			penaltyMultiplierNewRule=MapAt[Min[#*penaltyMultiplierGrowthFactor,
				"MaximumPenaltyMultiplier"/.{opts}]&,penaltyMultiplierRule,2]},
		{monitorRules[variables,Last@Block[{FindMinimum},FindMinimum[
			function+Apply[Plus,penalties/.constraintRateMultiplierRule
				/.lagrangeMultiplierNewRules/.penaltyMultiplierNewRule],
			List@@@solutionRules,findMinimumOptions]],StepMonitor,opts],
			penaltyMultiplierNewRule,lagrangeMultiplierNewRules}]

defineBadArgs@aLMKernel;

constraintRateMultiplier[function_,variables:multipleExpressionPatternObject,
	constraintValue_,opts___?OptionQ]:=
	constraintRateMultiplierContainer@Divide[
		Norm@If[
			ReplaceAll[Gradient,{opts}]===Automatic,D[function,{variables,1}],
				Gradient/.{opts} (*should be something for numeric derivative*)
				],
		Norm@D[constraintValue,{variables,1}]
		];

defineBadArgs@constraintRateMultiplier;

constraintPenaltyTransformation[function_,
	variables:multipleExpressionPatternObject,
	penalty:constraintPatternObject,penaltyMultiplier_Symbol,opts___?OptionQ]:=
	Module[{constraintValue,lagrangeMultiplier,scaledConstraintValue,
		scaledEquivalentConstraintValue},
		constraintValue=Which[
			MatchQ[Head[penalty],(Less|LessEqual)],
			scaledEquivalentConstraintValue=Max[
				scaledConstraintValue,
				-lagrangeMultiplier/(2*penaltyMultiplier)
				];
			Subtract@@penalty,
			MatchQ[Head[penalty],(Greater|GreaterEqual)],
			scaledEquivalentConstraintValue=Max[
				scaledConstraintValue,
				-lagrangeMultiplier/(2*penaltyMultiplier)
				];
			Subtract@@Reverse@penalty,
			MatchQ[Head[penalty],Equal],
				scaledEquivalentConstraintValue=scaledConstraintValue;
				Subtract@@penalty
			];
		scaledConstraintValue=constraintValue*
			constraintRateMultiplier[function,variables,constraintValue,opts];
		{lagrangeMultiplier*scaledEquivalentConstraintValue+penaltyMultiplier*
			scaledEquivalentConstraintValue^2,2*penaltyMultiplier*
			scaledEquivalentConstraintValue,lagrangeMultiplier}
		];

defineBadArgs@constraintPenaltyTransformation;

chooseMethod[method_Symbol,methodRulePatternObject_Rule,
	methodOptions_Symbol,opts___?OptionQ]:=
	Module[{methodOptionPossibleList,methodRuleList=Cases[{opts},
		Map[HoldPattern,methodRulePatternObject,{0}]],optionHeadAlternatives},
		If[methodRuleList==={},False,methodOptionPossibleList=Rest@Flatten@List@
			methodRuleList[[1,2]];If[optionsListValidQ[method,
				methodOptionPossibleList],methodOptions=Sequence@@
					methodOptionPossibleList;True,False]]]

defineBadArgs@chooseMethod;

Options@NMinimize`AugmentedLagrangeMultiplier={"InitialLagrangeMultipliers"->0,
	"InitialPenaltyMultiplier"->1,"MaximumPenaltyMultiplier"->10^5,
	"PenaltyMultiplierGrowthFactor"->GoldenRatio,Gradient->Automatic,
	Method->{vMMethodString,Method->{uMethodString,
		"MaxDisplacement"->{10,-10},"MaxNarrowingIterations"->6}}}

NMinimize[{function_,constraints:multipleConstraintPatternObject},
	variableStartRanges:multipleGuessRangePseudoPatternObject,opts___?OptionQ]:=
	Module[{constraintsList=List@@constraints,lagrangeMultiplierRules,
		lagrangeMultipliers,lagrangeMultiplierUpdates,methodOptions,
		options,penalties,penaltyMultiplier,penaltyMultiplierGrowthFactor,
		penaltyMultiplierRule,solutionRules=#1->Mean@{##2}&@@@
			variableStartRanges,variables=variableStartRanges[[All,1]],
		workingPrecision},(options=parseOptions[{methodOptions,opts},
			{NMinimize`AugmentedLagrangeMultiplier,NMinimize}];
		workingPrecision=WorkingPrecision/.{options};
		penaltyMultiplierGrowthFactor="PenaltyMultiplierGrowthFactor"
			/.{options};
		penaltyMultiplierRule=penaltyMultiplier->
			ReplaceAll["InitialPenaltyMultiplier",{options}];
		{penalties,lagrangeMultiplierUpdates,lagrangeMultipliers}=Transpose[
			constraintPenaltyTransformation[function,variables,#,
			penaltyMultiplier,options]&/@constraintsList];
		lagrangeMultiplierRules=Thread[lagrangeMultipliers->
			"InitialLagrangeMultipliers"/.{options}];
		FixedPoint[Apply[aLMKernel[function,variables,#1,penalties,#2,
			N[penaltyMultiplierGrowthFactor,workingPrecision],#3,
			lagrangeMultiplierUpdates,options]&,#]&,
			{monitorRules[variables,solutionRules,StepMonitor,options],
				penaltyMultiplierRule,lagrangeMultiplierRules}/.
				ruleNumeric[workingPrecision]
			,MaxIterations/.{options}])/;
		chooseMethod[NMinimize`AugmentedLagrangeMultiplier,
			aLMMethodRulePatternObject,methodOptions,opts]]

Attributes[FindMinimum]=oldAttributesFindMinimum;
Protect[NMinimize,FindMinimum];
Update/@{NMinimize,FindMinimum};

End[];

EndPackage[];