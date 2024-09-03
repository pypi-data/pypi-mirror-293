cd "../src"

echo "Complimentaty Commands ===="
python3 -m xt_neighbor_cpu --help
python3 -m xt_neighbor_cpu --version

echo "Basic Usage ===="
python3 -m xt_neighbor_cpu -i ../test/dummy_input.txt -o ../test/output1.txt
python3 -m xt_neighbor_cpu -i ../test/dummy_input.txt -d 2

echo "AIRR Mode ===="
python3 -m xt_neighbor_cpu -a -i ../test/dummy_input_airr.tsv

echo "Comparison Mode ===="
python3 -m xt_neighbor_cpu -a -i ../test/dummy_input_airr.tsv -I ../test/dummy_input_airr.tsv -o ../test/output2.txt

echo "Hamming Distance Mode ===="
python3 -m xt_neighbor_cpu -a -i ../test/dummy_input_airr.tsv -m hamming
python3 -m xt_neighbor_cpu -a -i ../test/dummy_input_airr.tsv -m hamming -d 2