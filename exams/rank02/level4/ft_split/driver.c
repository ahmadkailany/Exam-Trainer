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
char **ft_split(char *str);
int main(int ac, char **av)
{
	for (int a = 1; a < ac; a++)
	{
		char **t = ft_split(av[a]);
		int n = 0;
		if (!t) { ps("NULL"); pnl(); continue; }
		while (t[n]) { ps("["); ps(t[n]); ps("]"); n++; }
		ps(" ("); pn(n); ps(" words)"); pnl();
	}
	return (0);
}
