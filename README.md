# Reedlight

Find the viewpoint from which three paper cuts become one kingfisher. Then pull a print.

## Try it in Lens Studio

1. Extract the whole archive into a writable folder. Open `Reedlight.esproj` in Lens Studio 5.25.0. The first opening imports four Snap packages and compiles TypeScript.
2. Open the SPECS 27 Interactive Preview. Use **Sunlit Room** if choosing a scene. Look toward the paper and widen the Preview panel until the cue and button are both visible.
3. Click **Start**, or aim the centre of the view at Start for one second. In the editor, right-drag to look around. Look up at the layers. With the Preview panel focused, move right with **D**, using short movements near alignment. Use **A** if the cue points left. Keep roughly the same height and distance.
4. Stop when the eye, beak and feathers meet. The card reads **Aligned. Pull your print**. Look at the assembled bird, then select **Print**. To try again, select **Replay** and move left to the starting position.

The target position is approximately 16 cm right of the launch point. For an exact replay with the editor’s native camera tools, use the poses in the verification notes. The exhibit runs locally in the preview.

## Project contents

The scene, original textures and TypeScript are in `Assets/`. Snap’s template packages are in `Packages/`. `art-source/make-plates.py` generates the transparent artwork and a reference glTF model. Run it before `make-cover.py`. `make-placards.py` draws the cue cards. The original artwork tools used Python 3.13.1, Pillow 12.3.0 and Windows fonts.

[Devpost Learn design brief](devpost/design-brief.md) · [Editor walkthrough](devpost/verification.md) · [Credits](CREDITS.md)
