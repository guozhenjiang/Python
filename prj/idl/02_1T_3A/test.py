bytes_a = b'\x01\x02\x03\x04\x05'
bytes_b = b'\x06\x07\x08\x09\x10'
bytes_c = bytes()

print('bytes_a:', bytes_a)
print('bytes_b:', bytes_b)
print('bytes_c:', bytes_c)

bytes_c = bytes_a + bytes_b
bytes_a += bytes_b

print('bytes_a:', bytes_a)
print('bytes_c:', bytes_c)