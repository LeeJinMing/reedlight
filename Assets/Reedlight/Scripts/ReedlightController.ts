import {PressRegistration, Point3} from "./PressRegistration";
import WorldCameraFinderProvider from "InteractionKit.lspkg/Providers/CameraProvider/WorldCameraFinderProvider";
import {Button} from "UIKit.lspkg/Scripts/Components/Button/Button";
import {ElementContent} from "UIKit.lspkg/Scripts/Components/Content/ElementContent";
import {addContentToElement} from "UIKit.lspkg/Scripts/Components/Content/ElementContentFactory";

@component
export class ReedlightController extends BaseScriptComponent {
    private registration = new PressRegistration();
    private returning = false;
    private anchored = false;
    private camera: Transform;
    private frame: Transform;
    private plates: SceneObject;
    private print: SceneObject;
    private cards: SceneObject;
    private buttonHost: SceneObject;
    private focusTime = 0;
    private focusFired = false;
    private lastPressTime = -2;
    private label: ElementContent;
    private last = "";

    onAwake(): void {
        this.createEvent("OnStartEvent").bind(() => this.setup());
    }

    private setup(): void {
        const cameraComponent = WorldCameraFinderProvider.getInstance().getComponent();
        this.camera = cameraComponent.getTransform();
        this.frame = this.getTransform();
        this.plates = this.child("Fixed Plates");
        this.print = this.child("Registered Print");
        this.cards = this.child("Invitation and Cue");
        const host = this.child("Shared Control");
        this.buttonHost = host;
        const button = host.createComponent(Button.getTypeName()) as Button;
        button.setVariant({theme: "System3", shape: "Capsule", style: "Primary"});
        button.size = new vec3(16, 5.5, 1);
        button.initialize();
        this.label = addContentToElement(host, {text: "Start", textSize: 66});
        button.onTriggerUp.add(() => {
            this.focusFired = true;
            this.focusTime = 0;
            this.press();
        });
        if (global.deviceInfoSystem.isEditor()) {
            let startedOnButton = false;
            const hitsButton = (point: vec2): boolean => {
                const local = host.getTransform().getInvertedWorldTransform();
                const eye = local.multiplyPoint(this.camera.getWorldPosition());
                const rayPoint = local.multiplyPoint(cameraComponent.screenSpaceToWorldSpace(point, 100));
                const ray = rayPoint.sub(eye);
                if (ray.z >= -0.1) return false;
                const distance = -eye.z / ray.z;
                return distance > 0 && Math.abs(eye.x + distance * ray.x) < 8
                    && Math.abs(eye.y + distance * ray.y) < 2.75;
            };
            this.createEvent("TouchStartEvent").bind(event => {
                startedOnButton = hitsButton(event.getTouchPosition());
            });
            this.createEvent("TouchEndEvent").bind(event => {
                if (startedOnButton && hitsButton(event.getTouchPosition())) this.press();
                startedOnButton = false;
            });
        }
        this.refresh();
        this.createEvent("LateUpdateEvent").bind(() => this.update());
    }

    private child(name: string): SceneObject {
        const root = this.getSceneObject();
        for (let i = 0; i < root.getChildrenCount(); i++) {
            const object = root.getChild(i);
            if (object.name === name) return object;
        }
        throw new Error("Missing Reedlight scene object " + name);
    }

    private pose() {
        const inverse = this.frame.getInvertedWorldTransform();
        return {
            eye: inverse.multiplyPoint(this.camera.getWorldPosition()),
            forward: inverse.multiplyDirection(this.camera.forward.uniformScale(-1)),
        };
    }

    private update(): void {
        if (!this.anchored) {
            const back = this.camera.forward;
            this.frame.setWorldPosition(this.camera.getWorldPosition());
            this.frame.setWorldRotation(quat.angleAxis(Math.atan2(back.x, back.z), vec3.up()));
            this.anchored = true;
        }
        const {eye, forward} = this.pose();
        if (this.returning && Math.abs(eye.x) < 3 && Math.abs(eye.y) < 5 && Math.abs(eye.z) < 7) {
            this.returning = false;
        }
        this.registration.update(eye, forward, getDeltaTime());
        this.updateHeadPointing(eye, forward);
        this.refresh();
    }

    // A visitor can select the same physical control by pointing their head at
    // it for one second. Looking at the bird itself never activates the press.
    private updateHeadPointing(eye: Point3, forward: Point3): void {
        const centre = this.buttonHost.getTransform().getLocalPosition();
        const distance = (centre.z - eye.z) / forward.z;
        const inside = forward.z < -0.1 && distance > 0
            && Math.abs(eye.x + distance * forward.x - centre.x) < 4.5
            && Math.abs(eye.y + distance * forward.y - centre.y) < 2.4;
        if (!inside) {
            this.focusTime = 0;
            this.focusFired = false;
        } else if (!this.focusFired && !this.returning) {
            this.focusTime += Math.min(0.1, getDeltaTime());
            if (this.focusTime >= 1) {
                this.focusFired = true;
                this.press();
            }
        }
        const zoom = 1 + 0.10 * Math.min(1, this.focusTime);
        this.buttonHost.getTransform().setLocalScale(new vec3(zoom, zoom, 1));
    }

    private press(): void {
        const now = getTime();
        if (this.returning || !this.anchored || now - this.lastPressTime < 0.4) return;
        this.lastPressTime = now;
        if (this.registration.phase === "invitation") {
            this.registration.start();
            print("[Reedlight] Start");
        } else if (this.registration.phase === "search") {
            const {eye, forward} = this.pose();
            this.registration.update(eye, forward, 0);
            print(this.registration.takePrint() ? "[Reedlight] Print accepted" : "[Reedlight] Print rejected");
        } else {
            this.registration = new PressRegistration();
            this.returning = true;
            print("[Reedlight] Replay");
        }
        this.refresh();
    }

    private refresh(): void {
        const phase = this.registration.phase;
        const printed = phase === "printed";
        const cue = this.returning ? this.returnCue() : phase === "invitation"
            ? "invitation" : this.registration.cue;
        const label = this.returning ? "Return" : phase === "invitation" ? "Start"
            : printed ? "Replay" : this.registration.ready ? "Print" : "Print · Locked";
        const key = cue + "|" + label;
        if (key === this.last) return;
        this.last = key;
        for (let index = 0; index < this.cards.getChildrenCount(); index++) {
            const card = this.cards.getChild(index);
            card.enabled = card.name === cue;
        }
        this.label.text = label;
        this.label.opacity = label === "Print · Locked" || this.returning ? 0.80 : 1;
        this.plates.enabled = !printed;
        this.print.enabled = printed;
    }

    private returnCue(): string {
        const {eye} = this.pose();
        if (eye.x > 3) return "return-left";
        if (eye.x < -3) return "return-right";
        if (eye.z < -7) return "return-back";
        if (eye.z > 7) return "return-closer";
        return eye.y > 0 ? "return-lower" : "return-higher";
    }
}
