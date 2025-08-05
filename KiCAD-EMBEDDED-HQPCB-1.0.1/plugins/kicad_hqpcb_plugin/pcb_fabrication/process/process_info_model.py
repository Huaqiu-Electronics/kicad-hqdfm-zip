from dataclasses import dataclass

@dataclass
class ProcessInfo:
    bheight: str  # PCB Thickness
    lineweight: str  # Min Trace/Space Outer
    vias: str  # Min Drilled Hole


@dataclass
class ProcessInfoModel:
    bheight: str  # PCB Thickness
    copper: str  # Finished Copper Weight
    lineweight: str  # Min Trace/Space Outer
    vias: str  # Min Drilled Hole
    color: str  # Solder Mask Color
    charcolor: str  # Silkscreen
    cover: str  # Via Process
    spray: str  # Surface Finish
    insidecopper: str = "0"  # Inner Copper Weight
    cjh: str = None  # SurfaceProcessCtrl
