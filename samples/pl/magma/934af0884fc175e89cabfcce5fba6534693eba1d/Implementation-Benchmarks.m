/***
 *  Produces benchmarks
 *
 *  Distributed under the terms of the GNU Lesser General Public License (L-GPL)
 *                  http://www.gnu.org/licenses/
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published by
 *  the Free Software Foundation; either version 2.1 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 *  Copyright 2016 R. Lercier, C. Ritzenthaler & J.R. Sijsling
 */

AttachSpec("../package/spec");
AttachSpec("../g3twists_v2-0/spec");
filename := "Implementation-Benchmarks.dat";

n_max := 4;
exp_max := 4;
N := 2^6;

Fs := [* *];
Fs cat:= [*
GF(p, exp) : exp in [1] cat [ 25*n : n in [1..n_max] ], p in [19, 31, 41]
*];
Fs cat:= [*
GF(NextPrime(10^(50*N)), exp) : exp in [1..exp_max] cat [10], N in [1..4]
*];

for F in Fs do
    print "Proceeding to field", F;
    Write(filename, F);
    Domain := F;
    R<x,y,z> := PolynomialRing(F, 3);
    Mons := MonomialsOfDegree(R, 4);
    TotalTimeRec := 0;
    n := 0;
    while n ne N do
        f := &+[ Random(Domain)*Mons[i] : i in [1..#Mons] ];
        I, WI := DixmierOhnoInvariants(f);
        Time := Cputime();
        g := TernaryQuarticFromDixmierOhnoInvariants(I);
        delta := Cputime(Time);
        J, WJ := DixmierOhnoInvariants(g);
        if WPSNormalize(WI, I) eq WPSNormalize(WJ, J) then
            n +:= 1;
            TotalTimeRec +:= delta;
        else
            print F;
            print f;
        end if;
    end while;
    Write(filename, TotalTimeRec/N);
end for;

exit;
