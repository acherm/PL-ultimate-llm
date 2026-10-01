## Copyright (C) 2006 Michel D. Schmid
##
## This file is part of Octave.
##
## Octave is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2, or (at your option)
## any later version.
##
## Octave is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Octave; see the file COPYING.  If not, write to the Free
## Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
## 02110-1301, USA.

## -*- texinfo -*-
## @deftypefn {Function File} {} printNumInputDelays (@var{fid})
## @code{printMLPHeader} saves the header of a  neural network structure
## to a *.txt file with identification @code{fid}.
## @end deftypefn

## Author: mds
## $Revision$, $Date$

function printNumInputDelays(fid,net)

     ## now check the structure fields..
     cellNetFields = fieldnames(net);
     # search for numInputDelays
     if isfield(net,"numInputDelays")
        # test on scalar
        if isscalar(net.numInputDelays)
           fprintf(fid,"      numInputDelays:  %d  (read-only)\n",net.numInputDelays);
        # net.numInputDelays must be an integer... till now, 11-01-2006
        else
            error("numInputDelays must be a scalar value!");
        endif
     endif
     
endfunction