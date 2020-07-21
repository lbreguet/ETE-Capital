write-host "Running"
[int] $hour = get-date -format HH
while ($hour -gt 8 -or $hour -lt 17) {
	py ./data_show.py
}
