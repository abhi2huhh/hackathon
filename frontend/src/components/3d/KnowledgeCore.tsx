import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Line, OrbitControls } from "@react-three/drei";
import { useMemo, useRef } from "react";
import type { Group } from "three";

function Graph() {
  const ref = useRef<Group>(null);
  const nodes = useMemo(
    () =>
      Array.from({ length: 18 }, (_, i) => {
        const phi = Math.acos(-1 + (2 * i) / 18);
        const theta = Math.sqrt(18 * Math.PI) * phi;
        const r = 1.6;
        return [r * Math.cos(theta) * Math.sin(phi), r * Math.sin(theta) * Math.sin(phi), r * Math.cos(phi)] as [
          number,
          number,
          number,
        ];
      }),
    [],
  );
  const links = useMemo(() => {
    const pairs: Array<[[number, number, number], [number, number, number]]> = [];
    nodes.forEach((a, i) => {
      nodes.forEach((b, j) => {
        if (j <= i) return;
        const d = Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
        if (d < 1.55) pairs.push([a, b]);
      });
    });
    return pairs;
  }, [nodes]);

  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.12;
  });

  return (
    <group ref={ref}>
      {nodes.map((p, i) => (
        <mesh key={i} position={p}>
          <sphereGeometry args={[0.07, 16, 16]} />
          <meshStandardMaterial color={i % 3 === 0 ? "#d7ff3c" : "#efe7d6"} roughness={0.35} />
        </mesh>
      ))}
      {links.map((seg, i) => (
        <Line key={i} points={seg} color="#7c9a82" lineWidth={1} transparent opacity={0.45} />
      ))}
      <mesh>
        <icosahedronGeometry args={[0.55, 0]} />
        <meshStandardMaterial color="#c4a574" wireframe transparent opacity={0.55} />
      </mesh>
    </group>
  );
}

export function KnowledgeCore() {
  const reduce =
    typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mobile = typeof window !== "undefined" && window.innerWidth < 768;
  if (reduce) {
    return (
      <div className="grid h-[380px] place-items-center rounded-[2rem] border border-line bg-panel">
        <p className="font-display text-3xl">Knowledge core</p>
      </div>
    );
  }
  return (
    <div className="h-[380px] overflow-hidden rounded-[2rem] border border-line bg-[#080a09] md:h-[460px]">
      <Canvas camera={{ position: [0, 0, 5.2], fov: 45 }} dpr={mobile ? 1 : 1.5}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[3, 4, 2]} intensity={1.1} color="#d7ff3c" />
        <Float speed={1.2} rotationIntensity={0.25} floatIntensity={0.4}>
          <Graph />
        </Float>
        <OrbitControls enablePan={false} enableZoom={false} autoRotate={!mobile} autoRotateSpeed={0.6} />
      </Canvas>
    </div>
  );
}
