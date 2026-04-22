def rabin_karp_search(text, pattern, q=101):
    d = 256
    n, m = len(text), len(pattern)
    if m == 0 or m > n: return []
    p = 0
    t = 0
    h = pow(d, m-1) % q
    results = []

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                results.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % q
            if t < 0: t += q
    return results