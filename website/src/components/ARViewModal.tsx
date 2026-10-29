import React, { useState, useEffect, useRef } from 'react';
import { Camera, X, RefreshCw, Smartphone, Eye, AlertCircle } from 'lucide-react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

interface ARViewModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ARViewModal: React.FC<ARViewModalProps> = ({ isOpen, onClose }) => {
  const [arMode, setArMode] = useState<'model-viewer' | 'camera-overlay'>('model-viewer');
  const [cameraPermission, setCameraPermission] = useState<'prompt' | 'granted' | 'denied'>('prompt');
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [isDoorOpen, setIsDoorOpen] = useState<boolean>(false);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasContainerRef = useRef<HTMLDivElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Three.js instances for camera-overlay
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const leftDoorHingeRef = useRef<THREE.Object3D | null>(null);
  const rightDoorHingeRef = useRef<THREE.Object3D | null>(null);
  const reqIdRef = useRef<number>(0);

  // Stop camera when closing
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (reqIdRef.current) {
      cancelAnimationFrame(reqIdRef.current);
    }
  };

  useEffect(() => {
    if (!isOpen) {
      stopCamera();
    }
    return () => {
      stopCamera();
    };
  }, [isOpen]);

  const startCameraOverlay = async () => {
    setArMode('camera-overlay');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setCameraPermission('granted');
      initOverlayThreeScene();
    } catch (err: any) {
      console.warn('Camera access denied or unavailable:', err);
      setCameraPermission('denied');
      setCameraError(err.message || 'Camera access was denied or not found on this device.');
    }
  };

  const initOverlayThreeScene = () => {
    if (!canvasContainerRef.current) return;
    const container = canvasContainerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0.5, 2.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 0.8, 0);

    const light = new THREE.AmbientLight(0xffffff, 1.8);
    scene.add(light);
    const dir = new THREE.DirectionalLight(0xffffff, 2.0);
    dir.position.set(3, 5, 4);
    scene.add(dir);

    const loader = new GLTFLoader();
    loader.load('./models/Domestic_Refrigerator.glb', (gltf) => {
      const model = gltf.scene;
      scene.add(model);
      model.traverse((child) => {
        if (child.name === '10_Fresh_Food_Door_Assembly') leftDoorHingeRef.current = child;
        if (child.name === '11_Freezer_Door_Assembly') rightDoorHingeRef.current = child;
      });
    });

    let clock = new THREE.Clock();
    const animate = () => {
      reqIdRef.current = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      controls.update();

      if (leftDoorHingeRef.current && rightDoorHingeRef.current) {
        const targetL = isDoorOpen ? THREE.MathUtils.degToRad(78) : 0;
        const targetR = isDoorOpen ? THREE.MathUtils.degToRad(-78) : 0;
        leftDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(leftDoorHingeRef.current.rotation.y, targetL, delta * 4);
        rightDoorHingeRef.current.rotation.y = THREE.MathUtils.lerp(rightDoorHingeRef.current.rotation.y, targetR, delta * 4);
      }

      renderer.render(scene, camera);
    };
    animate();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-black/85 backdrop-blur-md">
      <div className="relative w-full max-w-4xl h-[90vh] bg-[#070d1e] border border-[#1e2e5c] rounded-xl flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#1e2e5c] bg-[#0c1633]">
          <div className="flex items-center gap-2.5">
            <Smartphone className="w-5 h-5 text-[#00e5ff]" />
            <div>
              <h3 className="font-mono text-sm font-bold text-white tracking-wide">
                AUGMENTED REALITY VIEWER
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                WebXR · Scene Viewer (ARCore) · AR Quick Look · Live Camera Overlay
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switcher */}
        <div className="flex border-b border-[#1e2e5c] bg-[#091129] px-4 py-2 gap-2">
          <button
            onClick={() => {
              stopCamera();
              setArMode('model-viewer');
            }}
            className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition ${
              arMode === 'model-viewer'
                ? 'bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/40'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Native Mobile AR (WebXR / QuickLook)
          </button>
          <button
            onClick={startCameraOverlay}
            className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition ${
              arMode === 'camera-overlay'
                ? 'bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/40'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Live Camera Overlay (Any Device)
          </button>
        </div>

        {/* Main Content Area */}
        <div className="relative flex-1 bg-black overflow-hidden flex items-center justify-center">
          {arMode === 'model-viewer' ? (
            <div className="relative w-full h-full flex flex-col items-center justify-center">
              {/* @ts-ignore */}
              <model-viewer
                src="./models/Domestic_Refrigerator.glb"
                alt="Domestic Refrigerator 3D Model"
                ar
                ar-modes="webxr scene-viewer quick-look"
                ar-scale="auto"
                camera-controls
                auto-rotate
                shadow-intensity="1.5"
                environment-image="neutral"
                style={{ width: '100%', height: '100%' }}
              >
                <button
                  slot="ar-button"
                  className="absolute bottom-6 left-1/2 -translate-x-1/2 btn-primary shadow-2xl flex items-center gap-2 py-3 px-6 text-sm"
                >
                  <Eye className="w-4 h-4" />
                  VIEW IN YOUR SPACE (AR)
                </button>
              {/* @ts-ignore */}
              </model-viewer>

              <div className="absolute top-4 left-4 right-4 bg-slate-900/80 backdrop-blur-md border border-slate-700/60 p-3 rounded-lg text-xs font-mono text-slate-300">
                <span className="text-[#00e5ff] font-bold">Mobile AR Instructions:</span>
                <ul className="list-disc ml-5 mt-1 space-y-1 text-slate-300">
                  <li>Android: Chrome with Google Play Services for AR (ARCore) places the life-size refrigerator on your room floor.</li>
                  <li>iPhone / iPad: Tap button to view in AR Quick Look with surface tracking.</li>
                  <li>Laptops/Desktop: Switch to "Live Camera Overlay" tab above.</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="relative w-full h-full overflow-hidden">
              {cameraPermission === 'prompt' && (
                <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-20 bg-[#070d1e]/95">
                  <Camera className="w-12 h-12 text-[#00e5ff] mb-3 animate-pulse" />
                  <h4 className="font-mono text-base font-bold text-white mb-2">
                    CAMERA ACCESS REQUEST
                  </h4>
                  <p className="text-xs text-slate-300 max-w-md mb-5 leading-relaxed font-sans">
                    The camera feed is used strictly to display the refrigerator model in your room live.
                    No images or video recordings are stored, saved, or transmitted.
                  </p>
                  <button onClick={startCameraOverlay} className="btn-primary">
                    GRANT CAMERA PERMISSION & START
                  </button>
                </div>
              )}

              {cameraPermission === 'denied' && (
                <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-20 bg-slate-950/95">
                  <AlertCircle className="w-12 h-12 text-amber-400 mb-3" />
                  <h4 className="font-mono text-base font-bold text-white mb-2">
                    CAMERA PERMISSION DENIED OR BLOCKED
                  </h4>
                  <p className="text-xs text-slate-300 max-w-md mb-4 font-mono">
                    {cameraError}
                  </p>
                  <button
                    onClick={() => setArMode('model-viewer')}
                    className="btn-secondary text-xs"
                  >
                    Switch back to WebAR
                  </button>
                </div>
              )}

              {/* Video background stream */}
              <video
                ref={videoRef}
                playsInline
                muted
                className="absolute inset-0 w-full h-full object-cover"
              />

              {/* 3D Model canvas overlay */}
              <div
                ref={canvasContainerRef}
                className="absolute inset-0 w-full h-full pointer-events-auto"
              />

              {/* Live camera controls */}
              <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between pointer-events-none">
                <div className="bg-black/70 backdrop-blur border border-slate-700/60 px-3 py-1.5 rounded text-xs font-mono text-slate-300">
                  CAMERA OVERLAY MODE · Manual Orbit & Zoom Enabled
                </div>
                <button
                  onClick={() => setIsDoorOpen(!isDoorOpen)}
                  className="pointer-events-auto btn-primary text-xs"
                >
                  {isDoorOpen ? 'Close Doors' : 'Open Doors'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
