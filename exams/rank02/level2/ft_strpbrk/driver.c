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
char *ft_strpbrk(const char *s1, const char *s2);
int main(int ac, char **av)
{
	for (int i = 1; i + 1 < ac; i += 2)
	{
		char *r = ft_strpbrk(av[i], av[i + 1]);
		if (!r) ps("NULL");
		else { ps("index "); pn(r - av[i]); ps(" -> ["); ps(r); ps("]"); }
		pnl();
	}
	return (0);
}
