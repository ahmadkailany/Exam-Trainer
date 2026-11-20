#include <unistd.h>
void print_bits(unsigned char octet)
{
	for (int i = 7; i >= 0; i--)
		write(1, (octet >> i) & 1 ? "1" : "0", 1);
}
