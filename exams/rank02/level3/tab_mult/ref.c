#include <unistd.h>
static void putnbr(int n)
{
	char c;
	if (n > 9)
		putnbr(n / 10);
	c = n % 10 + '0';
	write(1, &c, 1);
}
int main(int ac, char **av)
{
	if (ac != 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	int n = 0;
	for (int i = 0; av[1][i] >= '0' && av[1][i] <= '9'; i++)
		n = n * 10 + av[1][i] - '0';
	for (int i = 1; i <= 9; i++)
	{
		putnbr(i);
		write(1, " x ", 3);
		putnbr(n);
		write(1, " = ", 3);
		putnbr(i * n);
		write(1, "\n", 1);
	}
	return (0);
}
