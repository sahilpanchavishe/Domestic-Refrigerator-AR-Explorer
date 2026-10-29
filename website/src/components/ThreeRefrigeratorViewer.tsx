import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

interface ThreeViewerProps {
  selectedComponentId: string | null;
  onSelectComponent: (id: string | null) => void;
  isDoorOpen: boolean;
  onToggleDoor: (open: boolean) => void;
  showLabels: boolean;
  showFlow: boolean;
  isCameraActive: boolean;
  explodeFactor: number;
  filterCategory: string;
}

interface CalloutAnchor {
  id: string;
  num: number;
  label: string;
  type: 'major' | 'minor' | 'heat_out' | 'heat_in';
  anchor: THREE.Vector3;
}

export const ThreeRefrigeratorViewer: React.FC<ThreeViewerProps> = ({
  selectedComponentId,
  onSelectComponent,
  isDoorOpen,
  onToggleDoor,
  showLabels,
  showFlow,
  isCameraActive,
  explodeFactor,
  filterCategory
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [projectedCallouts, setProjectedCallouts] = useState<{ id: string; num: number; label: string; type: string; x: number; y: number; visible: boolean }[]>([]);

  // Three.js internal references
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const modelRootRef = useRef<THREE.Group | null>(null);

  // Door hinge nodes
  const leftDoorHingeRef = useRef<THREE.Object3D | null>(null);
  const rightDoorHingeRef = useRef<THREE.Object3D | null>(null);

  // Groups and original positions for explode view
  const groupsMapRef = useRef<Map<string, THREE.Object3D>>(new Map());
  const initialPositionsRef = useRef<Map<string, THREE.Vector3>>(new Map());
  const originalMaterialsRef = useRef<Map<THREE.Mesh, THREE.Material | THREE.Material[]>>(new Map());

  // Flow animation curve & particles
  const flowParticlesRef = useRef<THREE.Points | null>(null);

  // Animation frame handle
  const reqIdRef = useRef<number>(0);

  // 3D Anchor positions for floating screen callouts
  const calloutAnchors: CalloutAnchor[] = [
    { id: '01_Compressor', num: 1, label: 'Compressor', type: 'major', anchor: new THREE.Vector3(-0.25, 0.35, -0.42) },
    { id: '02_Condenser_Coil', num: 2, label: 'Condenser', type: 'major', anchor: new THREE.Vector3(0.0, 1.05, -0.48) },
    { id: '03_Capillary_Tube', num: 3, label: 'Expansion Device', type: 'major', anchor: new THREE.Vector3(0.28, 0.55, -0.32) },
    { id: '04_Evaporator_Unit', num: 4, label: 'Evaporator', type: 'major', anchor: new THREE.Vector3(0.22, 1.48, 0.05) },
    { id: '05_Filter_Drier', num: 5, label: 'Filter-Drier', type: 'minor', anchor: new THREE.Vector3(0.28, 0.35, -0.38) },
    { id: '06_Condenser_Fan', num: 6, label: 'Condenser Fan', type: 'minor', anchor: new THREE.Vector3(0.32, 0.38, -0.44) },
    { id: '08_Cabinet_Body', num: 8, label: 'Cabinet PUF', type: 'minor', anchor: new THREE.Vector3(-0.52, 1.35, 0.0) },
    { id: '10_Fresh_Food_Door_Assembly', num: 10, label: 'Fresh Door', type: 'minor', anchor: new THREE.Vector3(-0.55, 0.95, 0.45) },
    { id: '11_Freezer_Door_Assembly', num: 11, label: 'Freezer Door', type: 'minor', anchor: new THREE.Vector3(0.55, 0.95, 0.45) },
    { id: 'heat_out', num: 0, label: 'Q out · heat rejected', type: 'heat_out', anchor: new THREE.Vector3(-0.35, 1.15, -0.52) },
    { id: 'heat_in', num: 0, label: 'Q in · heat absorbed', type: 'heat_in', anchor: new THREE.Vector3(0.42, 1.45, 0.15) }
  ];

  // Explode vector map
  const explodeOffsets: Record<string, THREE.Vector3> = {
    '01_Compressor': new THREE.Vector3(-0.35, 0, -0.55),
    '02_Condenser_Coil': new THREE.Vector3(0, 0, -0.85),
    '03_Capillary_Tube': new THREE.Vector3(0.35, 0.15, -0.45),
    '04_Evaporator_Unit': new THREE.Vector3(0, 0.35, 0.5),
    '05_Filter_Drier': new THREE.Vector3(0.45, -0.15, -0.35),
    '06_Condenser_Fan': new THREE.Vector3(0.55, 0, -0.65),
    '07_Refrigerant_Lines': new THREE.Vector3(-0.25, 0, -0.35),
    '09_Shelves_And_Drawers': new THREE.Vector3(0, 0.65, 0.25),
    '10_Fresh_Food_Door_Assembly': new THREE.Vector3(-0.7, 0.2, 0.55),
    '11_Freezer_Door_Assembly': new THREE.Vector3(0.7, 0.2, 0.55),
    '12_Rear_Ventilation_Grille': new THREE.Vector3(0, 0, -1.1),
    '13_Thermostat_Electrical': new THREE.Vector3(-0.5, 0.3, 0.2)
  };

  // Setup Camera Video Stream when isCameraActive changes
  useEffect(() => {
    let stream: MediaStream | null = null;
    if (isCameraActive && videoRef.current) {
      navigator.mediaDevices?.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } }
      })
      .then((s) => {
        stream = s;
        if (videoRef.current) {
          videoRef.current.srcObject = s;
          videoRef.current.play();
        }
        if (sceneRef.current && rendererRef.current) {
          sceneRef.current.background = null;
          rendererRef.current.setClearColor(0x000000, 0);
        }
      })
      .catch((err) => {
        console.warn('Camera overlay error:', err);
      });
    } else {
      if (videoRef.current) {
        const s = videoRef.current.srcObject as MediaStream;
        s?.getTracks().forEach((track) => track.stop());
        videoRef.current.srcObject = null;
      }
      if (sceneRef.current && rendererRef.current) {
        sceneRef.current.background = new THREE.Color(0xf8fafc);
        rendererRef.current.setClearColor(0xf8fafc, 1);
      }
    }

    return () => {
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, [isCameraActive]);

  // Handle Zoom & Reset Custom Events
  useEffect(() => {
    const handleReset = () => {
      if (cameraRef.current && controlsRef.current) {
        cameraRef.current.position.set(2.4, 1.4, 2.6);
        controlsRef.current.target.set(0, 0.95, 0);
        controlsRef.current.update();
      }
    };

    const handleZoom = (e: any) => {
      if (cameraRef.current) {
        const delta = e.detail || 0;
        cameraRef.current.position.multiplyScalar(1 + delta);
        if (controlsRef.current) controlsRef.current.update();
      }
    };

    window.addEventListener('reset-camera', handleReset);
    window.addEventListener('zoom-camera', handleZoom);
    return () => {
      window.removeEventListener('reset-camera', handleReset);
      window.removeEventListener('zoom-camera', handleZoom);
    };
  }, []);

  // Main Three.js Scene Setup
  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const width = container.clientWidth || 800;
    const height = container.clientHeight || 600;

    // 1. Scene
    const scene = new THREE.Scene();
    scene.background = isCameraActive ? null : new THREE.Color(0xf8fafc);
    sceneRef.current = scene;

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(42, width / (height || 1), 0.1, 100);
    camera.position.set(2.4, 1.4, 2.6);
    cameraRef.current = camera;

    // 3. Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 4. Orbit Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 0.95, 0);
    controls.maxDistance = 7.0;
    controls.minDistance = 0.6;
    controls.maxPolarAngle = Math.PI / 2 + 0.05;
    controlsRef.current = controls;

    // 5. Studio Lighting
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0xe2e8f0, 1.4);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 2.0);
    dirLight.position.set(4, 6, 4);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.bias = -0.0005;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0x00e5ff, 0.8);
    fillLight.position.set(-4, 3, -3);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0xf97316, 1.2);
    rimLight.position.set(0, 2, -5);
    scene.add(rimLight);

    // Ground Plane with contact shadow
    const groundGeo = new THREE.PlaneGeometry(12, 12);
    const groundMat = new THREE.ShadowMaterial({ opacity: 0.18 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // Subtle Grid on floor
    const grid = new THREE.GridHelper(10, 40, 0xcbd5e1, 0xe2e8f0);
    grid.position.y = 0.001;
    scene.add(grid);

    // 6. Refrigeration Cycle Flow Loop Particles
    const flowPointsCount = 180;
    const flowPositions = new Float32Array(flowPointsCount * 3);
    const flowColors = new Float32Array(flowPointsCount * 3);

    // Define 4-stage closed loop waypoints
    const loopPoints = [
      new THREE.Vector3(-0.25, 0.35, -0.42), // Compressor Discharge
      new THREE.Vector3(-0.25, 0.85, -0.42),
      new THREE.Vector3(0.0, 1.25, -0.48),   // Condenser Top
      new THREE.Vector3(0.28, 0.55, -0.48),   // Condenser Bottom / Filter Drier
      new THREE.Vector3(0.28, 0.55, -0.32),   // Capillary Entrance
      new THREE.Vector3(0.22, 1.48, 0.05),    // Evaporator Coil
      new THREE.Vector3(0.0, 1.48, 0.05),
      new THREE.Vector3(-0.25, 0.45, -0.35)   // Suction Return
    ];
    const curve = new THREE.CatmullRomCurve3(loopPoints, true);

    for (let i = 0; i < flowPointsCount; i++) {
      const t = i / flowPointsCount;
      const pt = curve.getPoint(t);
      flowPositions[i * 3] = pt.x;
      flowPositions[i * 3 + 1] = pt.y;
      flowPositions[i * 3 + 2] = pt.z;

      // Color code based on stage
      if (t < 0.25) {
        // Hot gas: Red
        flowColors[i * 3] = 0.86; flowColors[i * 3 + 1] = 0.15; flowColors[i * 3 + 2] = 0.15;
      } else if (t < 0.5) {
        // Condensing: Orange
        flowColors[i * 3] = 0.92; flowColors[i * 3 + 1] = 0.35; flowColors[i * 3 + 2] = 0.05;
      } else if (t < 0.75) {
        // Cold mixture: Cyan
        flowColors[i * 3] = 0.0; flowColors[i * 3 + 1] = 0.90; flowColors[i * 3 + 2] = 1.0;
      } else {
        // Return vapour: Sky blue
        flowColors[i * 3] = 0.15; flowColors[i * 3 + 1] = 0.55; flowColors[i * 3 + 2] = 0.92;
      }
    }

    const flowGeo = new THREE.BufferGeometry();
    flowGeo.setAttribute('position', new THREE.BufferAttribute(flowPositions, 3));
    flowGeo.setAttribute('color', new THREE.BufferAttribute(flowColors, 3));

    const flowMat = new THREE.PointsMaterial({
      size: 0.045,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending
    });

    const flowPoints = new THREE.Points(flowGeo, flowMat);
    scene.add(flowPoints);
    flowParticlesRef.current = flowPoints;

    // 7. Load Refrigerator Model
    const loader = new GLTFLoader();
    const modelUrl = './models/Domestic_Refrigerator.glb';

    loader.load(
      modelUrl,
      (gltf) => {
        const root = gltf.scene;
        modelRootRef.current = root;
        scene.add(root);

        root.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            originalMaterialsRef.current.set(child, child.material);
          }

          if (child.parent === root && child.name) {
            groupsMapRef.current.set(child.name, child);
            initialPositionsRef.current.set(child.name, child.position.clone());
          }

          if (child.name === '10_Fresh_Food_Door_Assembly') {
            leftDoorHingeRef.current = child;
          }
          if (child.name === '11_Freezer_Door_Assembly') {
            rightDoorHingeRef.current = child;
          }
        });

        setLoading(false);
      },
      undefined,
      (err) => {
        console.error('Failed to load GLB model:', err);
        setLoadError('Unable to load 3D model. Please verify models/Domestic_Refrigerator.glb is present.');
        setLoading(false);
      }
    );

    // 8. Raycast Selection on Tap / Click
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let downPos = { x: 0, y: 0 };

    const handlePointerDown = (e: MouseEvent) => {
      downPos = { x: e.clientX, y: e.clientY };
    };

    const handlePointerUp = (e: MouseEvent) => {
      const dist = Math.hypot(e.clientX - downPos.x, e.clientY - downPos.y);
      if (dist > 5) return; // Dragging orbit, ignore click

      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      if (modelRootRef.current) {
        const intersects = raycaster.intersectObjects(modelRootRef.current.children, true);
        if (intersects.length > 0) {
          let topGroup: THREE.Object3D | null = intersects[0].object;
          while (topGroup && topGroup.parent !== modelRootRef.current && topGroup.parent !== scene) {
            topGroup = topGroup.parent;
          }
          if (topGroup && topGroup.name) {
            onSelectComponent(topGroup.name);
          }
        }
      }
    };

    const dom = renderer.domElement;
    dom.addEventListener('mousedown', handlePointerDown);
    dom.addEventListener('mouseup', handlePointerUp);

    // 9. Resize Observer
    const handleResize = () => {
      if (!containerRef.current || !rendererRef.current || !cameraRef.current) return;
      const w = containerRef.current.clientWidth || 800;
      const h = containerRef.current.clientHeight || 600;
      cameraRef.current.aspect = w / (h || 1);
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);
    const ro = new ResizeObserver(() => handleResize());
    ro.observe(container);

    // 10. Animation Render Loop & Floating Callout Projection
    let clock = new THREE.Clock();
    let flowOffset = 0;

    const animate = () => {
      reqIdRef.current = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      controls.update();

      // Smooth Door Hinge Rotation
      if (leftDoorHingeRef.current && rightDoorHingeRef.current) {
        const targetL = isDoorOpen ? THREE.MathUtils.degToRad(-68) : 0;
        const targetR = isDoorOpen ? THREE.MathUtils.degToRad(68) : 0;
        leftDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(leftDoorHingeRef.current.rotation.y, targetL, delta * 4.5);
        rightDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(rightDoorHingeRef.current.rotation.y, targetR, delta * 4.5);
      }

      // Flow Particles Movement
      if (flowParticlesRef.current) {
        flowParticlesRef.current.visible = showFlow;
        if (showFlow) {
          flowOffset = (flowOffset + delta * 0.12) % 1;
          const posAttr = flowParticlesRef.current.geometry.attributes.position as THREE.BufferAttribute;
          const count = posAttr.count;
          for (let i = 0; i < count; i++) {
            const t = (i / count + flowOffset) % 1;
            const pt = curve.getPoint(t);
            posAttr.setXYZ(i, pt.x, pt.y, pt.z);
          }
          posAttr.needsUpdate = true;
        }
      }

      // Project 3D Anchors to 2D Screen Coordinates for Floating Labels
      if (showLabels && containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const projected = calloutAnchors.map((c) => {
          const v = c.anchor.clone();
          v.project(camera);
          const isBehind = v.z > 1;
          const x = (v.x * 0.5 + 0.5) * rect.width;
          const y = (-(v.y * 0.5) + 0.5) * rect.height;
          return {
            id: c.id,
            num: c.num,
            label: c.label,
            type: c.type,
            x,
            y,
            visible: !isBehind && x > 20 && x < rect.width - 20 && y > 20 && y < rect.height - 20
          };
        });
        setProjectedCallouts(projected);
      } else {
        setProjectedCallouts([]);
      }

      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(reqIdRef.current);
      window.removeEventListener('resize', handleResize);
      ro.disconnect();
      dom.removeEventListener('mousedown', handlePointerDown);
      dom.removeEventListener('mouseup', handlePointerUp);
      renderer.dispose();
    };
  }, [isCameraActive, showFlow, showLabels]);

  // Handle Explode Factor Updates
  useEffect(() => {
    groupsMapRef.current.forEach((obj, name) => {
      const initialPos = initialPositionsRef.current.get(name);
      const offset = explodeOffsets[name];
      if (initialPos && offset) {
        obj.position.x = initialPos.x + offset.x * explodeFactor;
        obj.position.y = initialPos.y + offset.y * explodeFactor;
        obj.position.z = initialPos.z + offset.z * explodeFactor;
      }
    });
  }, [explodeFactor]);

  // Handle Part Highlighting & Category Filtering
  useEffect(() => {
    originalMaterialsRef.current.forEach((origMat, mesh) => {
      let topGroup: THREE.Object3D | null = mesh;
      while (topGroup && topGroup.parent !== modelRootRef.current) {
        topGroup = topGroup.parent;
      }
      const groupName = topGroup?.name || '';

      // Check category filter
      let matchesCategory = true;
      if (filterCategory === 'refrigeration') {
        matchesCategory = ['01_Compressor', '02_Condenser_Coil', '03_Capillary_Tube', '04_Evaporator_Unit', '05_Filter_Drier', '07_Refrigerant_Lines'].includes(groupName);
      } else if (filterCategory === 'cabinet') {
        matchesCategory = ['08_Cabinet_Body', '09_Shelves_And_Drawers', '10_Fresh_Food_Door_Assembly', '11_Freezer_Door_Assembly'].includes(groupName);
      } else if (filterCategory === 'electrical') {
        matchesCategory = ['06_Condenser_Fan', '12_Rear_Ventilation_Grille', '13_Thermostat_Electrical'].includes(groupName);
      }

      if (!matchesCategory) {
        mesh.visible = false;
        return;
      } else {
        mesh.visible = true;
      }

      // Highlight selected
      if (selectedComponentId && groupName === selectedComponentId) {
        mesh.material = new THREE.MeshStandardMaterial({
          color: 0x00e5ff,
          emissive: 0x005577,
          roughness: 0.2,
          metalness: 0.8
        });
      } else {
        mesh.material = origMat;
      }
    });
  }, [selectedComponentId, filterCategory]);

  return (
    <div className="relative w-full h-full bg-[#f8fafc] overflow-hidden">
      {/* Live Webcam Background Video Element */}
      <video
        ref={videoRef}
        playsInline
        muted
        className={`absolute inset-0 w-full h-full object-cover z-0 pointer-events-none transition-opacity duration-300 ${
          isCameraActive ? 'opacity-100' : 'opacity-0'
        }`}
      />

      {/* Three.js Canvas Container */}
      <div ref={containerRef} className="absolute inset-0 z-10 cursor-grab active:cursor-grabbing" />

      {/* Floating 3D Callout Overlays (Matches VCR-AR-Explorer Reference Style) */}
      {showLabels && !loading && (
        <div className="absolute inset-0 z-15 pointer-events-none">
          {projectedCallouts.map((c) => {
            if (!c.visible) return null;
            const isSelected = selectedComponentId === c.id;

            if (c.type === 'heat_out') {
              return (
                <div
                  key={c.id}
                  style={{ transform: `translate(${c.x}px, ${c.y}px)` }}
                  className="absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 bg-[#dc2626] text-white px-2 py-0.5 rounded text-[10px] font-mono font-bold tracking-tight shadow-md flex items-center gap-1 cursor-pointer hover:scale-105 transition"
                  onClick={() => onSelectComponent('02_Condenser_Coil')}
                >
                  <span>Q out · heat rejected</span>
                </div>
              );
            }

            if (c.type === 'heat_in') {
              return (
                <div
                  key={c.id}
                  style={{ transform: `translate(${c.x}px, ${c.y}px)` }}
                  className="absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 bg-[#0284c7] text-white px-2 py-0.5 rounded text-[10px] font-mono font-bold tracking-tight shadow-md flex items-center gap-1 cursor-pointer hover:scale-105 transition"
                  onClick={() => onSelectComponent('04_Evaporator_Unit')}
                >
                  <span>Q in · heat absorbed</span>
                </div>
              );
            }

            if (c.type === 'major') {
              return (
                <div
                  key={c.id}
                  style={{ transform: `translate(${c.x}px, ${c.y}px)` }}
                  className={`absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 px-2.5 py-0.5 rounded-full border shadow-md flex items-center gap-1.5 cursor-pointer hover:scale-105 transition ${
                    isSelected
                      ? 'bg-[#0f172a] text-white border-[#0f172a]'
                      : 'bg-white text-slate-800 border-[#ea580c]'
                  }`}
                  onClick={() => onSelectComponent(c.id)}
                >
                  <span className={`w-4 h-4 rounded-full text-[9px] font-mono font-bold flex items-center justify-center ${
                    isSelected ? 'bg-white text-slate-900' : 'bg-[#ea580c] text-white'
                  }`}>
                    {c.num}
                  </span>
                  <span className="text-[11px] font-semibold whitespace-nowrap">{c.label}</span>
                </div>
              );
            }

            // Minor circular badge
            return (
              <div
                key={c.id}
                style={{ transform: `translate(${c.x}px, ${c.y}px)` }}
                className={`absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 w-6 h-6 rounded-full border shadow-md flex items-center justify-center font-mono font-bold text-[10px] cursor-pointer hover:scale-110 transition ${
                  isSelected
                    ? 'bg-[#0f172a] text-white border-[#0f172a]'
                    : 'bg-white text-slate-800 border-slate-400 hover:border-slate-800'
                }`}
                onClick={() => onSelectComponent(c.id)}
                title={c.label}
              >
                {c.num}
              </div>
            );
          })}
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-white/90 backdrop-blur-sm z-30">
          <div className="w-10 h-10 border-4 border-[#0284c7] border-t-transparent rounded-full animate-spin mb-3" />
          <p className="font-mono text-xs font-bold tracking-wider text-slate-800">
            LOADING DOMESTIC REFRIGERATOR 3D ASSET...
          </p>
          <span className="text-[11px] text-slate-500 font-mono mt-1">165 Nodes · Dual Hinges · glTF 2.0</span>
        </div>
      )}

      {/* Error State */}
      {loadError && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-red-50 p-6 text-center z-30">
          <p className="text-red-700 font-mono text-xs mb-2 font-bold">{loadError}</p>
        </div>
      )}
    </div>
  );
};
