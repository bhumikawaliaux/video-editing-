import { Composition } from "remotion";
import { Hello } from "./Hello";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Hello"
    component={Hello}
    durationInFrames={60}
    fps={30}
    width={1080}
    height={1920}
  />
);
