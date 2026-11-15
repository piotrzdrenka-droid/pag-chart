Add-Type -AssemblyName System.Drawing
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$data = Get-Content -Raw (Join-Path $root 'history.json') | ConvertFrom-Json
$ink = [System.Drawing.ColorTranslator]::FromHtml('#0b1523')
$panel = [System.Drawing.ColorTranslator]::FromHtml('#122033')
$gold = [System.Drawing.ColorTranslator]::FromHtml('#f1c75b')
$blue = [System.Drawing.ColorTranslator]::FromHtml('#76b7e5')
$white = [System.Drawing.ColorTranslator]::FromHtml('#f3f5fa')
$muted = [System.Drawing.ColorTranslator]::FromHtml('#b7c4d5')
$grid = [System.Drawing.ColorTranslator]::FromHtml('#2e3d50')
function New-Canvas([int]$w,[int]$h) {
  $b = New-Object System.Drawing.Bitmap $w,$h
  $g = [System.Drawing.Graphics]::FromImage($b)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.Clear($ink)
  return ,@($b,$g)
}
function Draw-Text($g,[string]$s,[float]$x,[float]$y,[float]$size,$color,[bool]$bold=$false) {
  $style = if($bold){[System.Drawing.FontStyle]::Bold}else{[System.Drawing.FontStyle]::Regular}
  $f = New-Object System.Drawing.Font('Arial',$size,$style)
  $br = New-Object System.Drawing.SolidBrush($color)
  $g.DrawString($s,$f,$br,$x,$y)
  $br.Dispose(); $f.Dispose()
}
# Chart 1: every logged paid transaction, grouped into the three payout rounds.
$rounds = @(
  [pscustomobject]@{label='13 OCT'; round='2026-10-13'; pct='FIRST RECORDED ROUND'},
  [pscustomobject]@{label='30 OCT'; round='2026-10-30'; pct='+37.50% VS PREVIOUS'},
  [pscustomobject]@{label='13–14 NOV'; round='2026-11-13/14'; pct='+81.82% VS PREVIOUS'}
)
$summary = New-Canvas 1400 760; $bmp=$summary[0]; $g=$summary[1]
Draw-Text $g 'POLISH ARMAMENTS GROUP' 50 32 28 $gold $true
Draw-Text $g 'ALL DIVIDENDS PAID · LOGGED PAYOUTS' 50 76 38 $white $true
Draw-Text $g '13 OCT — 14 NOV 2026 · GOLD' 50 126 22 $muted $false
Draw-Text $g '975' 50 174 78 $gold $true
Draw-Text $g 'GOLD TOTAL' 258 216 27 $muted $true
$pen=New-Object System.Drawing.Pen($grid,2); $g.DrawLine($pen,50,285,1350,285); $pen.Dispose()
Draw-Text $g 'PAYOUT ROUND' 55 307 18 $muted $true
Draw-Text $g 'AMOUNT' 300 307 18 $muted $true
$baseX=300; $scale=1.05; $barH=52; $ys=@(355,465,575)
for($i=0;$i -lt $rounds.Count;$i++){
  $r=$rounds[$i]; $amount=($data.dividend_distributions | Where-Object round -eq $r.round | Measure-Object amount_gold -Sum).Sum
  $y=$ys[$i]; Draw-Text $g $r.label 55 ($y+3) 25 $white $true
  $count=($data.dividend_distributions | Where-Object round -eq $r.round).Count
  $countLabel=if($count -eq 1){'1 PAYMENT'}else{"$count PAYMENTS"}
  Draw-Text $g $countLabel 55 ($y+34) 16 $muted $false
  $g.FillRectangle((New-Object System.Drawing.SolidBrush($panel)),$baseX,$y,560,$barH)
  $g.FillRectangle((New-Object System.Drawing.SolidBrush($gold)),$baseX,$y,[int]($amount*$scale),$barH)
  Draw-Text $g (('{0:N0} GOLD' -f $amount)) ($baseX+[int]($amount*$scale)+18) ($y+8) 22 $white $true
  Draw-Text $g $r.pct 1070 ($y+13) 18 $(if($i -eq 0){$muted}else{$blue}) $true
}
$pen=New-Object System.Drawing.Pen($grid,2); $g.DrawLine($pen,50,675,1350,675); $pen.Dispose()
Draw-Text $g '13 OCT: 200 · 30 OCT: 75 + 75 + 100 + 25 = 275 · 13–14 NOV: 250 + 250 = 500' 50 686 16 $muted $false
Draw-Text $g 'Observed round spacing: 17 days, then 14–15 days; the charter describes a planned two-week schedule.' 50 715 16 $muted $false
$bmp.Save((Join-Path $root 'pag-dividend-payouts-summary.png'),[System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
# Chart 2: recorded asset value versus asset value plus dividends already paid before each reading.
$rows = @($data.observations | Sort-Object date)
$w=1600; $h=1000; $chart=New-Canvas $w $h; $bmp=$chart[0]; $g=$chart[1]
Draw-Text $g 'POLISH ARMAMENTS GROUP' 55 28 28 $gold $true
Draw-Text $g 'ASSET VALUE + DIVIDENDS PAID' 55 72 40 $white $true
Draw-Text $g 'Vexa displayed asset estimates through 15 NOV 2026 · latest read without report refresh' 55 126 22 $muted $false
# Legend
$g.DrawLine((New-Object System.Drawing.Pen($gold,5)),65,177,115,177); Draw-Text $g 'ASSET VALUE' 128 164 18 $white $true
$g.DrawLine((New-Object System.Drawing.Pen($blue,5)),335,177,385,177); Draw-Text $g 'ASSET VALUE + CUMULATIVE PAID DIVIDENDS' 398 164 18 $white $true
$left=130; $top=230; $right=1490; $bottom=825; $minY=2500.0; $maxY=11000.0
$start=[datetime]'2026-10-09'; $end=[datetime]'2026-11-15'
function X-Pos([datetime]$d){ return $left + (($d-$start).TotalDays/($end-$start).TotalDays)*($right-$left) }
function Y-Pos([double]$v){ return $bottom - (($v-$minY)/($maxY-$minY))*($bottom-$top) }
for($v=3000;$v -le 11000;$v+=2000){$y=Y-Pos $v; $p=New-Object System.Drawing.Pen($grid,1); $g.DrawLine($p,$left,$y,$right,$y); $p.Dispose(); Draw-Text $g ('{0:N0}' -f $v) 48 ($y-12) 18 $muted $false}
$p=New-Object System.Drawing.Pen($grid,2); $g.DrawLine($p,$left,$top,$left,$bottom); $g.DrawLine($p,$left,$bottom,$right,$bottom); $p.Dispose()
$ticks=@(@{d='2026-10-09';label='09 OCT'},@{d='2026-10-13';label='13 OCT'},@{d='2026-10-30';label='30 OCT'},@{d='2026-11-15';label='15 NOV'})
foreach($t in $ticks){$x=X-Pos ([datetime]$t.d); Draw-Text $g $t.label ($x-32) 840 17 $muted $false}
$assetPts=[System.Collections.Generic.List[object]]::new(); $adjPts=[System.Collections.Generic.List[object]]::new()
foreach($o in $rows){
  $date=[datetime]$o.date; $asset=[double]$o.value_gold
  $cum=0.0
  if($o.date -eq '2026-10-13'){$cum=$null}
  elseif($o.date -gt '2026-10-13' -and $o.date -lt '2026-10-30'){$cum=200.0}
  elseif($o.date -ge '2026-10-30' -and $o.date -lt '2026-11-13'){$cum=475.0}
  elseif($o.date -eq '2026-11-13'){$cum=725.0}
  elseif($o.date -eq '2026-11-14'){$cum=725.0}
  elseif($o.date -gt '2026-11-14'){$cum=975.0}
  $assetPts.Add([pscustomobject]@{date=$date;value=$asset;status=$o.status})
  $adj=if($null -eq $cum){$null}else{$asset+$cum}
  $adjPts.Add([pscustomobject]@{date=$date;value=$adj;status=$o.status})
}
function Draw-Series($points,$color,[bool]$dashed=$false){
  $prev=$null
  foreach($pt in $points){
    if($null -eq $pt.value){$prev=$null;continue}
    $x=X-Pos $pt.date; $y=Y-Pos ([double]$pt.value)
    if($null -ne $prev){$p=New-Object System.Drawing.Pen($color,4); if($dashed){$p.DashStyle=[System.Drawing.Drawing2D.DashStyle]::Dash}; $g.DrawLine($p,[single]$prev.x,[single]$prev.y,[single]$x,[single]$y); $p.Dispose()}
    if($pt.status -eq 'estimated_missing_day'){$p=New-Object System.Drawing.Pen($color,3); $g.DrawEllipse($p,[single]($x-6),[single]($y-6),12,12); $p.Dispose()}
    elseif($pt.status -eq 'saved_ui_refresh_unverified'){$b=New-Object System.Drawing.SolidBrush($blue); $g.FillRectangle($b,[single]($x-6),[single]($y-6),12,12); $b.Dispose()}
    else{$b=New-Object System.Drawing.SolidBrush($color); $g.FillEllipse($b,[single]($x-5),[single]($y-5),10,10); $b.Dispose()}
    $prev=[pscustomobject]@{x=$x;y=$y}
  }
}
Draw-Series $assetPts $gold $false
Draw-Series $adjPts $blue $false
$latest=$rows[-1]; $assetNow=[double]$latest.value_gold; $totalNow=$assetNow+975.0
$culture=[System.Globalization.CultureInfo]::GetCultureInfo('en-US')
Draw-Text $g ([string]::Format($culture,'ASSETS {0:N2} G',$assetNow)) 1030 260 20 $gold $true
Draw-Text $g ([string]::Format($culture,'+ PAID 975 G = {0:N2} G',$totalNow)) 1030 292 20 $blue $true
$pen=New-Object System.Drawing.Pen($grid,2); $g.DrawLine($pen,55,885,1545,885); $pen.Dispose()
Draw-Text $g 'Lines connect readings, not extra measurements; no reads are recorded for 23–27 Oct.' 55 896 17 $muted $false
Draw-Text $g '13 Oct reading has no time; adjusted point omitted. Open circles = estimates; square = unverified 22 Oct UI.' 55 920 17 $muted $false
Draw-Text $g 'Asset value + dividends is cumulative, not current assets held by PAG or shareholder profit.' 55 944 17 $muted $false
$bmp.Save((Join-Path $root 'pag-value-incl-dividends-2026-11-15.png'),[System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
Write-Output 'Created pag-dividend-payouts-summary.png and pag-value-incl-dividends-2026-11-15.png'
