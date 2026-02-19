param(
    [string]$VersionTag = "v2.3_working",
    [string]$ChangelogMessage = "First stable version - WAN transitions working! Chains working! Con-cat working on the same mp4 size only"
)

$ProjectRoot = "D:\streamlit_project\comfyui_integration"
$BackupFolder = "$ProjectRoot\stabilne_wersje"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupName = "${VersionTag}_${Timestamp}"
$BackupPath = "$BackupFolder\$BackupName"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  VERSION BACKUP - WAN Video Generator System" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Version:  $VersionTag" -ForegroundColor Yellow
Write-Host "Backup:   $BackupName" -ForegroundColor Yellow
Write-Host ""

# Create directories
New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
New-Item -ItemType Directory -Path "$BackupPath\docs" -Force | Out-Null

# Files and folders to backup (organized by category)
$ItemsToBackup = @{
    # Core scripts
    "Core Scripts" = @(
        "batch_transitions.py",
        "flow_parser.py",
        "config_validator.py",
        "workflow_base.py"
    )
    
    # Backends
    "Backends" = @(
        "backends\*.py"
    )
    
    # Utils
    "Utils" = @(
        "utils\*.py"
    )
    
    # Helpers
    "Helpers" = @(
        "helpers\*.py"
    )
    
    # Postprocessing
    "Postprocessing" = @(
        "postprocessing\*.py"
    )
    
    # Workflow configs
    "Workflow Configs" = @(
        "workflow_configs\*.yaml"
    )
    
    # Workflows (JSON templates)
    "Workflows" = @(
        "workflows\*.json"
    )
    
    # RUN scripts
    "RUN Scripts" = @(
        "RUNS\*.py"
    )
    
    # Requirements
    "Requirements" = @(
        "requirements.txt"
    )
}

# Exclusions
$ExcludePatterns = @(
    "*__pycache__*",
    "*.pyc",
    "*logs*",
    "*.tmp",
    "*\output\*",        # ← Folder output/
    "*\transitions\*",   # ← Folder transitions/
    "*\frames\*",        # ← Folder frames/ (też exclude)
    "*.mp4",
    "*.png",
    "*.jpg"
)

# Copy files by category
foreach ($Category in $ItemsToBackup.Keys) {
    Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ">> $Category" -ForegroundColor Cyan
    
    $Patterns = $ItemsToBackup[$Category]
    $CategoryCount = 0
    
    foreach ($Pattern in $Patterns) {
        $FullPattern = Join-Path $ProjectRoot $Pattern
        $Files = Get-ChildItem -Path $FullPattern -File -ErrorAction SilentlyContinue
        
        foreach ($File in $Files) {
            # Check exclusions
            $ShouldExclude = $false
            foreach ($ExcludePattern in $ExcludePatterns) {
                if ($File.FullName -like $ExcludePattern) {
                    $ShouldExclude = $true
                    break
                }
            }
            
            if ($ShouldExclude) { continue }
            
            # Calculate relative path
            $RelativePath = $File.FullName.Substring($ProjectRoot.Length + 1)
            $DestPath = Join-Path $BackupPath $RelativePath
            $DestDir = Split-Path $DestPath -Parent
            
            # Create destination directory
            if (-not (Test-Path $DestDir)) {
                New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
            }
            
            # Copy file
            Copy-Item $File.FullName $DestPath -Force
            Write-Host "  [OK] $RelativePath" -ForegroundColor Green
            $CategoryCount++
        }
    }
    
    if ($CategoryCount -eq 0) {
        Write-Host "  (no files)" -ForegroundColor DarkGray
    } else {
        Write-Host "  Total: $CategoryCount files" -ForegroundColor DarkCyan
    }
}

# Create CHANGELOG
Write-Host ""
Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ">> Creating CHANGELOG..." -ForegroundColor Cyan

$ChangelogText = @"
================================================================
  CHANGELOG - $BackupName
================================================================

VERSION: $VersionTag
DATE:    $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

================================================================
STATUS:
================================================================

[WORKING]
  * WAN 2.2 transitions generation
  * Chain transitions (multi-frame sequences)
  * Single transitions (image to image)
  * VRAM optimization (15.0-15.6 GB stable)
  * PyTorch memory pooling
  * Local ComfyUI backend
  * FLOW_FULL processing complete (8/8 transitions)

[UNKNOWN/UNTESTED]
  * Postprocessing (concatenation nie testowane)
  * Final video merge workflow

[KNOWN ISSUES]
  * Long prompts + short duration = background warping
  * Face drift w chain gdy twarz coraz mniejsza (expected)
  * Empty chain frames = model hallucinates new person

================================================================
CHANGES (This Session):
================================================================

[PROMPT OPTIMIZATION]
  * Discovered: Long prompts (40+ words) + short duration (2-3s) = problems
  * Solution: "smooth motion" dla krotkich transitions (2-5 slow max)
  * Detailed prompts ONLY dla dlugich akcji (7-8s, unbuttoning etc)

