param (
    [Parameter(Position = 0, Mandatory = $true, HelpMessage = "Specify the environment (dev or prod).")]
    [ValidateSet("dev", "prod")]
    [string] $environment
)

if ($environment -eq "dev") {
    . .\.venv\Scripts\Activate.ps1
    flask.exe run --reload --debugger
}
elseif ($environment -eq "prod") {
    . .\.venv\Scripts\Activate.ps1
    flask.exe run
}
else {
    Write-Host "Invalid environment specified. Use 'dev' or 'prod'."
    Write-Help
}
