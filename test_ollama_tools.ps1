param(
    [string]$Model = 'hermes-small'
)

$ErrorActionPreference = 'Stop'
$request = @{
    model = $Model
    stream = $false
    options = @{ temperature = 0; num_predict = 256 }
    messages = @(
        @{ role = 'user'; content = 'What is the weather in Vienna? Use the provided get_weather tool.' }
    )
    tools = @(
        @{
            type = 'function'
            function = @{
                name = 'get_weather'
                description = 'Get the current weather for a location.'
                parameters = @{
                    type = 'object'
                    properties = @{
                        location = @{ type = 'string'; description = 'City name, for example Vienna.' }
                    }
                    required = @('location')
                }
            }
        }
    )
} | ConvertTo-Json -Depth 12

$response = Invoke-RestMethod -Uri 'http://localhost:11434/api/chat' -Method Post `
    -ContentType 'application/json' -Body $request -TimeoutSec 180
$calls = @($response.message.tool_calls)
if (-not ($calls | Where-Object { $_.function.name -eq 'get_weather' })) {
    throw 'Ollama accepted the request but did not return the expected get_weather tool call.'
}

[pscustomobject]@{
    model = $response.model
    tool_calls = $calls
    done = $response.done
} | ConvertTo-Json -Depth 8
