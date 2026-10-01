
s = tf('s');

F1 = 4*s/(10*s^2 +4);

F2 = 3/(6*s + 16);

F3 = (4*s + 10)/(4*s^3+9*s^2+5*s);

F4 = 1/(7*s+10);

F5 = (8*s + 8)/(s^3+2*s^2+3*s);

F6 = (3*s+2)/(5*s^2+7*s+10);

F3_feedback = feedback(F3,1,+1);

H1 = F1;

H2 = F2;

H3_1 = F4 + F5;

H3 = F3_feedback * H3_1 * F6; 

H = H1 + H2 + H3;

step(H);

display(H);
