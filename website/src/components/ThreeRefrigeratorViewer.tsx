import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

interface ThreeViewerProps {
  selectedComponentId: string | null;
  onSelectComponent: (id: string | null) => void;
  isDoorOpen: boolean;
  onToggleDoor: (open: boolean) => void;
  explodeFactor: number;
  isIsolateMode: boolean;
  isCycleFlowActive: boolean;
  cameraPreset: string;
}

export const ThreeRefrigeratorViewer: React.FC<ThreeViewerProps> = ({
  selectedComponentId,
  onSelectComponent,
  isDoorOpen,
  onToggleDoor,
  explodeFactor,
  isIsolateMode,
  isCycleFlowActive,
  cameraPreset
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Three.js internal references
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const modelRootRef = useRef<THREE.Group | null>(null);

  // Door hinge nodes
  const leftDoorHingeRef = useRef<THREE.Object3D | null>(null);
  const rightDoorHingeRef = useRef<THREE.Object3D | null>(null);

  // Component groups cache
  const groupsMapRef = useRef<Map<string, THREE.Object3D>>(new Map());
  const initialPositionsRef = useRef<Map<string, THREE.Vector3>>(new Map());
  const originalMaterialsRef = useRef<Map<THREE.Mesh, THREE.Material | THREE.Material[]>>(new Map());

  // Animation frame handle
  const reqIdRef = useRef<number>(0);

  // Explode vector map
  const explodeOffsets: Record<string, THREE.Vector3> = {
    '01_Compressor': new THREE.Vector3(-0.4, 0, -0.6),
    '02_Condenser_Coil': new THREE.Vector3(0, 0, -0.85),
    '03_Capillary_Tube': new THREE.Vector3(0.3, 0.2, -0.4),
    '04_Evaporator_Unit': new THREE.Vector3(0, 0.35, 0.5),
    '05_Filter_Drier': new THREE.Vector3(0.4, -0.15, -0.35),
    '06_Condenser_Fan': new THREE.Vector3(0.5, 0, -0.65),
    '07_Refrigerant_Lines': new THREE.Vector3(-0.3, 0, -0.4),
    '09_Shelves_And_Drawers': new THREE.Vector3(0, 0.6, 0.3),
    '10_Fresh_Food_Door_Assembly': new THREE.Vector3(-0.65, 0.2, 0.5),
    '11_Freezer_Door_Assembly': new THREE.Vector3(0.65, 0.2, 0.5),
    '12_Rear_Ventilation_Grille': new THREE.Vector3(0, 0, -1.1),
    '13_Thermostat_Electrical': new THREE.Vector3(-0.5, 0.3, 0.2)
  };

  // Setup Three.js scene
  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const width = container.clientWidth || container.parentElement?.clientWidth || window.innerWidth || 800;
    const height = container.clientHeight || container.parentElement?.clientHeight || window.innerHeight || 600;

    // 1. Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x070d1e);
    scene.fog = new THREE.FogExp2(0x070d1e, 0.08);
    sceneRef.current = scene;

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(45, width / (height || 1), 0.1, 100);
    camera.position.set(2.2, 1.4, 2.8);
    cameraRef.current = camera;

    // 3. Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 4. Orbit Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 0.95, 0);
    controls.maxDistance = 6.0;
    controls.minDistance = 0.6;
    controls.maxPolarAngle = Math.PI / 2 + 0.1;
    controlsRef.current = controls;

    // 5. Lighting
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e293b, 1.2);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 2.2);
    dirLight.position.set(4, 6, 4);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 15;
    dirLight.shadow.bias = -0.0005;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0x00e5ff, 0.9);
    fillLight.position.set(-4, 3, -3);
    scene.add(fillLight);

    const rearLight = new THREE.DirectionalLight(0xf97316, 1.2);
    rearLight.position.set(0, 2, -5);
    scene.add(rearLight);

    // Studio ground grid
    const grid = new THREE.GridHelper(10, 40, 0x00e5ff, 0x1e2e5c);
    grid.position.y = 0;
    scene.add(grid);

    const groundGeo = new THREE.PlaneGeometry(12, 12);
    const groundMat = new THREE.ShadowMaterial({ opacity: 0.35 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // 6. Load Refrigerator Model
    const loader = new GLTFLoader();
    const modelUrl = './models/Domestic_Refrigerator.glb';

    loader.load(
      modelUrl,
      (gltf) => {
        const root = gltf.scene;
        modelRootRef.current = root;
        scene.add(root);

        // Traverse and catalog
        root.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            originalMaterialsRef.current.set(child, child.material);
          }

          // Check if it is a major assembly group
          if (child.parent === root && child.name) {
            groupsMapRef.current.set(child.name, child);
            initialPositionsRef.current.set(child.name, child.position.clone());
          }

          // Find door hinges
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
        setLoadError('Unable to load 3D model file. Please ensure models/Domestic_Refrigerator.glb is present.');
        setLoading(false);
      }
    );

    // 7. Click/Touch raycasting for selection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let mouseDownPos = { x: 0, y: 0 };

    const handlePointerDown = (e: MouseEvent) => {
      mouseDownPos = { x: e.clientX, y: e.clientY };
    };

    const handlePointerUp = (e: MouseEvent) => {
      const dist = Math.hypot(e.clientX - mouseDownPos.x, e.clientY - mouseDownPos.y);
      if (dist > 5) return; // Dragged, not click

      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children, true);

      if (intersects.length > 0) {
        let pickedObj: THREE.Object3D | null = intersects[0].object;
        let pickedGroupId: string | null = null;

        while (pickedObj && pickedObj.parent && pickedObj.parent !== scene) {
          if (pickedObj.parent === modelRootRef.current && pickedObj.name) {
            pickedGroupId = pickedObj.name;
            break;
          }
          pickedObj = pickedObj.parent;
        }

        if (pickedGroupId) {
          onSelectComponent(pickedGroupId);
        } else {
          onSelectComponent(null);
        }
      } else {
        onSelectComponent(null);
      }
    };

    const dom = renderer.domElement;
    dom.addEventListener('mousedown', handlePointerDown);
    dom.addEventListener('mouseup', handlePointerUp);

    // 8. Resize observer
    const handleResize = () => {
      if (!containerRef.current || !rendererRef.current || !cameraRef.current) return;
      const w = containerRef.current.clientWidth || containerRef.current.parentElement?.clientWidth || window.innerWidth || 800;
      const h = containerRef.current.clientHeight || containerRef.current.parentElement?.clientHeight || window.innerHeight || 600;
      cameraRef.current.aspect = w / (h || 1);
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);
    const ro = new ResizeObserver(() => handleResize());
    ro.observe(container);

    // Initial tick to guarantee proper sizing once CSS paints
    setTimeout(handleResize, 50);
    setTimeout(handleResize, 200);

    // 9. Animation render loop
    let clock = new THREE.Clock();
    const animate = () => {
      reqIdRef.current = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      controls.update();

      // Smooth door rotation towards target angle
      if (leftDoorHingeRef.current && rightDoorHingeRef.current) {
        const targetAngleL = isDoorOpen ? THREE.MathUtils.degToRad(78) : 0;
        const targetAngleR = isDoorOpen ? THREE.MathUtils.degToRad(-78) : 0;

        leftDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(
          leftDoorHingeRef.current.rotation.y,
          targetAngleL,
          delta * 4.0
        );
        rightDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(
          rightDoorHingeRef.current.rotation.y,
          targetAngleR,
          delta * 4.0
        );
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
  }, []);

  // Update door state animation
  useEffect(() => {
    // Handled in animation loop via isDoorOpen prop
  }, [isDoorOpen]);

  // Handle Explode Factor
  useEffect(() => {
    groupsMapRef.current.forEach((group, id) => {
      const initialPos = initialPositionsRef.current.get(id);
      if (!initialPos) return;

      const offset = explodeOffsets[id];
      if (offset) {
        group.position.copy(initialPos).addScaledVector(offset, explodeFactor);
      }
    });
  }, [explodeFactor]);

  // Handle Component Selection and Isolate Mode
  useEffect(() => {
    if (!modelRootRef.current) return;

    const highlightMat = new THREE.MeshStandardMaterial({
      color: 0x00e5ff,
      emissive: 0x005577,
      emissiveIntensity: 0.6,
      roughness: 0.2,
      metalness: 0.8
    });

    const ghostMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      transparent: true,
      opacity: 0.15,
      roughness: 0.8,
      metalness: 0.1
    });

    groupsMapRef.current.forEach((group, id) => {
      const isSelected = id === selectedComponentId;

      group.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          const original = originalMaterialsRef.current.get(child);
          if (!original) return;

          if (selectedComponentId) {
            if (isSelected) {
              child.material = highlightMat;
            } else if (isIsolateMode) {
              child.material = ghostMat;
            } else {
              child.material = original;
            }
          } else {
            child.material = original;
          }
        }
      });
    });
  }, [selectedComponentId, isIsolateMode]);

  // Handle Camera Presets
  useEffect(() => {
    if (!controlsRef.current || !cameraRef.current) return;
    const camera = cameraRef.current;
    const controls = controlsRef.current;

    switch (cameraPreset) {
      case 'front':
        camera.position.set(0, 0.95, 2.6);
        controls.target.set(0, 0.95, 0);
        break;
      case 'rear':
        camera.position.set(0, 0.95, -2.6);
        controls.target.set(0, 0.95, 0);
        break;
      case 'interior':
        camera.position.set(0, 0.95, 1.6);
        controls.target.set(0, 0.95, 0);
        onToggleDoor(true);
        break;
      case 'compressor':
        camera.position.set(-0.8, 0.4, -1.8);
        controls.target.set(-0.25, 0.35, -0.45);
        break;
      case 'reset':
      default:
        camera.position.set(2.2, 1.4, 2.8);
        controls.target.set(0, 0.95, 0);
        break;
    }
  }, [cameraPreset]);

  return (
    <div className="relative w-full h-full min-h-[460px] bg-[#070d1e] overflow-hidden rounded-lg">
      <div ref={containerRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#070d1e]/90 backdrop-blur-md z-30">
          <div className="w-12 h-12 border-4 border-[#00e5ff] border-t-transparent rounded-full animate-spin mb-4" />
          <p className="font-mono text-sm tracking-wider text-[#00e5ff] animate-pulse">
            LOADING DOMESTIC REFRIGERATOR 3D GEOMETRY...
          </p>
          <span className="text-xs text-slate-400 mt-2 font-mono">165 Nodes · 15 Materials · Dual Hinges</span>
        </div>
      )}

      {/* Error state */}
      {loadError && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-red-950/80 p-6 text-center z-30">
          <p className="text-red-400 font-mono text-sm mb-2">{loadError}</p>
        </div>
      )}

      {/* Instruction watermark */}
      <div className="absolute bottom-3 left-3 pointer-events-none text-[11px] font-mono text-slate-400/80 bg-slate-900/60 px-2.5 py-1.5 rounded border border-slate-800">
        Left Click / Drag: Orbit · Right Click: Pan · Scroll: Zoom · Click Part: Select
      </div>

      {/* Cycle flow indicator */}
      {isCycleFlowActive && (
        <div className="absolute top-3 left-3 pointer-events-none flex items-center gap-2 bg-[#0c1a3b]/85 border border-[#00e5ff]/40 px-3 py-1.5 rounded-full text-xs font-mono text-[#00e5ff] shadow-lg animate-pulse">
          <span className="w-2 h-2 rounded-full bg-[#00e5ff]" />
          REFRIGERATION CYCLE ACTIVE · CONSTANT-ENTHALPY THROTTLING
        </div>
      )}
    </div>
  );
};
