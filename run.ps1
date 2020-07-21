write-host "Running"
[int] $hour = get-date -format HH
write-host $hour
while ($hour -gt 8 -or $hour -lt 17) {
	py ./data_show.py;
	start-sleep (60*1);
	./run.ps1
}
