# Define the target directory
$targetDirectory = "F:\Local_Repository\Meme-Share\app\static\uploads"

# Delete all files in the target directory and its subdirectories
Get-ChildItem -Path $targetDirectory -Recurse -File | ForEach-Object { Remove-Item $_.FullName -Force }

# Delete all files in the "thumbnails" subdirectory
$thumbnailsDirectory = Join-Path $targetDirectory "thumbnails"
Get-ChildItem -Path $thumbnailsDirectory -File | ForEach-Object { Remove-Item $_.FullName -Force }

Write-Host "All files deleted successfully!"
