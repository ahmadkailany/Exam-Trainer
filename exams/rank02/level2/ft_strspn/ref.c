#include <stddef.h>
size_t ft_strspn(const char *s, const char *accept)
{
	size_t i = 0;
	while (s[i])
	{
		int found = 0;
		for (int j = 0; accept[j]; j++)
			if (s[i] == accept[j])
				found = 1;
		if (!found)
			break ;
		i++;
	}
	return (i);
}
