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
#include "ft_list.h"
void ft_list_foreach(t_list *begin_list, void (*f)(void *));
static t_list *build(int ac, char **av, int from)
{
	t_list *head = NULL;
	for (int i = ac - 1; i >= from; i--)
	{
		t_list *n = malloc(sizeof(t_list));
		n->data = strdup(av[i]);
		n->next = head;
		head = n;
	}
	return (head);
}
static void show(void *d) { ps("<"); ps((char *)d); ps(">"); pnl(); }
static void upper(void *d) { for (char *s = d; *s; s++) if (*s >= 'a' && *s <= 'z') *s -= 32; }
int main(int ac, char **av)
{
	t_list *l = build(ac, av, 1);
	ft_list_foreach(l, show);
	ft_list_foreach(l, upper);
	ft_list_foreach(l, show);
	ps("end"); pnl();
	return (0);
}
