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
int *ft_rrange(int start, int end);
int main(int ac, char **av)
{
	int s = atoi(av[1]), e = atoi(av[2]);
	int *t = ft_rrange(s, e);
	int n = (s > e ? s - e : e - s) + 1;
	if (!t) { ps("NULL"); pnl(); return (0); }
	for (int i = 0; i < n; i++) { if (i) ps(", "); pn(t[i]); }
	pnl();
	free(t);
	return (0);
}
