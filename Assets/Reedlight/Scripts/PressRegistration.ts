// Coordinates are centimetres in the launch frame. The viewer initially faces -Z.
export type Point3 = {x:number, y:number, z:number};
export const PRINT = {registerX:16, centreX:8, centreY:-10, referenceDepth:101, nearDepth:76, farDepth:130};
export type Phase = "invitation" | "search" | "printed";
export type Guidance = "look" | "back" | "closer" | "left" | "right" | "higher" | "lower" | "hold" | "ready" | "printed";

function centreAt(depth:number):Point3 {
    const ratio=depth/PRINT.referenceDepth;
    return {x:PRINT.registerX*(1-ratio)+PRINT.centreX*ratio,y:PRINT.centreY*ratio,z:-depth};
}
function projected(eye:Point3, depth:number) {
    const object=centreAt(depth);
    const scale=(-PRINT.referenceDepth-eye.z)/(object.z-eye.z);
    return {
        x: eye.x + (object.x - eye.x) * scale,
        y: eye.y + (object.y - eye.y) * scale,
        printScale: scale * depth / PRINT.referenceDepth
    };
}
export function inspectRegistration(eye:Point3, forward:Point3):{error:number, cue:Guidance} {
    if (eye.z < -27) return {error:Infinity,cue:"back"};
    if (eye.z > 48) return {error:Infinity,cue:"closer"};
    const dx=PRINT.centreX-eye.x, dy=PRINT.centreY-eye.y, dz=-PRINT.referenceDepth-eye.z;
    const magnitude=Math.hypot(dx,dy,dz)*Math.hypot(forward.x,forward.y,forward.z);
    const facing=magnitude>0?(forward.x*dx+forward.y*dy+forward.z*dz)/magnitude:-1;
    if(facing<.90)return {error:Infinity,cue:"look"};
    const near=projected(eye,PRINT.nearDepth), far=projected(eye,PRINT.farDepth);
    const ex=near.x-far.x, ey=near.y-far.y;
    const centreError = Math.hypot(ex, ey);
    // At the same centre, different apparent sizes still split the bird's beak and wing.
    // The outer ink marks reach roughly 20 cm from the centre of the print.
    const edgeDrift = 20 * Math.abs(near.printScale - far.printScale);
    const error = centreError + edgeDrift;
    if (edgeDrift > centreError) return {error, cue: eye.z < 0 ? "back" : "closer"};
    const cue:Guidance=Math.abs(ex)>=Math.abs(ey)?(ex>0?"right":"left"):(ey>0?"higher":"lower");
    return {error,cue};
}
export class PressRegistration {
    phase:Phase="invitation";
    cue:Guidance="look";
    ready=false;
    private dwell=0;
    start(){this.phase="search";this.cue="look";this.ready=false;this.dwell=0;}
    update(eye:Point3,forward:Point3,seconds:number) {
        if(this.phase!=="search")return;
        const {error,cue}=inspectRegistration(eye,forward);
        const threshold=this.ready?2.15:1.45;
        if(error>threshold) {this.ready=false;this.dwell=0;this.cue=cue;return;}
        this.dwell+=Math.max(0,Math.min(seconds,.10));
        this.ready=this.ready||this.dwell>=.25;
        this.cue=this.ready?"ready":"hold";
    }
    takePrint() {
        if(this.phase!=="search"||!this.ready)return false;
        this.phase="printed";this.cue="printed";this.ready=false;return true;
    }
}

