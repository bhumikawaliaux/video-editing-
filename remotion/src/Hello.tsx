import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const Hello: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#111", justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ color: "white", fontSize: 120, fontFamily: "sans-serif", opacity }}>Hello</h1>
    </AbsoluteFill>
  );
};
