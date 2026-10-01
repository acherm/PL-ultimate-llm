classdef LEAVE
    properties
        Block
        Arm
        Add
        Del
        Prec
        Id
    end
    methods (Static)
        function obj = LEAVE(block,arm,n,maxcolumnsnum)
            if (n<=maxcolumnsnum)
                obj.Block = block;
                obj.Arm = arm;
                obj.Add = {ONTABLE(block) EMPTYARM(arm) USEDCOLSNUM(n+1)};
                obj.Del = {HOLDING(block,arm) USEDCOLSNUM(n)};
                obj.Prec = {HOLDING(block,arm) USEDCOLSNUM(n)};
                obj.Id = ['LEAVE(' block.Name ',' arm ')'];
            else
                error('Too many columns')
            end
        end
    end
   end