import React from 'react';
import { X, GraduationCap, Users, FileText, CheckCircle, Code, Cpu, Award } from 'lucide-react';

interface AboutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-black/80 backdrop-blur-md">
      <div className="relative w-full max-w-3xl h-[86vh] bg-[#070d1e] border border-[#1e2e5c] rounded-xl flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#1e2e5c] bg-[#0c1633]">
          <div className="flex items-center gap-3">
            <GraduationCap className="w-5 h-5 text-[#00e5ff]" />
            <div>
              <h3 className="font-mono text-base font-bold text-white tracking-wide">
                PROJECT IDENTITY & ENGINEERING CREDITS
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                COEP Technological University, Pune · Robotics and AI
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

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Student details */}
          <div className="tech-panel p-5 border border-[#00e5ff]/40">
            <div className="flex items-center gap-2 mb-3">
              <Users className="w-4 h-4 text-[#00e5ff]" />
              <h4 className="font-mono text-xs font-bold text-[#00e5ff] uppercase tracking-wider">
                Prepared by (Robotics and AI)
              </h4>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-[#0b142d] p-3.5 rounded border border-[#1e2e5c]">
                <span className="text-[11px] font-mono text-slate-400 block">Student 1</span>
                <span className="font-mono text-base font-bold text-white block mt-0.5">
                  Sahil Panchavishe
                </span>
                <span className="inline-block mt-2 badge-tech badge-cyan">
                  MIS: 612302040
                </span>
              </div>

              <div className="bg-[#0b142d] p-3.5 rounded border border-[#1e2e5c]">
                <span className="text-[11px] font-mono text-slate-400 block">Student 2</span>
                <span className="font-mono text-base font-bold text-white block mt-0.5">
                  Megh Shidam
                </span>
                <span className="inline-block mt-2 badge-tech badge-cyan">
                  MIS: 612302058
                </span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-[#1e2e5c] text-xs font-mono text-slate-300">
              <span className="text-slate-400">Department:</span> Department of Robotics and AI<br />
              <span className="text-slate-400">Institution:</span> COEP Technological University, Pune (Est. 1854)
            </div>
          </div>

          {/* Implementation Architecture */}
          <div className="tech-panel p-5">
            <div className="flex items-center gap-2 mb-3">
              <Code className="w-4 h-4 text-emerald-400" />
              <h4 className="font-mono text-xs font-bold text-emerald-400 uppercase tracking-wider">
                Implementation Architecture
              </h4>
            </div>
            <ul className="space-y-2.5 text-xs text-slate-300 font-mono">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>
                  <strong className="text-white">Procedural 3D Geometry:</strong> Generated original 3D geometry using Blender Python API. Structured hierarchy of 165 nodes, 151 meshes, dual door hinge pivots, and exported to validated glTF 2.0 (GLB).
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>
                  <strong className="text-white">Three.js Web 3D Explorer:</strong> Custom WebGL renderer with PBR materials, orbit camera, explode slider, isolate ghosting mode, and live door hinge rotation animation.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>
                  <strong className="text-white">Cross-Platform WebAR & Camera Overlay:</strong> Google &lt;model-viewer&gt; for zero-install ARCore (Android) and AR Quick Look (iOS), with fallback live camera stream overlay for desktops and laptops.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>
                  <strong className="text-white">Unity 6 Project:</strong> Complete Unity project with URP, C# interaction controllers, AR Foundation support, and JSON data integration.
                </span>
              </li>
            </ul>
          </div>

          {/* Educational Applications & Limitations */}
          <div className="tech-panel p-5">
            <h4 className="font-mono text-xs font-bold text-[#fb923c] uppercase tracking-wider mb-2">
              Applications & Limitations
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-[#00e5ff] font-semibold block mb-1">Use it for:</span>
                <ul className="list-disc ml-4 space-y-1 text-slate-300">
                  <li>Engineering laboratory pre-briefing</li>
                  <li>Interactive 3D self-study on mobile phones</li>
                  <li>Visualizing concealed cooling coils & capillary tubes</li>
                  <li>Explaining refrigeration cycles to students</li>
                </ul>
              </div>
              <div>
                <span className="text-amber-400 font-semibold block mb-1">Keep in mind:</span>
                <ul className="list-disc ml-4 space-y-1 text-slate-300">
                  <li>Original educational 3D model, not manufacturer CAD</li>
                  <li>Refrigerant flow is conceptual animation, not CFD solver</li>
                  <li>No proprietary or invented temperature readings</li>
                  <li>AR surface detection requires compatible mobile device</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Download Technical Poster */}
          <div className="tech-panel p-4 flex items-center justify-between bg-gradient-to-r from-[#0c1633] to-[#12214d]">
            <div className="flex items-center gap-3">
              <FileText className="w-6 h-6 text-[#00e5ff]" />
              <div>
                <span className="font-mono text-xs font-bold text-white block">
                  Four-Page A3 Landscape Technical Poster (PDF)
                </span>
                <span className="text-[11px] font-mono text-slate-400">
                  Print-ready 420 × 297 mm · Hardware · Cycle · Architecture · QR
                </span>
              </div>
            </div>
            <a
              href="./Domestic-Refrigerator-AR-Explorer-Technical-Poster.pdf"
              download
              className="btn-primary text-xs"
            >
              DOWNLOAD PDF
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
