# ACP BREVET CONTROL TIME CALCULATOR


 ### Author: Makai DeBerry 
 email: Makai.deberry@gmail.com

## FUNCTIONALITY
1. Pick a brevet distance (200,300,400,600,or 1000km), and a starting date and time
2. Enter your controle distances in either miles or kilometers in their respective colums (the rest will appear automatically after you move to the next column)
3. changing the brevet distance or start time will recalculate every entery (no need to re-enter them)
4. The "begins at" time is based on UTC and then is converted to user time. times with no ofset are considered UTC

### Clearifications, Special cases and assumptions

- for any controle before 60km the under 60k controle rule is applied and takes the controle point distance/20 + 1 hour
- For rounding floats it round to the nearest km, for .5 it rounds to the nearest even number. The RUSA desciption on clearifies to round to the nearest minute so I felt the documentation was necessary
- controles at 0 Km: open and close after a 1 hour window
- controles 20% past the brevet distance reflect the same idea as the RUSA table and arent accepted

### Testing

1. The testcases live in the brevets folder and is named "test_acp_times.py"
2. Each case test a specific thing
	- a controle inside a single range
	- 0km controle
	- A final controle at the exact brevet distance
	- a controle a little past the brevet distance
	- A 1000km brevet with a control set going through every range past 600km 
