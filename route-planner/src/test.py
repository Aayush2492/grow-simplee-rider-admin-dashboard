a, b, c = 8, 8, 4

ans = 0

for i in [1, 2, 4, 8]:
    for j in [1, 2, 4, 8]:
        for k in [1, 2, 4]:
            if i >= j >= k:
                ans += i * j * k

print(ans)
print(8 * 8 * 4)
