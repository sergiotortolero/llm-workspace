<#
.SYNOPSIS
    Scaffold the standard docs structure (prd / adr / audits) for a project and
    seed it with the shared templates from the orchestrator root.

.PARAMETER ProjectName
    Folder name under Proyectos\, e.g. "Kibo".

.EXAMPLE
    .\scripts\New-ProjectDocs.ps1 -ProjectName "Kibo"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName
)

$ErrorActionPreference = 'Stop'

$root        = Split-Path -Parent $PSScriptRoot          # D:\LLM's
$projectPath = Join-Path $root "Proyectos\$ProjectName"
$templates   = Join-Path $root 'templates'

if (-not (Test-Path $projectPath)) {
    throw "Project folder not found: $projectPath"
}

$folders = @('docs\prd', 'docs\adr', 'docs\audits')
foreach ($f in $folders) {
    $target = Join-Path $projectPath $f
    if (-not (Test-Path $target)) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        Write-Host "  created  $f" -ForegroundColor Green
    } else {
        Write-Host "  exists   $f" -ForegroundColor DarkGray
    }
}

# Seed templates only if absent (never overwrite existing docs)
$seeds = @{
    'templates\prd-template.md'        = 'docs\prd\_TEMPLATE.md'
    'templates\adr-template.md'        = 'docs\adr\_TEMPLATE.md'
    'templates\user-story-template.md' = 'docs\prd\_USER_STORY_TEMPLATE.md'
    'templates\db-audit-template.md'   = 'docs\audits\_TEMPLATE.md'
}
foreach ($src in $seeds.Keys) {
    $from = Join-Path $root $src
    $to   = Join-Path $projectPath $seeds[$src]
    if ((Test-Path $from) -and -not (Test-Path $to)) {
        Copy-Item $from $to
        Write-Host "  seeded   $($seeds[$src])" -ForegroundColor Cyan
    }
}

Write-Host "Done: docs structure ready for '$ProjectName'." -ForegroundColor Yellow
