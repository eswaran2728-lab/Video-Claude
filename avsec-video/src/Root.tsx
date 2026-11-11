import {Composition} from 'remotion';
import {Training} from './Training';
import {FPS, H, W, TOTAL_FRAMES} from './meta';

export const Root = () => (
  <Composition id="Training" component={Training} durationInFrames={TOTAL_FRAMES} fps={FPS} width={W} height={H} />
);
