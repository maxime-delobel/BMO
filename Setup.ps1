Write-Host "This script will set the necessary environment variables for BMO to work"
Write-Host "First, make an API key on Google AI Studio, see README.MD for instructions"
$api_key = Read-Host -Prompt "Paste the API key:"
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "$api_key", "User")
Write-Host "All done! Restart IDE (VsCode) for changes to take effect"
