# Reedlight preview verification

## Reproduce the reveal

The recorded walkthrough used Lens Studio 5.25.0.26111423, SPECS 27 Interactive Preview and the Sunlit Room environment. The editor compiled the TypeScript and imported the project from a writable folder. The camera poses below are in centimetres relative to the launch position. In the native camera tool, keep roll at zero and use a target for **lookAt**.

| Step | Preview input | Visible result |
|---|---|---|
| Enter | At the origin, look toward (0, −10.6, −101). | Three sets of disconnected paper cuts. A card explains how to select Start. |
| Start | Aim at (8, −32, −101) for one second, then look back at the paper. | The card asks for a slow shift right. Print is locked. |
| Look for the bird | Translate from x = 0 to x = 16 while keeping y, z and the viewing direction fixed. | The near fragments slide faster than the far ones. The eye, breast and bill meet before the Print control is selected. After a brief hold, the card indicates alignment. |
| Print | At x = 16, aim at (8, −32, −101) again. Then look up. | A single registered print and the Replay control appear. |
| Replay | Look away before aiming at Replay. Return to x = 0. | The layers separate and the opening card returns. |

The visible preview also accepted a direct mouse click on Start. Trying to print at the starting position left the print locked. Five separate automated checks cover directional guidance, the registration position, scale error with depth, facing away, and holding or leaving the registration position.

## Toolchain and evidence

The official Devpost Learn `plan-lens` skill produced the planning file in this folder. The version used was `challengepost/learn-specs` at `5d8bc0800346d38e468c29b15afcb7ca92280005`. Snap CLAD 1.1.0 and the Lens Studio MCP were used to build and inspect the project. The final walkthrough used the editor’s native preview camera and a continuous recording of the displayed preview panel. The English side captions explain the input. [Design brief](design-brief.md) · [Devpost resources](https://learn-specs.devpost.com/resources)

The desktop preview establishes the optical effect and interaction sequence. No physical SPECS device was used. The optional LEAF test runner did not complete in the authoring workspace. Physical hand tracking, optical contrast in real rooms, and wearable comfort remain unverified.
