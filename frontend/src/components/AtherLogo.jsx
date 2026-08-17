import React from "react";

export function AtherLogo({ className = "size-8" }) {
  return (
    <div className={`relative flex items-center justify-center shrink-0 ${className}`}>
      <svg
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full drop-shadow-[0_0_12px_rgba(199,244,210,0.35)]"
      >
        <defs>
          <linearGradient id="ather-grad-primary" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#c7f4d2" />
            <stop offset="50%" stopColor="#34d399" />
            <stop offset="100%" stopColor="#059669" />
          </linearGradient>
          <linearGradient id="ather-grad-glow" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#c7f4d2" stopOpacity="0.2" />
          </linearGradient>
          <linearGradient id="ather-bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#1e222d" />
            <stop offset="100%" stopColor="#0d0e12" />
          </linearGradient>
        </defs>

        {/* Outer squircle frame */}
        <rect
          x="1"
          y="1"
          width="38"
          height="38"
          rx="11"
          fill="url(#ather-bg-gradient)"
          stroke="url(#ather-grad-primary)"
          strokeWidth="1.5"
          strokeOpacity="0.4"
        />

        {/* Geometric 'A' facet structure */}
        {/* Left pillar */}
        <path
          d="M12 30L20 9L23.5 17.5H16.5L12 30Z"
          fill="url(#ather-grad-primary)"
        />
        {/* Right pillar */}
        <path
          d="M28 30L20 9L16.5 17.5H23.5L28 30Z"
          fill="url(#ather-grad-primary)"
          fillOpacity="0.8"
        />
        {/* Crossbeam node */}
        <path
          d="M15 21H25L23.5 24.5H16.5L15 21Z"
          fill="url(#ather-grad-glow)"
        />

        {/* Top apex node */}
        <circle cx="20" cy="9" r="2" fill="#ffffff" />
        {/* Left base node */}
        <circle cx="12" cy="30" r="1.75" fill="#c7f4d2" />
        {/* Right base node */}
        <circle cx="28" cy="30" r="1.75" fill="#34d399" />
      </svg>
    </div>
  );
}

export default AtherLogo;
