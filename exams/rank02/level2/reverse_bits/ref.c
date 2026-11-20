unsigned char reverse_bits(unsigned char octet)
{
	unsigned char r = 0;
	for (int i = 0; i < 8; i++)
		r = (r << 1) | ((octet >> i) & 1);
	return (r);
}
