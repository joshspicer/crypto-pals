import sys

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result
# ----------------------------------

def hexTo64(hex):
	return HEX.decode('hex').encode('base64')

def fixedXOR(buf1, buf2):
	x = buf1.decode('hex')
	y = buf2.decode('hex')
	return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))

#challenge2string1 = '1c0111001f010100061a024b53535009181c'
#challenge2string2 = '686974207468652062756c6c277320657965'
#print fixedXOR(hex1, hex2).encode('hex')

def singleByteXOR(input, key):
	output = ""
	for i in input:
		output += chr(ord(i) ^ ord(key))
	return output

# challenge2 end #

frequency = {
' ': 13,
'e': 12.02,
't': 9.10,
'a': 8.12,
'o': 7.68,
'i': 7.31,
'n': 6.95,
's': 6.28,
'r': 6.02,
'h': 5.92,
'd': 4.32,
'l': 3.98,
'u': 2.88,
'c': 2.71,
'm': 2.61,
'f': 2.30,
'y': 2.11,
'w': 2.09,
'g': 2.03,
'p': 1.82,
'b': 1.49,
'v': 1.11,
'k': 0.69,
'x': 0.17,
'q': 0.11,
'j': 0.10,
'z': 0.07
}


class Result:
	def __init__(self, score, key, result):
		self.score = score
		self.key = key
		self.result = result

	def __eq__(self, other):
		return self.result == other.result

	def __lt__(self, other):
		return self.score < other.score

	def printObject(self):
		print('Key: ' + self.key + " Score: " + str(self.score) + " Phrase: " + str(self.result) + "\n")
	
	def __iter__(self):
		return self

def frequencyInEnglish(char):
	return frequency.get(char, 0)

def smartSingleByteXOR(input):
	arr = []
	options='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for key in options:
		score = 0
		result = singleByteXOR(input, key)
		for char in result:
			if True: # ((ord(char) in range(97,122)) or (ord(char) in range(64i,90) or (ord(char) == 32))):
				score += frequencyInEnglish(char)
		arr.append(Result(int(100*(float(score)/float(len(result)))), key, result))
	# Return sorted list
	arr.sort()
	return arr 


challengeThreeString='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')
#for ans in smartSingleByteXOR(challengeThreeString):
#	ans.printObject()
#print smartSingleByteXOR(challengeThreeString)[-1].printObject()

# challenge 3 end #

def detectSingleCharacterXOR(largeFile):
	bestCandidates = []
	lines = []
	with open(largeFile) as f:
		lines = f.readlines()
	lines = map(lambda x: x.decode('hex'), map(lambda x: x.split('\n')[0], lines))
#	print lines

	for l in lines:
		bestCandidates.append(smartSingleByteXOR(l)[-1])

	bestCandidates.sort()
	return bestCandidates


# for ans in detectSingleCharacterXOR('4.txt'):
#	ans.printObject()


# challenge 4 end #

# challenge 5 start #

c5input = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''

c5output = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

def repeatedXOR(inputText, key):
	output = ""
	modValue = len(key)
	for i in range(0,len(inputText)):
		output += chr(ord(inputText[i]) ^ ord(key[i % modValue]))

	return output


#print repeatedXOR(c5input, 'ICE').encode('hex')
#print repeatedXOR(c5output.decode('hex'), 'ICE')


# challenge 5 done #

# challenge 6 start #			

c6example1 = 'this is a test'
c6example2 = 'wokka wokka!!!'

def editDistance(str1, str2):
	total = 0
	b1 = tobits(str1)
	b2 = tobits(str2)
	for a,b in zip(b1, b2):
		if a != b:
			total += 1
	return total

# print editDistance(c6example1, c6example2)


def theThreeMostLikelyKeySizes(input):
	mostLikelySizes = []
	for size in range(2, 40):
		firstSample = input[0:size]
		secondSample = input[size+1:(2*size+1)]
		editD = editDistance(firstSample, secondSample) / size
		# Cover case where we don't have three options yet
		if (len(mostLikelySizes) != 3):
			mostLikelySizes.append(editD)
			mostLikelySizes.sort()
		for curr in range(0, len(mostLikelySizes)):
			if (mostLikelySizes[len(mostLikelySizes) - curr - 1] > editD):
				mostLikelySizes[len(mostLikelySizes) - curr - 1] = editD
				break
		mostLikelySizes.sort()
	
	return mostLikelySizes

	
#breakRepeatedXOR(input):
#	KEYSIZES = theThreeMostLikelyKeySizes(input)

fileSix = ''
with open('6.txt', 'r') as myfile:
    fileSix=myfile.read().replace('\n', '')

# print theThreeMostLikelyKeySizes(fileSix.decode('base64'))


def breakIntoBlocksOfSizeN(theFile, n):
	output = []
	for i in range(0, len(theFile), n):
		output.append(theFile[i:i+n]) 
	return output


testBrokenBlocks = breakIntoBlocksOfSizeN(fileSix, 5)	

def transposeBlocks(blocks, n):
	# Create array of empty strings, one for each tranposed string
	output = []
	for i in range(0,n):
		output.append('')
	# Start sifting bits from each block into correct string	
	for b in blocks:
		for whichBucket in range(0,len(b)):
			output[whichBucket] += b[whichBucket]
	return output



#print transposeBlocks(testBrokenBlocks, 5)
		
def breakRepeatKeyXOR(input):
	output = []
	KEYSIZE = theThreeMostLikelyKeySizes(input)
	transposedOptions = []
	for k in KEYSIZE:
		transposedOptions = transposeBlocks(breakIntoBlocksOfSizeN(input, k), k)
	# Start solving
	for t in transposedOptions:
		output.append(smartSingleByteXOR(t)[-1])
	return output




for item in breakRepeatKeyXOR(fileSix):
	print item.printObject()




