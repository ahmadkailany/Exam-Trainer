#include <stddef.h>
size_t ft_strcspn(const char *s, const char *reject)
{
	size_t i = 0;
	while (s[i])
	{
		for (int j = 0; reject[j]; j++)
			if (s[i] == reject[j])
				return (i);
		i++;
	}
	return (i);
}
