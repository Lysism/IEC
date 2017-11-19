# Sample Input

```
3 2.53571 1050.0 1050.0
-100.0 350.0 90.0 1.75
350.0 -100.0 0.0 1.75
350.0 800.0 180.0 1.75
```

`3 2.53571 1050.0 1050.0`

* N = 3 (number of lines following, 1<=N<=10)
* t = 2.53571 (local time when all signals have been received)
* x, y = 1050.0, 1050.0 (destination point on plane)

For each signal:

`-100.0 350.0 90.0 1.75`

* x, y = -100.0, 350.0
* D = 90.0 (compass heading [0-360 degrees, 0 is North, 270 is West, 180 is South, 90 is East])
* time = 1.75 (time that this signal was encoded)

Output:

`45 degrees`
