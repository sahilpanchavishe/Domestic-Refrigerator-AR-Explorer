import React, { useState } from 'react';
import { 
  Box, 
  Layers, 
  Smartphone, 
  RotateCw, 
  Sliders, 
  Eye, 
  BookOpen, 
  Activity, 
  Info, 
  ChevronRight, 
  ChevronLeft, 
  X, 
  Download, 
  Compass,
  FileText
} from 'lucide-react';
import { ThreeRefrigeratorViewer } from './components/ThreeRefrigeratorViewer';
import { ARViewModal } from './components/ARViewModal';
import { ComponentLibraryModal } from './components/ComponentLibraryModal';
import { CycleExplanationModal } from './components/CycleExplanationModal';
import { AboutModal } from './components/AboutModal';
import componentsData from './data/components.json';

export const App: React.FC = () => {
  const [selectedComponentId, setSelectedComponentId] = useState<string | null>('01_Compressor');
  const [isDoorOpen, setIsDoorOpen] = useState<boolean>(false);
  const [explodeFactor, setExplodeFactor] = useState<number>(0);
  const [isIsolateMode, setIsIsolateMode] = useState<boolean>(false);
  const [isCycleFlowActive, setIsCycleFlowActive] = useState<boolean>(false);
  const [cameraPreset, setCameraPreset] = useState<string>('reset');

  // Modals
  const [isAROpen, setIsAROpen] = useState<boolean>(false);
  const [isLibraryOpen, setIsLibraryOpen] = useState<boolean>(false);
  const [isCycleOpen, setIsCycleOpen] = useState<boolean>(false);
  const [isAboutOpen, setIsAboutOpen] = useState<boolean>(false);

  const selectedComponent = componentsData.find((c) => c.id === selectedComponentId);
  const currentIndex = componentsData.findIndex((c) => c.id === selectedComponentId);

  const handleNextComponent = () => {
    const nextIdx = (currentIndex + 1) % componentsData.length;
    setSelectedComponentId(componentsData[nextIdx].id);
  };

  const handlePrevComponent = () => {
    const prevIdx = (currentIndex - 1 + componentsData.length) % componentsData.length;
    setSelectedComponentId(componentsData[prevIdx].id);
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-[#070d1e] text-slate-100 overflow-hidden font-sans">
      {/* Top Header Engineering Title Block */}
      <header className="flex flex-wrap items-center justify-between px-4 py-2.5 bg-[#091129] border-b border-[#1e2e5c] z-20">
        <div className="flex items-center gap-3">
          <div className="bg-[#00e5ff]/10 border border-[#00e5ff]/40 p-1.5 rounded text-[#00e5ff]">
            <Box className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="badge-tech badge-cyan text-[10px]">DRG. NO. REF-001</span>
              <span className="text-[10px] font-mono text-slate-400">SHEET 1 / 4 · SECTION A</span>
            </div>
            <h1 className="font-mono text-sm md:text-base font-bold text-white tracking-wide">
              DOMESTIC REFRIGERATOR AR EXPLORER
            </h1>
            <p className="text-[10px] font-mono text-slate-400 hidden sm:block">
              Department of Robotics and AI · COEP Technological University, Pune
            </p>
          </div>
        </div>

        {/* Action Header Buttons */}
        <div className="flex items-center gap-2 mt-2 sm:mt-0">
          <button
            onClick={() => setIsAROpen(true)}
            className="btn-primary text-xs"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span>AR VIEW</span>
          </button>

          <button
            onClick={() => setIsCycleOpen(true)}
            className="btn-secondary text-xs"
          >
            <Activity className="w-3.5 h-3.5 text-[#00e5ff]" />
            <span className="hidden md:inline">VCR CYCLE</span>
          </button>

          <button
            onClick={() => setIsLibraryOpen(true)}
            className="btn-secondary text-xs"
          >
            <BookOpen className="w-3.5 h-3.5 text-[#fb923c]" />
            <span className="hidden md:inline">PARTS SPEC</span>
          </button>

          <button
            onClick={() => setIsAboutOpen(true)}
            className="btn-secondary text-xs"
          >
            <Info className="w-3.5 h-3.5 text-slate-300" />
            <span className="hidden lg:inline">CREDITS</span>
          </button>

          <a
            href="./Domestic-Refrigerator-AR-Explorer-Technical-Poster.pdf"
            download
            className="btn-accent-copper text-xs flex items-center gap-1.5"
            title="Download Four-Page A3 Poster PDF"
          >
            <FileText className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">POSTER (PDF)</span>
          </a>
        </div>
      </header>

      {/* Main Workspace Layout */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden relative">
        {/* Left: 3D Viewport Area */}
        <div className="flex-1 flex flex-col relative h-[60vh] lg:h-full bg-grid-pattern overflow-hidden">
          {/* Top Controls Toolbar */}
          <div className="absolute top-3 left-3 right-3 z-10 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
            {/* Camera View Presets */}
            <div className="flex items-center gap-1.5 bg-[#091129]/90 backdrop-blur-md p-1 rounded-md border border-[#1e2e5c] pointer-events-auto shadow-lg">
              <span className="text-[10px] font-mono text-slate-400 px-2 uppercase font-semibold">
                Camera:
              </span>
              {[
                { id: 'reset', label: 'Iso' },
                { id: 'front', label: 'Front' },
                { id: 'rear', label: 'Rear' },
                { id: 'interior', label: 'Interior' },
                { id: 'compressor', label: 'Compressor' }
              ].map((p) => (
                <button
                  key={p.id}
                  onClick={() => setCameraPreset(p.id)}
                  className={`px-2.5 py-1 text-[11px] font-mono rounded transition ${
                    cameraPreset === p.id
                      ? 'bg-[#00e5ff] text-slate-950 font-bold'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>

            {/* Quick Actions */}
            <div className="flex items-center gap-2 pointer-events-auto">
              <button
                onClick={() => setIsDoorOpen(!isDoorOpen)}
                className={`px-3 py-1.5 rounded text-xs font-mono font-semibold transition flex items-center gap-1.5 border shadow-lg ${
                  isDoorOpen
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/50'
                    : 'bg-[#0c1633]/90 text-[#00e5ff] border-[#00e5ff]/40 hover:bg-[#00e5ff]/20'
                }`}
              >
                <RotateCw className="w-3.5 h-3.5" />
                {isDoorOpen ? 'CLOSE DOORS' : 'OPEN DOORS'}
              </button>

              <button
                onClick={() => setIsCycleFlowActive(!isCycleFlowActive)}
                className={`px-3 py-1.5 rounded text-xs font-mono font-semibold transition border shadow-lg ${
                  isCycleFlowActive
                    ? 'bg-[#00e5ff] text-slate-950 border-[#00e5ff]'
                    : 'bg-[#0c1633]/90 text-slate-300 border-[#1e2e5c] hover:border-[#00e5ff]/50'
                }`}
              >
                CYCLE FLOW
              </button>
            </div>
          </div>

          {/* Three.js 3D Viewer Canvas */}
          <div className="flex-1 w-full h-full">
            <ThreeRefrigeratorViewer
              selectedComponentId={selectedComponentId}
              onSelectComponent={setSelectedComponentId}
              isDoorOpen={isDoorOpen}
              onToggleDoor={setIsDoorOpen}
              explodeFactor={explodeFactor}
              isIsolateMode={isIsolateMode}
              isCycleFlowActive={isCycleFlowActive}
              cameraPreset={cameraPreset}
            />
          </div>

          {/* Bottom Floating Toolbar: Explode Slider & Ghosting */}
          <div className="absolute bottom-3 right-3 z-10 flex items-center gap-3 bg-[#091129]/90 backdrop-blur-md px-3.5 py-2 rounded-lg border border-[#1e2e5c] shadow-xl">
            <div className="flex items-center gap-2">
              <Sliders className="w-3.5 h-3.5 text-[#00e5ff]" />
              <span className="text-xs font-mono text-slate-300">Explode:</span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={explodeFactor}
                onChange={(e) => setExplodeFactor(parseFloat(e.target.value))}
                className="w-24 md:w-32 accent-[#00e5ff] cursor-pointer"
              />
              <span className="text-[11px] font-mono text-slate-400 w-8">
                {Math.round(explodeFactor * 100)}%
              </span>
            </div>

            <div className="h-4 w-px bg-slate-700" />

            <label className="flex items-center gap-1.5 text-xs font-mono text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={isIsolateMode}
                onChange={(e) => setIsIsolateMode(e.target.checked)}
                className="accent-[#00e5ff]"
              />
              Isolate Part
            </label>
          </div>
        </div>

        {/* Right Sidebar: Component Information & Spec Panel */}
        <aside className="w-full lg:w-[420px] bg-[#091129] border-t lg:border-t-0 lg:border-l border-[#1e2e5c] flex flex-col overflow-hidden z-10 shadow-2xl">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between px-5 py-3 border-b border-[#1e2e5c] bg-[#0c1633]">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#00e5ff]" />
              <h2 className="font-mono text-xs font-bold text-white tracking-wider uppercase">
                Component Inspector
              </h2>
            </div>
            {selectedComponent && (
              <button
                onClick={() => setSelectedComponentId(null)}
                className="text-slate-400 hover:text-white text-xs font-mono flex items-center gap-1"
              >
                <X className="w-3.5 h-3.5" /> Deselect
              </button>
            )}
          </div>

          {/* Component Details Card */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {selectedComponent ? (
              <div className="space-y-4">
                {/* Part ID Badge & Navigation */}
                <div className="flex items-center justify-between">
                  <span className="badge-tech badge-cyan">
                    PART #{selectedComponent.number.toString().padStart(2, '0')}
                  </span>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={handlePrevComponent}
                      className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
                      title="Previous Component"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    <span className="text-[11px] font-mono text-slate-400 px-1">
                      {currentIndex + 1} / {componentsData.length}
                    </span>
                    <button
                      onClick={handleNextComponent}
                      className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
                      title="Next Component"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Name & Short Description */}
                <div>
                  <h3 className="font-mono text-lg font-bold text-white">
                    {selectedComponent.name}
                  </h3>
                  <p className="text-xs text-slate-300 font-sans mt-1 leading-relaxed">
                    {selectedComponent.shortDescription}
                  </p>
                </div>

                {/* Technical Attributes */}
                <div className="space-y-2.5 text-xs">
                  <div className="tech-panel p-3">
                    <span className="text-[11px] font-mono text-[#00e5ff] font-semibold block mb-0.5">
                      PRIMARY FUNCTION
                    </span>
                    <p className="text-slate-200 font-sans leading-relaxed">
                      {selectedComponent.function}
                    </p>
                  </div>

                  <div className="tech-panel p-3">
                    <span className="text-[11px] font-mono text-[#fb923c] font-semibold block mb-0.5">
                      WORKING PRINCIPLE
                    </span>
                    <p className="text-slate-200 font-sans leading-relaxed">
                      {selectedComponent.workingPrinciple}
                    </p>
                  </div>

                  <div className="tech-panel p-3">
                    <span className="text-[11px] font-mono text-emerald-400 font-semibold block mb-0.5">
                      CYCLE STAGE & ROLE
                    </span>
                    <p className="text-slate-200 font-sans leading-relaxed">
                      {selectedComponent.cycleRole}
                    </p>
                  </div>

                  <div className="tech-panel p-3">
                    <span className="text-[11px] font-mono text-slate-400 font-semibold block mb-0.5">
                      LOCATION IN APPLIANCE
                    </span>
                    <p className="text-slate-200 font-sans leading-relaxed">
                      {selectedComponent.location}
                    </p>
                  </div>

                  <div className="tech-panel p-3 bg-[#0c1633]/60 border-l-2 border-l-[#00e5ff]">
                    <span className="text-[11px] font-mono text-[#00e5ff] font-semibold block mb-0.5">
                      ENGINEERING RELEVANCE
                    </span>
                    <p className="text-slate-300 font-sans text-[11px] leading-relaxed">
                      {selectedComponent.practicalRelevance}
                    </p>
                  </div>

                  <div className="tech-panel p-3 bg-amber-500/5 border-l-2 border-l-amber-500">
                    <span className="text-[11px] font-mono text-amber-400 font-semibold block mb-0.5">
                      STUDENT NOTE
                    </span>
                    <p className="text-slate-300 font-sans text-[11px] leading-relaxed">
                      {selectedComponent.studentNote}
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center text-center h-full py-8 text-slate-400">
                <Box className="w-10 h-10 text-slate-500 mb-3 animate-pulse" />
                <h4 className="font-mono text-sm font-semibold text-slate-300 mb-1">
                  NO PART SELECTED
                </h4>
                <p className="text-xs max-w-xs font-sans text-slate-400 mb-5">
                  Click on any component in the 3D refrigerator to highlight its geometry and inspect its thermodynamic role.
                </p>
                <div className="w-full space-y-1.5 text-left">
                  <span className="text-[11px] font-mono text-slate-500 block uppercase">
                    Quick Select:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {componentsData.map((c) => (
                      <button
                        key={c.id}
                        onClick={() => setSelectedComponentId(c.id)}
                        className="px-2 py-1 rounded bg-[#0c1633] border border-[#1e2e5c] text-[11px] font-mono text-slate-300 hover:text-[#00e5ff] hover:border-[#00e5ff] transition"
                      >
                        #{c.number.toString().padStart(2, '0')} {c.name.split(' ')[0]}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer Metadata */}
          <div className="p-3 bg-[#0c1633] border-t border-[#1e2e5c] text-[11px] font-mono text-slate-400 flex items-center justify-between">
            <span>COEP Tech University</span>
            <span>Sahil P. & Megh S.</span>
          </div>
        </aside>
      </div>

      {/* Modals */}
      <ARViewModal isOpen={isAROpen} onClose={() => setIsAROpen(false)} />
      <ComponentLibraryModal
        isOpen={isLibraryOpen}
        onClose={() => setIsLibraryOpen(false)}
        onSelectComponent={(id) => setSelectedComponentId(id)}
      />
      <CycleExplanationModal isOpen={isCycleOpen} onClose={() => setIsCycleOpen(false)} />
      <AboutModal isOpen={isAboutOpen} onClose={() => setIsAboutOpen(false)} />
    </div>
  );
};
