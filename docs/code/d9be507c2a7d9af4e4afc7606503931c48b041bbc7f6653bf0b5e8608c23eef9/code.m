function solution = sudokuSolver(board)
% SUDOKUSOLVER Solve a Sudoku puzzle.
%   solution = sudokuSolver(board) takes a partially filled Sudoku board and
%   returns the solved board.

% This function works by filling in the board one cell at a time, starting from
% the top-left. If a cell is empty, it tries numbers 1-9 in order. If a number
% is valid (i.e., it doesn't already appear in the same row, column, or 3x3
% sub-grid), it recursively tries to fill in the rest of the board.

% If it can't find a valid number for a cell, it backtracks and tries a different
% number for the previous cell.

% The base case for the recursion is when the board is full (i.e., there are no
% more empty cells).

% This function assumes that the input board is valid (i.e., it's a 9x9 matrix
% of integers between 0 and 9, where 0 represents an empty cell).

% See also SUDOKUVALID.

% Author: Will Dwinnell
% Copyright 2017 Will Dwinnell

    solution = board;
    for i = 1:9
        for j = 1:9
            if solution(i,j) == 0
                for k = 1:9
                    if isValid(solution, i, j, k)
                        solution(i,j) = k;
                        solution = sudokuSolver(solution);
                        if all(all(solution ~= 0))
                            return;
                        end
                        solution(i,j) = 0;
                    end
                end
                return;
            end
        end
    end
end

function isValid = isValid(board, row, col, num)
% ISVALID Check if a number can be placed in a given cell.
%   isValid = isValid(board, row, col, num) returns true if it's valid to place
%   the number num in the cell at position (row, col), and false otherwise.

% A number is valid if it doesn't already appear in the same row, column, or
% 3x3 sub-grid.

% See also SUDOKUSOLVER.

% Author: Will Dwinnell
% Copyright 2017 Will Dwinnell

    isValid = true;
    for i = 1:9
        if board(row,i) == num || board(i,col) == num
            isValid = false;
            return;
        end
    end
    subGridRow = 3*floor((row-1)/3) + 1;
    subGridCol = 3*floor((col-1)/3) + 1;
    for i = 0:2
        for j = 0:2
            if board(subGridRow+i, subGridCol+j) == num
                isValid = false;
                return;
            end
        end
    end
end