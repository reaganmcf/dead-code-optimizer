#!/usr/bin/fish

for f in testcases/test*.iloc
	python3 deadcode.py < $f > testcases/opt-(basename $f).iloc
	echo "Running " $f
	echo "Before"
	../ILOC_Simulator/sim < $f 
	
	echo "--"
	echo "After"
	../ILOC_Simulator/sim < testcases/opt-(basename $f).iloc

	echo "----------"
end