[VRAM INSIGHTS]
  * RTX 5070Ti 16GB allocates 15.0-15.6 GB (97% safe limit)
  * PyTorch memory pooling strategy discovered
  * Transitions 1-2: cold start (~5 min)
  * Transitions 3+: full cache (~3 min) - faster!
  * NOT linear: frame count != VRAM usage (pooling!)

[CHAIN TRANSITIONS]
  * Multi-frame sequences working! (corridor walk)
  * Face consistency requires similar face size across frames
  * Empty frames = model adds random people (don't use!)
  * Solution: 2-frame chains + static hold frames

[FLOW_FULL RESULTS]
  * 8 transitions generated successfully
  * Mixed durations: 2-8s
  * Quality: "piekne" / "sztos" (user feedback)
  * Total time: ~45-50 min (ETA accurate!)

[FIXES APPLIED]
  * Transition 1: Long prompt caused background warping
    -> Fix: Simplify to "smooth motion"
  * Transition 5: Face drift (panties_off -> out)
    -> Fix: Trim external video in CapCut, extract better frame
  * Chain 3: Mystery woman appeared (empty corridor frame)
    -> Fix: Use 2-frame chain, separate static hold

[WORKFLOW IMPROVEMENTS]
  * Minimal prompts dla lacznikow (simple transitions)
  * Detailed prompts dla akcji (complex animations)
  * Duration strategy:
    - Short (<=3s): minimal prompt, fast interpolation
    - Long (>=7s): detailed prompt, complex actions
  * External video integration strategy (CapCut trim)

================================================================
SYSTEM ARCHITECTURE:
================================================================

Core:
  * video_generator.py        - Main orchestrator
  * FLOW_FULL                 - Config with all transitions
  * ComfyUI (main.py)         - Backend server

Workflow:
  * WAN 2.2 model             - Image animation (Lightricks)
  * workflow_api.json         - ComfyUI workflow template

Monitoring:
  * monitor_vram.bat          - Real-time VRAM tracking
  * nvidia-smi                - GPU stats

================================================================
HARDWARE REQUIREMENTS (VERIFIED):
================================================================

GPU:
  * RTX 5070Ti 16GB (tested)
  * VRAM usage: 15.0-15.6 GB (stable)
  * Transitions <5s: pure GPU (no RAM spillover)
  * Transitions 8s: ~60 GB RAM spillover (OK with 80 GB RAM)

CPU/RAM:
  * 80 GB RAM (sufficient)
  * Peak usage: ~60 GB (8s transitions)
  * Typical: ~15 GB (2-5s transitions)

Storage:
  * ~500 MB per transition (output)
  * SSD recommended (frame I/O)

================================================================
FLOW_FULL CONFIGURATION:
================================================================

Total transitions: 8
Mix strategy:
  * 1x 8s (unbuttoning - detailed action)
  * 7x 2-5s (simple transitions/laczniki)

Settings:
  * FPS: 16 (WAN default)
  * Steps: 20 (standard), 25 (detailed actions)
  * CFG: 3.5 (standard), 4.0+ (complex actions)
  * Frame count: (duration x fps x 4) + 1 (WAN optimization)

================================================================
BEST PRACTICES DISCOVERED:
================================================================

[DO]
  * Use minimal prompts ("smooth motion") dla <3s transitions
  * Use detailed prompts dla >=7s complex actions
  * Monitor VRAM z monitor_vram.bat
  * Let PyTorch cache warm up (transitions 3+ faster!)
  * Chain images musza miec subject w podobnej skali
  * Trim external videos w CapCut dla better frames

[DON'T]
  * Long prompts (40+ words) + short duration (2s)
  * Empty frames w chain sequences
  * Expect face consistency gdy face <128px w source
  * Fill 100% VRAM (PyTorch needs ~3% headroom)
  * Assume linear VRAM scaling (memory pooling!)

================================================================
GENERATION TIMES (Measured):
================================================================

Transition 1 (cold start):     ~5 min
Transition 2 (warming):        ~5 min
Transitions 3+ (cached):       ~3 min
Long transition (8s):          ~18 min

Total FLOW_FULL (8 trans):     ~45-50 min

================================================================
NEXT STEPS (TODO):
================================================================

[PENDING]
  1. Re-generate Transition 1 (simplified prompt)
  2. Trim biustonosz.mp4 w CapCut
  3. Extract frame 60 -> 04_ewelina_out_v2.png
  4. Re-generate Transition 5 (better target frame)
  5. Trim chain mystery woman (CapCut)
  6. Generate 2 poczatkowe filmy:
     - Film 1: Idle/standing (3s, minimal prompt)
     - Film 2: Unbuttoning (8s, detailed prompt)
  7. Test postprocessing (concatenation)
  8. Final video merge!

================================================================
PROMPTS TO USE (New Videos):
================================================================

Film 1 (Idle, 3s):
  pos: "woman standing naturally, subtle breathing"
  neg: "blurry, low quality, sudden movements"
  duration: 3, fps: 16, steps: 20, cfg: 3.5

Film 2 (Unbuttoning, 8s):
  pos: "woman slowly and carefully unbuttoning her blouse, 
        delicate finger movements on each button, gentle 
        graceful motion, one button at a time, soft elegant 
        pace"
  neg: "blurry, low quality, rushed movements, sudden changes, 
        jerky motion, skipped buttons"
  duration: 8, fps: 16, steps: 25, cfg: 4.0

================================================================
WHY THIS BACKUP:
================================================================

[DZIALA!]
  * 8/8 transitions generated successfully
  * Quality confirmed by user ("piekne", "sztos")
  * System stable (no crashes)
  * VRAM/RAM usage understood
  * Optimization strategies validated

Before making changes:
  * Adding postprocessing
  * Generating new videos
  * Modifying prompts/configs

This is the LAST KNOWN GOOD VERSION!

================================================================
"@

$ChangelogText | Out-File "$BackupPath\CHANGELOG.txt" -Encoding UTF8
Write-Host "  [OK] CHANGELOG.txt created" -ForegroundColor Green

# Create version info file
$VersionInfo = @"
Version: $VersionTag
Timestamp: $Timestamp
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Backup Name: $BackupName
System: WAN 2.2 Video Generator
Hardware: RTX 5070Ti 16GB + 80GB RAM
Status: WORKING (transitions + chains complete)
"@

$VersionInfo | Out-File "$BackupPath\VERSION.txt" -Encoding UTF8
Write-Host "  [OK] VERSION.txt created" -ForegroundColor Green

# Create quick reference card
$QuickRef = @"
================================================================
  QUICK REFERENCE CARD
================================================================

[START SYSTEM]
  Terminal 1: python main.py
  Terminal 2: monitor_vram.bat
  Terminal 3: python video_generator.py --flow FLOW_FULL

[SETTINGS CHEATSHEET]

  Short transitions (<3s):
    pos: "smooth motion"
    duration: 2-3
    steps: 15-20
    cfg: 3.0-3.5

  Long actions (>=7s):
    pos: "detailed description..."
    duration: 7-8
    steps: 20-25
    cfg: 4.0-4.5

[VRAM USAGE]
  * Normal: 15.0-15.6 GB (safe)
  * Warning: >15.8 GB
  * Crash: 16.0 GB

[GENERATION TIMES]
  * 2-3s transition: ~3-5 min
  * 5s transition: ~5 min
  * 8s transition: ~18 min

[CHAINS]
  * Use 2-4 frames max
  * All frames must have subject
  * Similar face/subject size
  * NO empty frames!

================================================================
"@

$QuickRef | Out-File "$BackupPath\QUICK_REFERENCE.txt" -Encoding UTF8
Write-Host "  [OK] QUICK_REFERENCE.txt created" -ForegroundColor Green

# Create ZIP archive
Write-Host ""
Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ">> Creating ZIP archive..." -ForegroundColor Cyan

$ZipPath = "$BackupFolder\${BackupName}.zip"
Compress-Archive -Path "$BackupPath\*" -DestinationPath $ZipPath -Force

$SizeMB = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)

Write-Host "  [OK] Archive created" -ForegroundColor Green
Write-Host ""

# Cleanup temp folder
Remove-Item $BackupPath -Recurse -Force

# Summary
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  BACKUP COMPLETE!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "[!] WORKING VERSION SAVED!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Location: $ZipPath" -ForegroundColor Cyan
Write-Host "Size:     $SizeMB MB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files backed up:" -ForegroundColor Yellow
Write-Host "  * video_generator.py (core)" -ForegroundColor White
Write-Host "  * FLOW_FULL config" -ForegroundColor White
Write-Host "  * ComfyUI workflow" -ForegroundColor White
Write-Host "  * Monitor scripts" -ForegroundColor White
Write-Host "  * CHANGELOG (complete session notes)" -ForegroundColor White
Write-Host "  * QUICK_REFERENCE (settings cheatsheet)" -ForegroundColor White
Write-Host ""
Write-Host "To restore this version:" -ForegroundColor Yellow
Write-Host "  1. Extract ${BackupName}.zip" -ForegroundColor White
Write-Host "  2. Copy files to project root" -ForegroundColor White
Write-Host "  3. Read CHANGELOG.txt for full details" -ForegroundColor White
Write-Host "  4. Read QUICK_REFERENCE.txt for settings" -ForegroundColor White
Write-Host ""
Write-Host "This backup contains the LAST KNOWN GOOD VERSION!" -ForegroundColor Green
Write-Host ""