#!/usr/bin/env python3
"""Place readable references clear of solder-mask openings and component bodies.
Run after routing; copper and connectivity are untouched. Native DRC is still required.
"""
import math,json,sys
from pathlib import Path
import pcbnew as pcb
from shapely.geometry import box,LineString
from shapely.strtree import STRtree
R=Path(__file__).resolve().parents[1];path=next(R.glob('*.kicad_pcb'));b=pcb.LoadBoard(str(path))
def mm(a):return pcb.ToMM(a)
def rect(it,pad=0):
 bb=it.GetBoundingBox();return box(mm(bb.GetX())-pad,mm(bb.GetY())-pad,mm(bb.GetRight())+pad,mm(bb.GetBottom())+pad)
def vec(x,y):return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
allowed=box(50.2,50.2,149.8,129.8)
# Clip only out-of-board silk segments (antenna module and connector overhangs).
for f in b.GetFootprints():
 for g in list(f.GraphicalItems()):
  if g.GetLayer()!=pcb.F_SilkS or not isinstance(g,pcb.PCB_SHAPE):continue
  if allowed.covers(rect(g)):continue
  if g.GetShape()==pcb.SHAPE_T_SEGMENT:
   a=g.GetStart();c=g.GetEnd();line=LineString([(mm(a.x),mm(a.y)),(mm(c.x),mm(c.y))]).intersection(allowed)
   if line.is_empty or line.geom_type!='LineString':g.SetLayer(pcb.F_Fab)
   else:g.SetStart(vec(*line.coords[0]));g.SetEnd(vec(*line.coords[-1]))
  else:g.SetLayer(pcb.F_Fab)
# Relocate a connector legend that originally crossed its outline.
for t in b.GetDrawings():
 if isinstance(t,pcb.PCB_TEXT) and t.GetText()=='BAT +  /  -':t.SetPosition(vec(65,121))
obstacles=[];bodies=[]
for f in b.GetFootprints():
 for p in f.Pads():
  if p.IsOnLayer(pcb.F_Cu):obstacles.append(rect(p,.16))
 outlines=[rect(g) for g in f.GraphicalItems() if g.GetLayer()==pcb.F_CrtYd]
 if outlines:
  bounds=[a.bounds for a in outlines];bodies.append(box(min(a[0]for a in bounds),min(a[1]for a in bounds),max(a[2]for a in bounds),max(a[3]for a in bounds)))
 for g in f.GraphicalItems():
  if g.GetLayer()==pcb.F_SilkS:obstacles.append(rect(g,.16))
for g in b.GetDrawings():
 if g.GetLayer()==pcb.F_SilkS:obstacles.append(rect(g,.16))
used=[]
tree=STRtree(obstacles+bodies)
# Dense parts first; keep reference closest to its own part when possible.
for f in sorted(b.GetFootprints(),key=lambda f:len(f.GetReference()),reverse=True):
 ref=f.Reference();ref.SetVisible(True);ref.SetTextSize(vec(.8,.8));ref.SetTextThickness(pcb.FromMM(.12));ref.SetTextAngle(pcb.EDA_ANGLE(0,pcb.DEGREES_T))
 pos=f.GetPosition();cx=mm(pos.x);cy=mm(pos.y);old=ref.GetPosition()
 offsets=[(x*.5,y*.5)for x in range(-44,45)for y in range(-44,45)];offsets.sort(key=lambda p:p[0]*p[0]+p[1]*p[1])
 candidates=[(mm(old.x),mm(old.y))]+[(cx+x,cy+y)for x,y in offsets]
 found=False
 for x,y in candidates:
  ref.SetPosition(vec(x,y));rb=rect(ref,.16)
  if allowed.covers(rb) and len(tree.query(rb))==0:used.append(rb);tree=STRtree(obstacles+bodies+used);found=True;break
 if not found:raise RuntimeError('No legal silkscreen position for '+f.GetReference())
pcb.SaveBoard(str(path),b);print('Placed',len(used),'references and clipped overhanging silk; copper untouched.')
