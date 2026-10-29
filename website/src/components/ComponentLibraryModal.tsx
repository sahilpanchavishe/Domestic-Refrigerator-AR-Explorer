import React, { useState } from 'react';
import { X, Search, BookOpen, Layers, ShieldCheck, Wrench, Sparkles } from 'lucide-react';
import componentsData from '../data/components.json';

interface ComponentLibraryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectComponent: (id: string) => void;
}

export const ComponentLibraryModal: React.FC<ComponentLibraryModalProps> = ({
  isOpen,
  onClose,
  onSelectComponent
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'cycle' | 'cabinet' | 'auxiliary'>('all');

  if (!isOpen) return null;

  const filtered = componentsData.filter((comp) => {
    const matchesSearch =
      comp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      comp.function.toLowerCase().includes(searchTerm.toLowerCase()) ||
      comp.workingPrinciple.toLowerCase().includes(searchTerm.toLowerCase());

    if (!matchesSearch) return false;

    if (activeTab === 'cycle') {
      return ['01_Compressor', '02_Condenser_Coil', '03_Capillary_Tube', '04_Evaporator_Unit', '05_Filter_Drier', '07_Refrigerant_Lines'].includes(comp.id);
    }
    if (activeTab === 'cabinet') {
      return ['08_Cabinet_Body', '09_Shelves_And_Drawers', '10_Fresh_Food_Door_Assembly', '11_Freezer_Door_Assembly'].includes(comp.id);
    }
    if (activeTab === 'auxiliary') {
      return ['06_Condenser_Fan', '12_Rear_Ventilation_Grille', '13_Thermostat_Electrical'].includes(comp.id);
    }
    return true;
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-black/80 backdrop-blur-md">
      <div className="relative w-full max-w-5xl h-[88vh] bg-[#070d1e] border border-[#1e2e5c] rounded-xl flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#1e2e5c] bg-[#0c1633]">
          <div className="flex items-center gap-3">
            <BookOpen className="w-5 h-5 text-[#00e5ff]" />
            <div>
              <h3 className="font-mono text-base font-bold text-white tracking-wide">
                REFRIGERATOR COMPONENT SPECIFICATION LIBRARY
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                13 Verified Assemblies · Thermodynamic Principles · Mechanical Design Notes
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

        {/* Filter bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 px-6 py-3 border-b border-[#1e2e5c] bg-[#091129]">
          <div className="relative flex-1 min-w-[240px] max-w-md">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search components, functions, or principles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-[#0d1838] border border-[#1e2e5c] rounded-md pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 font-mono focus:outline-none focus:border-[#00e5ff]"
            />
          </div>

          <div className="flex items-center gap-2">
            {(['all', 'cycle', 'cabinet', 'auxiliary'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 rounded text-xs font-mono capitalize transition ${
                  activeTab === tab
                    ? 'bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/50'
                    : 'text-slate-400 hover:text-white border border-transparent'
                }`}
              >
                {tab === 'all' ? 'All Components (13)' : tab === 'cycle' ? 'Core Cycle (6)' : tab === 'cabinet' ? 'Cabinet & Doors (4)' : 'Auxiliary (3)'}
              </button>
            ))}
          </div>
        </div>

        {/* Component list */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((comp) => (
            <div
              key={comp.id}
              className="tech-panel p-5 flex flex-col justify-between hover:border-[#00e5ff]/60 transition group"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="badge-tech badge-cyan">
                    PART #{comp.number.toString().padStart(2, '0')}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    ID: {comp.id}
                  </span>
                </div>

                <h4 className="font-mono text-base font-bold text-white mb-1 group-hover:text-[#00e5ff] transition">
                  {comp.name}
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed mb-4">
                  {comp.shortDescription}
                </p>

                <div className="space-y-2 text-xs font-mono">
                  <div className="bg-[#0c1633]/80 p-2.5 rounded border border-[#1e2e5c]">
                    <span className="text-[#00e5ff] font-semibold block mb-0.5">Primary Function:</span>
                    <span className="text-slate-300 font-sans">{comp.function}</span>
                  </div>

                  <div className="bg-[#0c1633]/80 p-2.5 rounded border border-[#1e2e5c]">
                    <span className="text-[#fb923c] font-semibold block mb-0.5">Thermodynamic Principle:</span>
                    <span className="text-slate-300 font-sans">{comp.workingPrinciple}</span>
                  </div>

                  <div className="bg-[#0c1633]/80 p-2.5 rounded border border-[#1e2e5c]">
                    <span className="text-emerald-400 font-semibold block mb-0.5">Cycle Role:</span>
                    <span className="text-slate-300 font-sans">{comp.cycleRole}</span>
                  </div>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-[#1e2e5c] flex items-center justify-between">
                <span className="text-[11px] font-mono text-slate-400">
                  Location: {comp.location.split(',')[0]}
                </span>
                <button
                  onClick={() => {
                    onSelectComponent(comp.id);
                    onClose();
                  }}
                  className="btn-secondary text-xs flex items-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#00e5ff]" />
                  Highlight in 3D
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
