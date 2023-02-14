SRC=src
TLS=tools
RES=results
BLD=build

### Build ###

# Build correlation script.
buildtools:
	gcc -O3 -o ${BLD}/correlate ${TLS}/correlate.c -lm
	sudo chmod +x ${BLD}/correlate

### Run ###

# Sample encryption timings through serial link.
# Make sure the key in the Pico is full of zeros.
study:
	@mkdir -p ${RES}
	sudo python3 ${TLS}/sample.py 8192000 ${RES}/study_samples

# Sample encryption timings through serial link.
# Make sure the key in the Pico is the private key.
attack:
	@mkdir -p ${RES}
	sudo python3 ${TLS}/sample.py 8192000 ${RES}/attack_samples

# Perform correlation between study and attack.
correlate:
	(tail -4096 ${RES}/study_samples; tail -4096 ${RES}/attack_samples) \
	| ${BLD}/correlate >> ${RES}/correlated

### Analyze ###

# Plots the average cycle count with regard to each possible value (0 to 255) 
# for each byte of the input block (plaintext[0] to plaintext[15]).
# Each subplot corresponds to one of the 16 bytes of the input plaintext block.
# The input data are the most recent values obtained with the study phase.
overview_study:
	tail -4096 ${RES}/study_samples > ${RES}/study_tmp
	python3 ${TLS}/overview.py ${RES}/study_tmp
	rm ${RES}/study_tmp

# Plots the average cycle count with regard to each possible value (0 to 255) 
# for each byte of the input block (plaintext[0] to plaintext[15]).
# Each subplot corresponds to one of the 16 bytes of the input plaintext block.
# The input data are the most recent values obtained with the attack phase.
overview_attack:
	tail -4096 ${RES}/attack_samples > ${RES}/attack_tmp
	python3 ${TLS}/overview.py ${RES}/attack_tmp
	rm ${RES}/attack_tmp

# Shows a representation of the 'supposed known bits' of the private key.
# If a bit is known, his value ('1' or '0') is printed. Else, '_' is printed.
# The bits are grouped in bytes. k[0] ... k[15] ar represented from left to right
# with MSB first.
# User can manually execute the script with custom probability as threshold.
show_known_bits:
	tail -16 ${RES}/correlated > ${RES}/correlated_tmp
	python3 ${TLS}/known_bits.py ${RES}/correlated_tmp 0.9
	rm ${RES}/correlated_tmp

# Prints hard-coded key in the same format as output of show_known_bits.
# It allows to compare easily what is known and the real private key.
# The key in the python script is the same as the one hard-coded in the C file main.c.
show_private_key:
	python3 ${TLS}/print_key.py