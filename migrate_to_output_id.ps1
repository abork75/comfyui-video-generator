# migrate_to_output_id.ps1
# Opcjonalna migracja: przemianowuje stare pliki {slug}__{stem}__{pid}.png
# na nową konwencję {output_id}.png zgodnie z danymi z YAML projektu.
#
# Uruchom PO restarcie serwera (który auto-przypisze output_id w YAML-u),
# a PRZED ponowną generacją.
#
# Wymaga: Python z modułem PyYAML (pip install pyyaml)

param(
    [Parameter(Mandatory=$true)]
    [string]$RunFile   # np. "RUN_012 - dmuchinj w oponke.yaml"
)

$runsDir = "D:\streamlit_project\comfyui_integration\runs"
$yamlPath = Join-Path $runsDir $RunFile

if (-not (Test-Path $yamlPath)) {
    Write-Host "Nie znaleziono pliku: $yamlPath" -ForegroundColor Red
    exit 1
}

# Wczytaj YAML przez Python
$pyScript = @"
import yaml, json, sys
with open(r'$($yamlPath.Replace("'","\'"))', encoding='utf-8') as f:
    data = yaml.safe_load(f)
slots_data = []
for tile in data.get('pic_flow', []):
    tile_name = tile.get('name', tile.get('id',''))
    out_dir = tile.get('output_dir', '')
    for slot in tile.get('image_slots', []):
        img = slot.get('image', '')
        for p in slot.get('prompts', []):
            slots_data.append({
                'tile': tile_name,
                'image': img,
                'pid': p.get('id',''),
                'output_id': p.get('output_id',''),
                'out_dir': out_dir
            })
print(json.dumps(slots_data))
"@

$json = python -c $pyScript 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Błąd Python: $json" -ForegroundColor Red
    exit 1
}

$prompts = $json | ConvertFrom-Json
Write-Host ""
Write-Host "=== Migracja plików do output_id ===" -ForegroundColor Cyan
Write-Host "Plik: $RunFile" -ForegroundColor Gray
Write-Host ""

$ok = 0; $skip = 0; $notfound = 0

foreach ($p in $prompts) {
    if (-not $p.output_id) {
        Write-Host "  BRAK output_id: tile=$($p.tile) pid=$($p.pid)" -ForegroundColor Yellow
        $skip++
        continue
    }

    $outDir = $p.out_dir
    if (-not (Test-Path $outDir)) { $notfound++; continue }

    # Szukaj starego pliku wg poprzedniej konwencji
    $tileParts = $p.tile.ToLower() -replace '[^a-z0-9_\-]','_' -replace '_+','_'
    $imgStem   = [System.IO.Path]::GetFileNameWithoutExtension($p.image)
    $oldStem   = "${tileParts}__${imgStem}__$($p.pid)"

    $found = $false
    foreach ($ext in @('.png','.jpg','.jpeg','.webp')) {
        $oldPath = Join-Path $outDir "$oldStem$ext"
        $newPath = Join-Path $outDir "$($p.output_id)$ext"
        if (Test-Path $oldPath) {
            if (Test-Path $newPath) {
                Write-Host "  CEL JUŻ ISTNIEJE: $($p.output_id)$ext" -ForegroundColor Yellow
                $skip++
            } else {
                Rename-Item $oldPath $newPath
                Write-Host "  OK  $oldStem$ext" -ForegroundColor Green
                Write-Host "   -> $($p.output_id)$ext" -ForegroundColor DarkGreen
                $ok++
            }
            $found = $true
            break
        }
    }
    if (-not $found) {
        Write-Host "  BRAK PLIKU: $oldStem (tile=$($p.tile) pid=$($p.pid))" -ForegroundColor DarkGray
        $notfound++
    }
}

Write-Host ""
Write-Host "=== Gotowe: $ok przemianowanych, $skip pominiętych, $notfound nieznalezionych ===" -ForegroundColor Cyan
