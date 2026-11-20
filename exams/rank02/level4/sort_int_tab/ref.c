void sort_int_tab(int *tab, unsigned int size)
{
	for (unsigned int i = 0; i + 1 < size; i++)
		for (unsigned int j = 0; j + 1 < size - i; j++)
			if (tab[j] > tab[j + 1])
			{
				int t = tab[j];
				tab[j] = tab[j + 1];
				tab[j + 1] = t;
			}
}
