import React from 'react';
import { X, Flame, Snowflake, Activity, ArrowRight, Gauge, Cpu } from 'lucide-react';

interface CycleModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CycleExplanationModal: React.FC<CycleModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-black/80 backdrop-blur-md">
      <div className="relative w-full max-w-4xl h-[88vh] bg-[#070d1e] border border-[#1e2e5c] rounded-xl flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#1e2e5c] bg-[#0c1633]">
          <div className="flex items-center gap-3">
            <Activity className="w-5 h-5 text-[#00e5ff]" />
            <div>
              <h3 className="font-mono text-base font-bold text-white tracking-wide">
                HOW A DOMESTIC REFRIGERATOR WORKS · THE VCR CYCLE
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                One Closed Loop · Two Operating Pressures · Continuous Heat Pumping
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
          {/* Overview Banner */}
          <div className="tech-panel p-5 border-l-4 border-l-[#00e5ff]">
            <h4 className="font-mono text-sm font-bold text-white mb-1.5">
              Thermodynamic Working Principle
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed font-sans">
              A domestic refrigerator does not "create cold". Instead, it acts as a thermodynamic heat pump. It absorbs heat from a low-temperature space (the interior food cabinet at +3°C and freezer at -18°C) by evaporating liquid refrigerant at low pressure, and rejects that heat into the higher-temperature kitchen room (+25°C to +35°C) by condensing the refrigerant vapour at high pressure.
            </p>
          </div>

          {/* Schematic Diagram Block */}
          <div className="tech-panel p-5">
            <h4 className="font-mono text-xs font-bold text-[#00e5ff] tracking-wider uppercase mb-4">
              Closed Loop Refrigeration Circuit Schematic
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              {/* State 1 -> 2 */}
              <div className="bg-[#0b142d] p-4 rounded-lg border border-red-500/30 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="badge-tech bg-red-500/20 text-red-400 border border-red-500/40">
                      STAGE 1 → 2
                    </span>
                    <Cpu className="w-4 h-4 text-red-400" />
                  </div>
                  <h5 className="font-mono text-sm font-bold text-white mb-1">
                    Compression
                  </h5>
                  <p className="text-[11px] text-slate-300">
                    Low-pressure vapour enters the compressor and is squeezed into high-pressure, superheated hot gas.
                  </p>
                </div>
                <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-red-400">
                  + Work Input (W_in)
                </div>
              </div>

              {/* State 2 -> 3 */}
              <div className="bg-[#0b142d] p-4 rounded-lg border border-amber-500/30 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="badge-tech bg-amber-500/20 text-amber-400 border border-amber-500/40">
                      STAGE 2 → 3
                    </span>
                    <Flame className="w-4 h-4 text-amber-400" />
                  </div>
                  <h5 className="font-mono text-sm font-bold text-white mb-1">
                    Condensation
                  </h5>
                  <p className="text-[11px] text-slate-300">
                    Hot gas gives up heat to room air through the rear condenser coil, condensing into high-pressure liquid.
                  </p>
                </div>
                <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-amber-400">
                  - Heat Out (Q_out)
                </div>
              </div>

              {/* State 3 -> 4 */}
              <div className="bg-[#0b142d] p-4 rounded-lg border border-cyan-500/30 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="badge-tech bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                      STAGE 3 → 4
                    </span>
                    <Gauge className="w-4 h-4 text-cyan-400" />
                  </div>
                  <h5 className="font-mono text-sm font-bold text-white mb-1">
                    Throttling (Expansion)
                  </h5>
                  <p className="text-[11px] text-slate-300">
                    High-pressure liquid forces through the narrow capillary tube; pressure and saturation temperature plunge.
                  </p>
                </div>
                <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-cyan-400">
                  Constant Enthalpy (h3 = h4)
                </div>
              </div>

              {/* State 4 -> 1 */}
              <div className="bg-[#0b142d] p-4 rounded-lg border border-blue-500/30 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="badge-tech bg-blue-500/20 text-blue-400 border border-blue-500/40">
                      STAGE 4 → 1
                    </span>
                    <Snowflake className="w-4 h-4 text-blue-400" />
                  </div>
                  <h5 className="font-mono text-sm font-bold text-white mb-1">
                    Evaporation
                  </h5>
                  <p className="text-[11px] text-slate-300">
                    Sub-zero liquid-vapour boils inside evaporator fins by absorbing heat from the food compartment.
                  </p>
                </div>
                <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-blue-400">
                  + Heat In (Q_in = Cooling)
                </div>
              </div>
            </div>
          </div>

          {/* Energy Balance & COP */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="tech-panel p-5">
              <h5 className="font-mono text-xs font-bold text-[#00e5ff] uppercase mb-2">
                1st Law Energy Balance (Steady-State)
              </h5>
              <div className="bg-[#091129] p-3 rounded font-mono text-sm text-center text-white border border-[#1e2e5c] mb-3">
                Q_out = Q_in + W_in
              </div>
              <p className="text-xs text-slate-300 font-sans leading-relaxed">
                The total thermal energy rejected at the condenser coil (Q_out) equals the heat absorbed from refrigerated food (Q_in) plus the electrical mechanical work consumed by the compressor motor (W_in).
              </p>
            </div>

            <div className="tech-panel p-5">
              <h5 className="font-mono text-xs font-bold text-[#fb923c] uppercase mb-2">
                Coefficient of Performance (COP)
              </h5>
              <div className="bg-[#091129] p-3 rounded font-mono text-sm text-center text-white border border-[#1e2e5c] mb-3">
                COP = Q_in / W_in = (h1 - h4) / (h2 - h1)
              </div>
              <p className="text-xs text-slate-300 font-sans leading-relaxed">
                For a typical domestic household refrigerator, COP ranges between 1.5 and 2.6. Every 1 Joule of electrical work moves up to 2.6 Joules of heat out of the food compartment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
