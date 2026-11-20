#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static void ps(const char *s) { write(1, s, strlen(s)); }
static void pn(long long n)
{
	char b[32];
	int i = 31;
	unsigned long long u = n < 0 ? 0ULL - (unsigned long long)n : (unsigned long long)n;
	b[i] = 0;
	do { b[--i] = '0' + u % 10; u /= 10; } while (u);
	if (n < 0) b[--i] = '-';
	write(1, b + i, 31 - i);
}
static void pnl(void) { write(1, "\n", 1); }
char *ft_strrev(char *str);
int main(int ac, char **av)
{
	for (int i = 1; i < ac; i++)
	{
		char buf[512];
		strcpy(buf, av[i]);
		char *r = ft_strrev(buf);
		ps("["); ps(buf); ps("]"); ps(r == buf ? " returns str" : " WRONG RETURN VALUE"); pnl();
	}
	return (0);
}
