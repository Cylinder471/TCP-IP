# Number of characters to be read
# at once.
FRAME_SIZE = 10

# Buffer size of tcp socket
BUFFER_SIZE = 1024 * 10

# Constant to determine the end
# of file and transaction.
END_OF_FILE = "##**##**##**##**##"

# CRC generator key
CRC_GENERATOR = "10110100110101110011010101110100000101"

# Accept and reject acknowledgements
# from receiver to the sender.
REJECT = "NAK"
ACCEPT = "OK"
