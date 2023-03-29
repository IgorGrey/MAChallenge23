def calculate_checksum(nmea_sentence):
    """
    Calculates the checksum of an NMEA sentence.

    :param nmea_sentence: the NMEA sentence to calculate the checksum for
    :return: the checksum as a string
    """
    # Remove the starting '$' and ending '*' characters
    nmea_sentence = nmea_sentence.strip('$')
    nmea_sentence = nmea_sentence.strip('*')

    # Calculate the checksum
    checksum = 0
    for char in nmea_sentence:
        checksum ^= ord(char)

    # Convert the checksum to a hexadecimal string
    checksum_hex = hex(checksum)[2:]

    # Pad the hexadecimal string with a leading zero if necessary
    if len(checksum_hex) == 1:
        checksum_hex = '0' + checksum_hex

    return checksum_hex.upper()
nmea = "$CCTHD,80.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00"
calculate_checksum(nmea)
print(calculate_checksum(nmea))