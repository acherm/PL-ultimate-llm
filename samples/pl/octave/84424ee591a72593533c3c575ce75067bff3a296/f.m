function xp = f(t,y)
%y = [ uo vo wo 0 0 0 0 titacero ];
global rho 
global vinf
global sup
global b
global c
global g
global m
global de
global Ix
global Iy
global Iz
global V
global Po
V = sqrt(y(1)^2 + y(2)^2 + y(3)^2) ;
betha = asind(y(2)/vinf);
alpha = atand(y(3)/y(1));


fila1 = [1 alpha alpha^2 alpha^3 alpha^4 alpha^5 alpha^6 abs(betha) betha^2 abs(betha^3) betha^4 alpha*abs(betha)]; 

fila2 = [1 alpha alpha^2 alpha^3 alpha^4] ;

##Cxo =  fila1*hl20.Po(:,3)*-1 ;
##
##Czo = fila1*hl20.Po(:,1)*-1 ;
##
##Cmo = fila1*hl20.Po(:,2) ; 
##
##Czde= fila2*hl20.Pde(:,1)*-1 ;
##
##Cmde= fila2*hl20.Pde(:,2) ;
##
##Cxde= fila2*hl20.Pde(:,3)*-1 ;
##
##Cmq = interp1(hl20.Cdamp_alpha,hl20.Cmq,alpha);
##
##Cno = interp2(hl20.Cn_alpha,hl20.Cn_beta,hl20.Cn',alpha,abs(betha)); %(3,:) fila3 - ":" todas las columnas
##%Cno = interp1(hl20.Cn_beta,hl20.Cn(3,:),betha);
##
##Clp = interp1(hl20.Cdamp_alpha,hl20.Clp,alpha);
##
##Clr = interp1(hl20.Cdamp_alpha,hl20.Clr,alpha);
##
##Cnp = interp1(hl20.Cdamp_alpha,hl20.Cnp,alpha);
##
##Cnr = interp1(hl20.Cdamp_alpha,hl20.Cnr,alpha);

Cxo =  fila1*Po(:,3)*-1 ;

Czo = fila1*Po(:,1)*-1 ;

Cmo = fila1*Po(:,2) ; 

Czde= fila2*Pde(:,1)*-1 ;

Cmde= fila2*Pde(:,2) ;

Cxde= fila2*Pde(:,3)*-1 ;

Cmq = interp1(Cdamp_alpha,Cmq,alpha);

Cno = interp2(Cn_alpha,Cn_beta,Cn',alpha,abs(betha)); %(3,:) fila3 - ":" todas las columnas
%Cno = interp1(Cn_beta,Cn(3,:),betha);

Clp = interp1(Cdamp_alpha,Clp,alpha);

Clr = interp1(Cdamp_alpha,Clr,alpha);

Cnp = interp1(Cdamp_alpha,Cnp,alpha);

Cnr = interp1(Cdamp_alpha,Cnr,alpha);




xp(1)= ((0.5*rho*vinf^2*sup*(Cxo + Cxde*de) - m*g*sin(y(7)))/m) - y(5)*y(3) + y(6)*y(2);
xp(2)= ((0.5*rho*vinf^2*sup*(-0.01242*betha)+ m*g*cos(y(7))* sin(y(8)))/ m) - y(6)*y(1) + y(4)*y(3);
xp(3)= ((0.5*rho*vinf^2*sup*(Czo + Czde*de) + m*g*cos(y(7))*cos(y(8)))/m) - y(4)*y(2)+y(5)*y(1);
xp(4)= (0.5*rho*vinf^2*sup*b*(-0.00787*betha + Clp*((y(4)*b)/(2*V))+ Clr*((y(6)*b)/(2*V)))-y(5)*y(6)*(Iz-Iy))/Ix; 
xp(5)= (0.5*rho*vinf^2*sup*b*(Cmo + Cmq*((y(5)*c)/2*V) + Cmde*de )-y(5)*y(6)*(Ix-Iz))/Iy ;
xp(6)= (0.5*rho*vinf^2*sup*b*(Cno + Cnp*((y(4)*b)/(2*V)) + Cnr*((y(6)*b)/(2*V))) - y(4)*y(5)*(Iy-Ix))/Iz ;
xp(7)= y(5)*cos(y(8))- y(6)*sin(y(8));
xp(8)= y(4) + y(5)*sin(y(8))*tan(y(8)) + y(6)*cos(y(8))*tan(y(7)) ;

xp = xp';
    



endfunction


