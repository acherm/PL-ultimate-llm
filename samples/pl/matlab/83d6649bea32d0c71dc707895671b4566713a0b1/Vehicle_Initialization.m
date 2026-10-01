
set(0,'DefaultFigureWindowStyle','docked')


lapsim.plotpooper=false;

%% 1. Chassis Initialization

% Structural
chassis.wheelbase= 1.524; % [m]
chassis.fronttrack = 1.2192; % [m]
chassis.reartrack = 1.1684; % [m]


% Mass Distribution
chassis.mass.totalmass = 275; % [kg]
chassis.mass.totalmassdistribution = 50; % [%] weight on front tires
chassis.mass.frontnonsusmass = 12; % [kg] front non suspended mass per wheel
chassis.mass.rearnonsusmass = 13; % [kg] rear non suspended mass per wheel
chassis.mass.susmass = chassis.mass.totalmass - 2*chassis.mass.frontnonsusmass - 2*chassis.mass.rearnonsusmass;


chassis.mass.a = chassis.wheelbase*chassis.mass.totalmassdistribution/100;
chassis.mass.b = chassis.wheelbase*(100-chassis.mass.totalmassdistribution)/100;

chassis.mass.cg = 294; % [mm] total mass cg height
chassis.mass.frontnonsusmassheight = 260; % [mm] front non suspended mass height
chassis.mass.rearnonsusmassheight = 260; % [mm] rear non suspended mass height

chassis.mass.susmassrollinertia = 200; % [kg.m^2] suspended mass roll inertia (ref SM CG - Ixx)

% Spring & ARB stiffnesses
chassis.spring.fspringstiff = 26.3; % [N/mm] front spring stiffness
chassis.spring.rspringstiff = 35.03; % [N/mm] rear spring stiffness
chassis.arb.fARBstiff = 19.27; % [N/mm]
chassis.arb.rARBstiff = 19.91; % [N/mm]


% Motion Ratios
chassis.spring.fspringMR = 1.25; % [mm/mm] front spring motion ratio
chassis.spring.rspringMR = 1.3; % [mm/mm] rear spring motion ratio
chassis.arb.fARBMR = 2.250; % [mm/mm]
chassis.arb.rARBMR = 2.250; % [mm/mm]
chassis.spring.FWR = chassis.spring.fspringstiff/chassis.spring.fspringMR^2; %Front Wheel Rate (N/mm)
chassis.spring.RWR = chassis.spring.rspringstiff/chassis.spring.rspringMR^2; %Rear Wheel Rate (N/mm)
% Roll
chassis.roll.fRCheight = 15; % [mm] front roll center height
chassis.roll.rRCheight = 40; % [mm] rear roll center height
chassis.roll.SMCGheight = (chassis.mass.totalmass*chassis.mass.cg-(2*chassis.mass.frontnonsusmass*chassis.mass.frontnonsusmassheight+2*chassis.mass.rearnonsusmass*chassis.mass.rearnonsusmassheight))/chassis.mass.susmass;

chassis.roll.AR_FrontSpring = ((chassis.fronttrack.^2)*tan(deg2rad(1)) * chassis.spring.FWR * 1000)/2; %Anti-roll stiffness from front spring (Nm/deg)
chassis.roll.AR_RearSpring = ((chassis.reartrack.^2)*tan(deg2rad(1)) * chassis.spring.RWR * 1000)/2; %Anti-roll stiffness from rear spring (Nm/deg)

chassis.roll.AR_FrontARB = ((chassis.arb.fARBstiff*1000)*(chassis.fronttrack.^2)*tan(deg2rad(1)))/(chassis.arb.fARBMR.^2); %Anti-roll stiffness from front ARB (Nm/deg)
chassis.roll.AR_RearARB = (chassis.arb.rARBstiff*1000* (chassis.reartrack.^2)*tan(deg2rad(1)))/(chassis.arb.rARBMR.^2); %Anti-roll stiffness from rear ARB (Nm/deg)
chassis.roll.AR_Total = chassis.roll.AR_FrontSpring + chassis.roll.AR_RearSpring + chassis.roll.AR_FrontARB + chassis.roll.AR_RearARB; %Total Anti-roll stiffness
chassis.roll.dz = chassis.roll.SMCGheight -(((chassis.roll.rRCheight-chassis.roll.fRCheight)/(chassis.wheelbase*1000) * ((1-(chassis.mass.totalmassdistribution/100))*(chassis.wheelbase*1000))) + chassis.roll.fRCheight); % Z distance from SM CG to roll axis at the SM CG

% Aerodynamics
chassis.aero.DFcoeff = 0; % [] down force coefficient
chassis.aero.DFdist = 45; % [%] front down force distribution
chassis.aero.airdensity = 1.2255; % [kg/m^3] 
chassis.aero.frontalarea = 1.75; % [m^2]
chassis.aero.aerospeed = 187.2; % [km/h] vehicle speed for aero calcs
chassis.aero.Cd = 0.3;  %  [] drag coefficient

% Tire
chassis.tire.tireR=0.2286; %[m] tire radius
chassis.tire.rollingresistance=0.015; %[] coefficient of rolling resistance
chassis.tire.ftirestiff = 120; % [N/mm]
chassis.tire.rtirestiff = 120; % [N/mm]
% load(strcat(pwd,'\mat files\','tiredata.mat'));
% chassis.tire.Fypos=tiredata.Fypos;
% chassis.tire.Fxpos=tiredata.Fxpos;
% chassis.tire.Fyneg=tiredata.Fyneg;
% chassis.tire.Fxneg=tiredata.Fxneg;
% chassis.tire.Fzdata=tiredata.Fzdata;
lapsim.vehicle.chassis=chassis;
clear chassis %tiredata
