import os.path
import argparse
import simbolo
import reader
import utils
import shannon
import writer

"""
TODO:
[x]	Reading the command line arguments works but we should
	probably make the messages more readable(?), a bit more
	nice to the eye :P

[x]	1- Check if files exist
[x]	2- Read and create dictionary ( { simb: total vezes que aparece no ficheiro } )
[x]	3 - Transform that into {simb: Simbolo}
[x]	4 - Do calculations, entropy and shit (see if file is worth compressing)
[x]	5 - Shannon fano
[]	7 - write, byte per byte

	that's all folks :P
"""

parser = argparse.ArgumentParser("Compress some files")

# "nargs=+" -> gathers all the file names passed as arguments, in a list
parser.add_argument('files', nargs='+')

# debug flag
parser.add_argument('-d', action='store_true')

parser.add_argument('-check', action='store_true')

args = parser.parse_args()

real_files = []
for i in args.files:
	if not os.path.isfile(i):
		print "{0} does not exist!".format(i)
	else:
		real_files.append(i)

if len(real_files)==0:
	raise SystemExit("You entered no existing files!\nTerminating...")

simbolos = {} # simbolos -> { char x: how many x's are in the file }
for i in real_files:
	f = open(i, 'r')
	total_lido = reader.read_file(f, simbolos) # reads file, updates simbolos, returns number of bytes read
	# Transform simbolos -> { char x: Simbolo(#x's, total_lido) }
	for key in simbolos.keys():				   
		total_simb = simbolos[key]
		simbolos[key] = simbolo.Simbolo(key, total_simb, total_lido)
	# Sort by freq
	sortedList = sorted(simbolos.values(), reverse=True)
	# Entropy and shit -> decisions
	e = utils.entropy(sortedList)
	if args.d: 
		print e
		print utils.entropyLimit(total_lido)
	
	if args.check:
		raise SystemExit("Entropy checked!")
	# Shannon
	shannon.shannon(sortedList, 0, len(sortedList)-1)
	
	if args.d:
		for x in sortedList:
			if x.getSimb() == '\n':
				print "\\n: %s (%f)" % (x.getCode(), x.getFreq())
			else:
				print "%c: %s (%f)" % (x.getSimb(), x.getCode(), x.getFreq())

	#Assuming the model: <file_name>.<extension> 
	temp = i.split('.')
	newFileName = temp[0]+"_zip"	
	outFile = open(newFileName, "wb")
	#write
	teste = {}
	for i in sortedList:
		teste[i.getSimb()] = i 
	
	writer.write(teste, f, outFile)
	f.close()
	outFile.close();
