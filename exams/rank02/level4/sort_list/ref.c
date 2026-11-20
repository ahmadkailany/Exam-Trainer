#include "list.h"
t_list *sort_list(t_list *lst, int (*cmp)(int, int))
{
	int swapped = 1;
	while (swapped)
	{
		swapped = 0;
		for (t_list *c = lst; c && c->next; c = c->next)
			if (!cmp(c->data, c->next->data))
			{
				int t = c->data;
				c->data = c->next->data;
				c->next->data = t;
				swapped = 1;
			}
	}
	return (lst);
}
