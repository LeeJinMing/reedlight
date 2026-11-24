---
status: draft
---

# Design brief: Reedlight

## The one spatial moment

The visitor shifts sideways until abstract paper cuts on three fixed, world-space planes suddenly register as one kingfisher. The bird is already visible in the layered artwork when the visitor reaches for the separate Print control.

**Entrant’s exact words**

> 我希望观众记住侧移到刚刚好的位置，三层原本看不懂的纸雕突然拼成一只翠鸟的那一瞬间。就按这个方向继续做。

**English translation**

> I want visitors to remember the instant they move sideways to just the right spot and three layers of paper cuts that hadn’t made sense suddenly come together as a kingfisher. Keep going in this direction.

The entrant explicitly approved this creative direction and asked production to continue. The draft status applies to the wording of this document. Choices marked **(default)** are production decisions under the entrant’s delegation of art, theme, and implementation.

## Why it belongs on glasses

- Uses the visitor’s own viewpoint, places the artwork in the room, and leaves their hands free until they choose to print.
- Moving the head sideways makes near fragments cross the view faster than far fragments. The visitor discovers the image by finding a position in the room. The laptop preview can demonstrate the same effect by translating its camera.

## Product or overlay

- Type — a self-contained virtual gallery exhibit with layered paper-cut art **(default)**.
- Sensing — use the tracked viewpoint and a standard pinch on a spatial button. The preview supplies the viewpoint and mouse-driven pinch.
- Preview stand-in — none needed. Preview camera translation drives the same parallax as physical sideways movement on glasses.

## Where things live

- Fix the exhibit in room space relative to the launch pose **(default)**. Place three parallel transparent planes at 76, 101, and 130 cm ahead, with the exhibit centered about 10 cm below launch eye level **(default)**. Fit the artwork within a 60 × 40 cm reference sheet at the middle plane and size the visible marks for the preview field of view **(default)**.
- Author each plane’s artwork from the same composite projected from a viewpoint 16 cm to the right of the launch eye **(default)**. Keep the planes fixed. Use broken silhouettes and distribute recognizable features across the planes so the entry view reads as abstract. Use bright teal and warm cream paper tones that remain visible in the additive preview **(default)**.
- Put one large spatial control at a time just below the exhibit near its right edge, within comfortable reach and clear of the art **(default)**. Place the flat print at the middle plane in the exhibit frame **(default)**.

## Hands and input

- Pinch Start **(default)**. Shift your head or body sideways to find alignment. In Interactive Preview, move the camera laterally at a steady height and heading to reproduce that motion.
- Pinch the separate Print button once the live view is aligned. Require 0.25 seconds within tolerance **(default)**. Use a slightly wider exit tolerance to reduce flicker **(default)**. Recheck the live pose on press and reject presses outside the acceptable registration range. Early presses leave the artwork and current viewpoint intact.
- Pinch Replay to clear the card and restore the three planes. Keep the exhibit fixed and guide the visitor left to the original viewing position with a return marker. Restore the opening prompt and re-arm Print after they reach that position **(default)**.
- Targets are big and highlight when aimed at. Use standard mouse-driven pinch in Interactive Preview. Voice input is out of scope.

## When things show

- At entry, show the separated layers, Start, and the invitation “Step sideways and watch the layers line up.” **(default)** Keep the title and instructions free of any bird reference or silhouette.
- After Start, show a small registration mark with a shape change and brief “Keep moving” hint near the artwork **(default)**. Keep Print visible with an unavailable state until registration is stable. The artwork resolves through parallax as the visitor moves. Readiness changes only the control and cue.
- After a valid press, replace the layered view with a flat card made from the same composite, matching the registered silhouette, orientation, and colors **(default)**. Show Replay in place of Print. Use the return marker only during replay **(default)**.

## Done criteria

Each one can be checked in Lens Studio's preview.

1. Open a fresh Interactive Preview at the entry pose. Read the opening instruction and confirm the three planes look abstract, the controls fit in view, and the prompt leaves the subject a surprise.
2. Pinch Start and try Print at the entry pose and while passing briefly through alignment. No card appears, the planes remain in place, and the visitor can keep moving.
3. With heading and height held steady, translate the actual Preview camera to the right. See the near cuts shift faster than the far cuts and the kingfisher become readable before any press. Hold the correct viewpoint until Print becomes available. Move off alignment and verify Print becomes unavailable beyond the exit tolerance. Looking right from the entry position alone leaves the view misaligned.
4. Return to the correct viewpoint, hold, and pinch Print. One flat card appears with the same silhouette, orientation, and colors as the registered view. Check that stray fragments and duplicated edges are absent, and that Replay is visible and reachable.
5. Pinch Replay. Follow the marker back to the entry viewpoint, confirm the card is gone and the abstract view is restored, then solve and print a second time in the same session.

## Out of scope

- Live scene recognition, voice, multiplayer, persistent anchors, and saving or exporting prints.

## Risks and open questions

- Verify that the entry pose conceals the silhouette, the 16 cm shift is easy to find, and the artwork and control fit together in the SPECS Preview field of view. Tune visible margins and registration tolerance against actual camera movement.
- Comfort over time and real hand-tracking behavior remain feel unproven.

## Build notes for CLAD
- Build for SPECS so it runs and can be demonstrated in Lens Studio's preview. No SPECS device is available.
- Use Spectacles Interaction Kit (SIK) and UI Kit for all interactions, so they work with the mouse in Interactive Preview and with LEAF.
- Build any stand-in exactly as described above, and keep it obvious in the scene.
- Use real-world scale in centimeters. Keep content inside the user's view during the main task.
- The display is additive: black renders as transparent. Don't rely on black or very dark content to be seen; keep text light and readable from where the user stands.
- Get the basic flow working first, then add detail.
- Write LEAF scenarios for each done criterion, run them in preview, and report which pass. Say which criteria have no test.
- Don't record, identify, or follow people.

## After the build: judge it
This part is for you, after CLAD finishes.

1. **Does it work?** Ask your agent which LEAF tests passed and which done criteria have no test.
2. **Walk around it.** Open the preview in Interactive Preview. Use WASD to move, Q and E to go down and up, and right-drag (or hold Shift) to look around. Clicking acts as a pinch. Stand where a user would and look at the task.
3. **Ask the three questions.**
   - Does it use what I'm looking at?
   - Does it put something in my space, where it belongs?
   - Does it free my hands or let me keep my eyes up?
   - Would it be just as good on a phone? If so, what would make it need the glasses?
4. **Check comfort.**
   - Everything I need is in view while I do the task. Nothing sits at the edges, behind me, or stuck to my face.
   - Every control is within reach of someone standing there.
   - Text reads easily from where I stand. No dark UI disappearing.
   - Things show when needed and get out of the way.
5. **Label what you know.** Write "logic proven" next to anything the tests and preview show working, and "feel unproven" next to anything only real glasses could tell you (comfort over time, real hand tracking, real recognition).
6. **Fix with design notes, not code.** Tell your agent what to change in design terms, for example: "Move the step card 15 cm lower and next to the pan. Make the Next button twice as big. Re-run the tests." If a fix takes under a minute, like nudging a panel, do it yourself in the scene.
7. **Submit.** Record a video under 3 minutes of your Lens in the preview, public on YouTube. Make your repo public with your Lens Studio project and this `devpost/` folder. Details are on the hackathon site: https://learn-specs.devpost.com/resources
