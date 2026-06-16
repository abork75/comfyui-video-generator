# rename_modelka2_to_output_id.ps1
# Przemianowuje pliki modelka_2_modele ze starej konwencji na output_id.

$dir = "C:\Users\abork\AppData\Local\CapCut\Videos\muszelka_pliki\obce\oponka\modelka_2_modele"

$map = @{
    "modelka_2__model_bazowy__p0000002.png" = "LPy4a8uQVpXy6iRhPO.png"
    "modelka_2__model_bazowy__p0000003.png" = "mOuEIUEE3erAH0IviR.png"
    "modelka_2__model_bazowy__p0000004.png" = "8oAy9ZlOJ3Zms15Cfz.png"
    "modelka_2__model_bazowy__p0000005.png" = "HBD4jf1IbcCx1VXxue.png"
    "modelka_2__model_bazowy__p0000006.png" = "w8YxHwA9Gn1PSuIbY0.png"
    "modelka_2__model_bazowy__p0000007.png" = "o5cBgrXCM9t2lxUDlX.png"
    "modelka_2__model_bazowy__p0000008.png" = "thEWF66YruFeptzCwy.png"
    "modelka_2__model_bazowy__p0000009.png" = "2NKR2abAe7R7BCmTcJ.png"
    "modelka_2__model_bazowy__p0000010.png" = "68DlcO0wgs21gY5zqm.png"
}

Write-Host ""
Write-Host "=== Migracja modelka_2_modele -> output_id ===" -ForegroundColor Cyan
Write-Host "Dir: $dir" -ForegroundColor Gray
Write-Host ""

$ok = 0; $skip = 0; $notfound = 0

foreach ($entry in $map.GetEnumerator()) {
    $src = Join-Path $dir $entry.Key
    $dst = Join-Path $dir $entry.Value
    if (Test-Path $src) {
        if (Test-Path $dst) {
            Write-Host "  SKIP (exists): $($entry.Value)" -ForegroundColor Yellow
            $skip++
        } else {
            Rename-Item $src $dst
            Write-Host "  OK  $($entry.Key)" -ForegroundColor Green
            Write-Host "   -> $($entry.Value)" -ForegroundColor DarkGreen
            $ok++
        }
    } else {
        Write-Host "  NOT FOUND: $($entry.Key)" -ForegroundColor DarkGray
        $notfound++
    }
}

$orphan = Join-Path $dir "modelka_2__model_bazowy__p0000001.png"
if (Test-Path $orphan) {
    Write-Host ""
    Write-Host "  ORPHAN (not in YAML): modelka_2__model_bazowy__p0000001.png" -ForegroundColor Yellow
    Write-Host "  Delete manually if not needed." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done: $ok renamed, $skip skipped, $notfound not found ===" -ForegroundColor Cyan
