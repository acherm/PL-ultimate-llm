# This file is part of NIT ( http://www.nitlanguage.org ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Simple example of binary search tree
module trees

# A binary tree node
class Node
	var value: Int
	var left: nullable Node = null
	var right: nullable Node = null

	# Insert a value in the tree
	fun insert(v: Int)
	do
		if v < value then
			var l = left
			if l == null then
				left = new Node(v)
			else
				l.insert(v)
			end
		else if v > value then
			var r = right
			if r == null then
				right = new Node(v)
			else
				r.insert(v)
			end
		end
	end

	# Print the tree in order
	fun print_in_order
	do
		var l = left
		if l != null then l.print_in_order
		print value
		var r = right
		if r != null then r.print_in_order
	end

	# Search for a value in the tree
	fun search(v: Int): Bool
	do
		if v == value then return true
		if v < value then
			var l = left
			if l == null then return false
			return l.search(v)
		else
			var r = right
			if r == null then return false
			return r.search(v)
		end
	end
end

# Create a tree and insert some values
var root = new Node(50)
root.insert(30)
root.insert(70)
root.insert(20)
root.insert(40)
root.insert(60)
root.insert(80)

print "Tree in order:"
root.print_in_order

print "\nSearching for 40: {root.search(40)}"
print "Searching for 25: {root.search(25)}"