# -*- coding: utf-8 -*-
# Generate images from Mermaid diagrams in architecture/

Param(
    [string]$OutputDir = "architecture",
    [switch]$Force = $false
)

$ErrorActionPreference = 'Stop'

function Info($msg) { Write-Host ("INFO: " + $msg) }
function Ok($msg)   { Write-Host ("OK: " + $msg) }
function Err($msg)  { Write-Host ("ERROR: " + $msg) }

# Force UTF-8 console encoding (Windows PowerShell 5.1)
try { chcp 65001 | Out-Null } catch {}
$env:PYTHONUTF8 = '1'
[Console]::InputEncoding  = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
$OutputEncoding = New-Object System.Text.UTF8Encoding $false

try {
    # Check if Python is available
    $pythonCmd = "python"
    try {
        $null = & $pythonCmd --version
    } catch {
        Err "Python not found. Please install Python and ensure it's in PATH."
        exit 1
    }

    # Check if render_mermaid.py exists
    $renderScript = "scripts\utils\render_mermaid.py"
    if (-not (Test-Path $renderScript)) {
        Err "render_mermaid.py not found at $renderScript"
        exit 1
    }

    # List of diagrams to generate
    $diagrams = @(
        "architecture_progressive.mmd",
        "api_gateway_components.mmd", 
        "ai_agent_service_components.mmd",
        "data_flow_progressive.mmd",
        "network_architecture.mmd",
        "data_model.mmd",
        "security_architecture.mmd",
        "mvp_architecture.mmd",
        "rabbitmq_workflow.mmd",
        "mvp_services_components.mmd"
    )

    $generated = 0
    $skipped = 0

    foreach ($diagram in $diagrams) {
        $mmdPath = Join-Path $OutputDir $diagram
        if (-not (Test-Path $mmdPath)) {
            Info "Skipping $diagram (not found)"
            $skipped++
            continue
        }

        $baseName = $diagram -replace '\.mmd$', ''
        $pngPath = Join-Path $OutputDir "$baseName.png"
        $svgPath = Join-Path $OutputDir "$baseName.svg"

        # Check if images already exist
        if (-not $Force -and (Test-Path $pngPath) -and (Test-Path $svgPath)) {
            Info "Skipping $diagram (images exist, use -Force to regenerate)"
            $skipped++
            continue
        }

        Info "Generating images for $diagram..."
        
        try {
            # Generate PNG
            & $pythonCmd $renderScript --input $mmdPath --output $pngPath --format png
            if ($LASTEXITCODE -eq 0) {
                Ok "Generated PNG: $pngPath"
            } else {
                Err "Failed to generate PNG for $diagram"
                continue
            }

            # Generate SVG
            & $pythonCmd $renderScript --input $mmdPath --output $svgPath --format svg
            if ($LASTEXITCODE -eq 0) {
                Ok "Generated SVG: $svgPath"
                $generated++
            } else {
                Err "Failed to generate SVG for $diagram"
            }
        } catch {
            Err "Error generating images for $diagram`: $($_.Exception.Message)"
        }
    }

    Ok "Generation complete: $generated generated, $skipped skipped"
    exit 0
}
catch {
    Err $_.Exception.Message
    exit 1
}
