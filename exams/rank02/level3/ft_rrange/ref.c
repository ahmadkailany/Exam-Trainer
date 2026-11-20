#include <stdlib.h>
int *ft_rrange(int start, int end)
{
	int n = (start > end ? start - end : end - start) + 1;
	int *t = malloc(sizeof(int) * n);
	int step = end > start ? -1 : 1;
	if (!t)
		return (NULL);
	for (int i = 0; i < n; i++)
		t[i] = end + i * step;
	return (t);
}
