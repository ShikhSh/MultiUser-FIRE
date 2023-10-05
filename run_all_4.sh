#! /usr/bin/bash

cd MainAlgo/
python3 run.py
echo "1 iterations done"
python3 run.py
echo "2 iterations done"
python3 run.py
echo "3 iterations done"
python3 run.py
echo "4 iterations done"
cd ..

cd Baseline1/
python3 run.py
echo "1 iterations done"
python3 run.py
echo "2 iterations done"
python3 run.py
echo "3 iterations done"
python3 run.py
echo "4 iterations done"
cd ..

cd Baseline2/
python3 run.py
echo "1 iterations done"
python3 run.py
echo "2 iterations done"
python3 run.py
echo "3 iterations done"
python3 run.py
echo "4 iterations done"
cd ..

cd Baseline3/
python3 run.py
echo "1 iterations done"
python3 run.py
echo "2 iterations done"
python3 run.py
echo "3 iterations done"
python3 run.py
echo "4 iterations done"
cd ..

python3 coalate_results.py