def receiver(got, pattern_bits):  # The receiver should do division also as the sender does
    rem = division_process(got, pattern_bits)
    for k in range(len(rem)):  # Check the remainder == 0 (looping bit by bit)
        if rem[k] != 0:
            return False
    return True


def division_process(data_bits, divisor):
    rem = [0 for x in range(len(divisor))]  # To store the remainder
    data_with_pattern = [0 for x in range(len(data_bits) + len(divisor))]  # Array of length sum of parameters lengths

    for i in range(len(data_bits)):
        data_with_pattern[i] = data_bits[i]
    for i in range(len(divisor)):
        rem[i] = data_with_pattern[i]

    # print(len(data_with_pattern))
    # print(data_with_pattern)
    # print(rem)

    for i in range(len(data_bits)):
        # print('First data bit:', rem[0])
        # print('remainder:')
        if rem[0] == 1:
            for j in range(1, len(divisor)):  # bitwise XOR
                rem[j-1] = rem[j] ^ divisor[j]
                # print(rem[j-1])
        else:
            for j in range(1, len(divisor)):
                rem[j-1] = rem[j]
                # print(rem[j-1])
        rem[len(divisor) - 1] = data_with_pattern[i + len(divisor)]
        # print(rem[len(pattern_bits) - 1])
    return rem


''' Start of the program '''

print('Read a stream of bits for "DATA":')
stream_data = input()

data = []
for bit in stream_data:
    data.append(int(bit))

''' Data is read and put in data array now as integers '''

print('Read a stream of bits for "PATTERN":')
stream_divisor = input()

pattern = []
for bit in stream_divisor:
    pattern.append(int(bit))

''' Divisor is read and put in pattern array now as integers '''

remainder = division_process(data, pattern)
print('The remainder:')
for i in range(len(remainder) - 1):
    print('remainder[', i, '] =', remainder[i])

generated = []
print('The generated code from CRC (Data will be sent from sender):')
for i in data:
    generated.append(i)
for i in range(len(remainder) - 1):
    generated.append(remainder[i])

print(generated)  # Sender

arrived_data = [0 for j in range(len(data) + len(remainder) - 1)]  # Receiver
print('Read the data arrived to receiver to check if there is an error using CRC:')
# If you have read a bit wrong it will be considered as a noise (Data received with noise)
# If you have read the data here exactly the same as generated => the data received without any noise
received = input()
for k in range(len(received)):
    arrived_data[k] = int(received[k])

''' Data is being arrived to receiver '''

flag = receiver(arrived_data, pattern)

if flag:
    print('The data was received to receiver successfully with no any error !')
else:
    print('An error in the received data in receiver side ...')

''' Computing the error percentage by comparing the generated bits in the sender and arrived to receiver '''

count = 0
if len(generated) == len(arrived_data):
    for i in range(len(generated)):
        if (generated[i] ^ arrived_data[i]) == 1:  # Two bits are different to each other
            count += 1
print('The percentage error = ', "{:.2f}".format(count/len(generated) * 100), '%')
