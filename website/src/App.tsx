import React, { useState, useRef, useEffect } from 'react';
import { 
  RotateCcw, 
  Plus, 
  Minus, 
  Tag, 
  Activity, 
  Camera, 
  VideoOff, 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Layers, 
  DoorClosed, 
  DoorOpen, 
  Smartphone, 
  FileText, 
  Type, 
  X, 
  ChevronRight, 
  ChevronLeft,
  CheckCircle,
  GraduationCap,
  Users,
  BookOpen,
  Info
} from 'lucide-react';
import { ThreeRefrigeratorViewer } from './components/ThreeRefrigeratorViewer';
import { ARViewModal } from './components/ARViewModal';
import { ComponentLibraryModal } from './components/ComponentLibraryModal';
import { CycleExplanationModal } from './components/CycleExplanationModal';
import { AboutModal } from './components/AboutModal';
import componentsData from './data/components.json';

export const App: React.FC = () => {
  // Navigation tabs: '3d' | 'components' | 'cycle' | 'exploded' | 'project' | 'references'
  const [activeTab, setActiveTab] = useState<string>('3d');
  
  // Selected component
  const [selectedComponentId, setSelectedComponentId] = useState<string | null>('01_Compressor');
  
  // Viewer controls
  const [isDoorOpen, setIsDoorOpen] = useState<boolean>(false);
  const [showLabels, setShowLabels] = useState<boolean>(true);
  const [showFlow, setShowFlow] = useState<boolean>(true);
  const [isCameraActive, setIsCameraActive] = useState<boolean>(false);
  const [explodeFactor, setExplodeFactor] = useState<number>(0);
  const [isPlayingCycle, setIsPlayingCycle] = useState<boolean>(false);
  const [cycleStep, setCycleStep] = useState<number>(0);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [fontSizeScale, setFontSizeScale] = useState<number>(1); // 1 = Normal, 1.15 = Large

  // Modals
  const [isAROpen, setIsAROpen] = useState<boolean>(false);
  const [isLibraryOpen, setIsLibraryOpen] = useState<boolean>(false);
  const [isCycleOpen, setIsCycleOpen] = useState<boolean>(false);
  const [isAboutOpen, setIsAboutOpen] = useState<boolean>(false);
  const [isReferencesOpen, setIsReferencesOpen] = useState<boolean>(false);

  // Cycle sequence for "Play cycle"
  const cycleComponents = ['01_Compressor', '02_Condenser_Coil', '03_Capillary_Tube', '04_Evaporator_Unit'];

  useEffect(() => {
    let timer: any;
    if (isPlayingCycle) {
      timer = setInterval(() => {
        setCycleStep((prev) => {
          const next = (prev + 1) % cycleComponents.length;
          setSelectedComponentId(cycleComponents[next]);
          return next;
        });
      }, 3500);
    }
    return () => clearInterval(timer);
  }, [isPlayingCycle]);

  // Handle Tab changes
  const handleTabClick = (tab: string) => {
    setActiveTab(tab);
    if (tab === 'components') {
      setIsLibraryOpen(true);
    } else if (tab === 'cycle') {
      setIsCycleOpen(true);
    } else if (tab === 'exploded') {
      setExplodeFactor(0.65);
      setActiveTab('3d');
    } else if (tab === 'project') {
      setIsAboutOpen(true);
    } else if (tab === 'references') {
      setIsReferencesOpen(true);
    } else if (tab === 'home' || tab === '3d') {
      setExplodeFactor(0);
      setActiveTab('3d');
    }
  };

  const selectedComponent = componentsData.find((c) => c.id === selectedComponentId);
  const currentIndex = componentsData.findIndex((c) => c.id === selectedComponentId);

  const handleNextPart = () => {
    const nextIdx = (currentIndex + 1) % componentsData.length;
    setSelectedComponentId(componentsData[nextIdx].id);
  };

  const handlePrevPart = () => {
    const prevIdx = (currentIndex - 1 + componentsData.length) % componentsData.length;
    setSelectedComponentId(componentsData[prevIdx].id);
  };

  // Font size toggle
  const toggleFontSize = () => {
    setFontSizeScale((prev) => (prev === 1 ? 1.15 : 1));
  };

  return (
    <div 
      className="flex flex-col h-screen w-screen bg-[#f8fafc] text-[#0f172a] overflow-hidden font-sans select-none"
      style={{ fontSize: `${fontSizeScale * 14}px` }}
    >
      {/* ============================================================== */}
      {/* 1. TOP NAVBAR (Matches VCR AR Explorer Reference Header)       */}
      {/* ============================================================== */}
      <header className="flex items-center justify-between px-4 py-2.5 bg-white border-b border-slate-200 z-30 shadow-sm">
        {/* Left: Logo Badge */}
        <div className="flex items-center gap-3">
          <div 
            onClick={() => handleTabClick('3d')}
            className="flex items-center gap-2 cursor-pointer group"
          >
            <div className="bg-[#070d1e] text-white px-2.5 py-1 rounded font-mono font-bold text-sm tracking-wider flex items-center">
              <span className="text-[#00e5ff]">REF</span>
              <span className="text-[#f97316]">/AR</span>
            </div>
            <span className="font-bold text-slate-800 text-sm tracking-tight group-hover:text-[#0284c7] transition">
              AR Explorer
            </span>
          </div>
        </div>

        {/* Center: Navigation Items */}
        <nav className="hidden md:flex items-center gap-1">
          {[
            { id: 'home', label: 'Home' },
            { id: '3d', label: '3D Explorer' },
            { id: 'components', label: 'Components' },
            { id: 'cycle', label: 'Cycle' },
            { id: 'exploded', label: 'Exploded' },
            { id: 'project', label: 'Project' },
            { id: 'references', label: 'References' }
          ].map((tab) => {
            const isActive = activeTab === tab.id || (tab.id === '3d' && activeTab === '3d');
            return (
              <button
                key={tab.id}
                onClick={() => handleTabClick(tab.id)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold transition ${
                  isActive
                    ? 'bg-[#0f172a] text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Right: Actions (AR, PDF, Font Scaling) */}
        <div className="flex items-center gap-2">
          {/* AR Button */}
          <button
            onClick={() => setIsAROpen(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-[#0284c7] text-[#0284c7] hover:bg-[#0284c7]/10 font-mono text-xs font-bold transition shadow-sm"
            title="Launch WebAR / Mobile AR"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span>AR</span>
          </button>

          {/* PDF Brochure Download */}
          <a
            href="./Domestic-Refrigerator-AR-Explorer-Technical-Poster.pdf"
            download
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-slate-300 text-slate-700 hover:text-slate-900 hover:border-slate-400 hover:bg-slate-50 font-mono text-xs font-semibold transition shadow-sm"
            title="Download Technical Poster (PDF)"
          >
            <span>PDF</span>
          </a>

          {/* Font Size Adjuster */}
          <button
            onClick={toggleFontSize}
            className="p-1.5 rounded border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition text-xs font-mono font-bold"
            title="Toggle Text Size"
          >
            A±
          </button>
        </div>
      </header>

      {/* ============================================================== */}
      {/* 2. MAIN WORKSPACE LAYOUT (Left Sidebar + Center 3D Viewport)    */}
      {/* ============================================================== */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden relative">
        {/* ------------------------------------------------------------ */}
        {/* LEFT SIDEBAR: 3D Explorer & Numbered Components List         */}
        {/* ------------------------------------------------------------ */}
        <aside className="w-full md:w-[320px] lg:w-[340px] bg-white border-r border-slate-200 flex flex-col z-10 shrink-0 shadow-sm overflow-hidden">
          {/* Sidebar Top Title */}
          <div className="p-4 border-b border-slate-100">
            <h2 className="font-bold text-base text-slate-900 tracking-tight">
              3D Explorer
            </h2>
            <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">
              Tap a part in 3D or pick it here. Numbers match the callouts.
            </p>
          </div>

          {/* Numbered Components List */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {componentsData.map((part) => {
              const isSelected = selectedComponentId === part.id;
              const isIllustrative = part.id === '05_Filter_Drier' || part.id === '13_Thermostat_Electrical';
              
              return (
                <button
                  key={part.id}
                  onClick={() => setSelectedComponentId(part.id)}
                  className={`w-full flex items-start gap-2.5 px-3 py-2 rounded-lg text-left transition group ${
                    isSelected
                      ? 'bg-slate-100 text-[#0f172a] shadow-inner'
                      : 'hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  {/* Number Circle Badge */}
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-xs font-bold font-mono transition border ${
                    isSelected
                      ? 'bg-[#0f172a] text-white border-[#0f172a]'
                      : 'bg-white text-slate-800 border-slate-300 group-hover:border-slate-400'
                  }`}>
                    {part.number}
                  </div>

                  {/* Component Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className={`text-xs tracking-tight truncate ${
                        isSelected ? 'font-bold text-slate-900' : 'font-semibold text-slate-700'
                      }`}>
                        {part.name}
                      </span>
                    </div>
                    {isIllustrative && (
                      <span className="text-[10px] text-[#ea580c] italic font-sans block">
                        illustrative
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>

          {/* REFRIGERANT STATE (CONCEPTUAL) LEGEND */}
          <div className="p-3.5 border-t border-slate-200 bg-slate-50/70">
            <h3 className="text-[10px] font-mono font-bold tracking-wider text-[#ea580c] uppercase mb-2">
              REFRIGERANT STATE (CONCEPTUAL)
            </h3>
            <div className="space-y-1.5 text-[11px] text-slate-700 font-sans">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#dc2626] shrink-0" />
                <span>High-pressure hot vapour</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#ea580c] shrink-0" />
                <span>Condensing (vapour → liquid)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#f97316] shrink-0" />
                <span>High-pressure liquid</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#38bdf8] shrink-0" />
                <span>Low-pressure liquid–vapour mix</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#0284c7] shrink-0" />
                <span>Evaporating (liquid → vapour)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#1e40af] shrink-0" />
                <span>Low-pressure vapour</span>
              </div>
            </div>
            <p className="text-[9.5px] text-slate-400 mt-2 leading-tight">
              Flow arrows are a conceptual animation, not a CFD or thermodynamic simulation.
            </p>
          </div>
        </aside>

        {/* ------------------------------------------------------------ */}
        {/* CENTER / RIGHT: 3D VIEWPORT WITH INTERACTIVE OVERLAYS        */}
        {/* ------------------------------------------------------------ */}
        <main className="flex-1 flex flex-col relative h-[50vh] md:h-full bg-[#f8fafc] overflow-hidden">
          {/* Top Floating Instruction Banner */}
          <div className="absolute top-3 left-0 right-0 z-20 flex justify-center pointer-events-none px-4">
            <div className="bg-[#0f172a]/85 backdrop-blur-md text-white text-[11px] font-sans px-4 py-1.5 rounded-full shadow-lg pointer-events-auto flex items-center gap-1.5 border border-slate-700/50">
              {isCameraActive ? (
                <span>camera overlay · drag to turn · scroll / pinch to resize · tap a part · not surface-tracked — use AR for that</span>
              ) : (
                <>
                  <span>Drag to rotate · scroll / pinch to zoom · right-drag or two fingers to pan · <strong>tap a part</strong> to learn about it.</span>
                  <button 
                    onClick={() => setIsAROpen(true)}
                    className="text-[#00e5ff] font-semibold underline hover:text-[#38bdf8] ml-1"
                  >
                    Try it in AR →
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Three.js 3D Viewport Component */}
          <div className="flex-1 w-full h-full relative">
            <ThreeRefrigeratorViewer
              selectedComponentId={selectedComponentId}
              onSelectComponent={setSelectedComponentId}
              isDoorOpen={isDoorOpen}
              onToggleDoor={setIsDoorOpen}
              showLabels={showLabels}
              showFlow={showFlow}
              isCameraActive={isCameraActive}
              explodeFactor={explodeFactor}
              filterCategory={filterCategory}
            />
          </div>

          {/* ---------------------------------------------------------- */}
          {/* BOTTOM FLOATING TOOLBAR (Exact Match to VCR Reference)     */}
          {/* ---------------------------------------------------------- */}
          <div className="absolute bottom-3 left-0 right-0 z-20 flex justify-center pointer-events-none px-2">
            <div className="bg-white/95 backdrop-blur-md border border-slate-300 px-3 py-2 rounded-2xl shadow-xl flex flex-wrap items-center gap-2 pointer-events-auto text-xs">
              {/* Reset View */}
              <button
                onClick={() => {
                  setExplodeFactor(0);
                  setIsDoorOpen(false);
                  window.dispatchEvent(new CustomEvent('reset-camera'));
                }}
                className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold transition"
                title="Reset Camera"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reset</span>
              </button>

              {/* Zoom Buttons */}
              <div className="flex items-center border border-slate-200 rounded-lg overflow-hidden">
                <button
                  onClick={() => window.dispatchEvent(new CustomEvent('zoom-camera', { detail: -0.2 }))}
                  className="px-2 py-1.5 hover:bg-slate-100 text-slate-700 font-bold transition border-r border-slate-200"
                  title="Zoom In"
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => window.dispatchEvent(new CustomEvent('zoom-camera', { detail: 0.2 }))}
                  className="px-2 py-1.5 hover:bg-slate-100 text-slate-700 font-bold transition"
                  title="Zoom Out"
                >
                  <Minus className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Toggle Doors */}
              <button
                onClick={() => setIsDoorOpen(!isDoorOpen)}
                className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg font-semibold transition ${
                  isDoorOpen
                    ? 'bg-[#ea580c] text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
                title="Open/Close Refrigerator Doors"
              >
                {isDoorOpen ? <DoorOpen className="w-3.5 h-3.5" /> : <DoorClosed className="w-3.5 h-3.5" />}
                <span>Doors</span>
              </button>

              {/* Labels Toggle */}
              <button
                onClick={() => setShowLabels(!showLabels)}
                className={`px-3 py-1.5 rounded-lg font-semibold transition ${
                  showLabels
                    ? 'bg-[#0f172a] text-white shadow-sm'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                Labels
              </button>

              {/* Flow Toggle */}
              <button
                onClick={() => setShowFlow(!showFlow)}
                className={`px-3 py-1.5 rounded-lg font-semibold transition ${
                  showFlow
                    ? 'bg-[#0f172a] text-white shadow-sm'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                Flow
              </button>

              {/* Camera Background Toggle */}
              <button
                onClick={() => setIsCameraActive(!isCameraActive)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-semibold transition ${
                  isCameraActive
                    ? 'bg-[#dc2626] text-white'
                    : 'border border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
                title="Toggle Web Browser Camera Background Overlay"
              >
                {isCameraActive ? (
                  <>
                    <VideoOff className="w-3.5 h-3.5" />
                    <span>Stop camera</span>
                  </>
                ) : (
                  <>
                    <span className="w-2 h-2 rounded-full bg-[#dc2626] animate-pulse" />
                    <Camera className="w-3.5 h-3.5 text-[#dc2626]" />
                    <span>Camera</span>
                  </>
                )}
              </button>

              {/* Filter Dropdown */}
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold focus:outline-none text-xs"
              >
                <option value="all">Show all</option>
                <option value="refrigeration">Refrigeration Loop</option>
                <option value="cabinet">Cabinet & Doors</option>
                <option value="electrical">Electrical & Fan</option>
              </select>

              {/* Explode Slider */}
              <div className="flex items-center gap-1.5 px-2">
                <span className="text-xs text-slate-600 font-semibold">Explode</span>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={explodeFactor}
                  onChange={(e) => setExplodeFactor(parseFloat(e.target.value))}
                  className="w-20 sm:w-28 accent-[#ea580c] cursor-pointer"
                />
              </div>

              {/* Step Navigation & Play Cycle */}
              <div className="flex items-center gap-1 border-l border-slate-200 pl-2">
                <button
                  onClick={handlePrevPart}
                  className="p-1.5 rounded hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition"
                  title="Previous Part"
                >
                  <SkipBack className="w-3.5 h-3.5" />
                </button>

                <button
                  onClick={() => setIsPlayingCycle(!isPlayingCycle)}
                  className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg font-semibold transition ${
                    isPlayingCycle
                      ? 'bg-[#ea580c] text-white'
                      : 'bg-slate-100 text-slate-800 hover:bg-slate-200'
                  }`}
                  title="Play 4-Stage Refrigeration Cycle"
                >
                  {isPlayingCycle ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                  <span>{isPlayingCycle ? 'Pause' : 'Play cycle'}</span>
                </button>

                <button
                  onClick={handleNextPart}
                  className="p-1.5 rounded hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition"
                  title="Next Part"
                >
                  <SkipForward className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* ============================================================== */}
      {/* 3. MODALS (Components, Cycle, Project, References, AR)         */}
      {/* ============================================================== */}
      <ARViewModal isOpen={isAROpen} onClose={() => setIsAROpen(false)} />
      <ComponentLibraryModal 
        isOpen={isLibraryOpen} 
        onClose={() => setIsLibraryOpen(false)} 
        onSelectComponent={(id) => {
          setSelectedComponentId(id);
          setIsLibraryOpen(false);
          setActiveTab('3d');
        }}
      />
      <CycleExplanationModal isOpen={isCycleOpen} onClose={() => setIsCycleOpen(false)} />
      <AboutModal isOpen={isAboutOpen} onClose={() => setIsAboutOpen(false)} />

      {/* References Modal */}
      {isReferencesOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="w-full max-w-2xl bg-white border border-slate-300 rounded-xl overflow-hidden shadow-2xl p-6">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-[#0284c7]" />
                <h3 className="font-bold text-base text-slate-900">Engineering References & Citations</h3>
              </div>
              <button 
                onClick={() => setIsReferencesOpen(false)}
                className="p-1 rounded text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-3 text-xs text-slate-700 leading-relaxed">
              <p>• <strong>C. P. Arora</strong>, <em>Refrigeration and Air Conditioning</em>, 3rd ed., McGraw-Hill, 2008.</p>
              <p>• <strong>W. F. Stoecker & J. W. Jones</strong>, <em>Refrigeration and Air Conditioning</em>, McGraw-Hill.</p>
              <p>• <strong>Y. A. Çengel & M. A. Boles</strong>, <em>Thermodynamics: An Engineering Approach</em>, McGraw-Hill.</p>
              <p>• <strong>ASHRAE Handbook</strong> — <em>Refrigeration (Systems and Equipment)</em>, ASHRAE, 2022.</p>
              <p>• <strong>Software stack</strong>: three.js, Google &lt;model-viewer&gt;, React 19, Vite 6, TypeScript, ReportLab, Blender 5.2 Python API.</p>
              <p>• <strong>Validation</strong>: Khronos Group glTF-Validator 2.0 (0 errors, 0 warnings).</p>
            </div>
            <div className="mt-6 pt-3 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setIsReferencesOpen(false)}
                className="px-4 py-2 rounded bg-[#0f172a] text-white font-semibold text-xs hover:bg-slate-800"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
