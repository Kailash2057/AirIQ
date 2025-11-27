import React from 'react';

interface AiriQLogoProps {
  size?: number;
  className?: string;
}

export function AiriQLogo({ size = 100, className = "" }: AiriQLogoProps) {
  // Replace 'airiq-logo.png' with your actual logo filename
  // Place your logo image in the /public folder
  const logoSrc = '/airiq-logo.jpg';
  
  return (
    <img
      src={logoSrc}
      alt="AiriQ Logo"
      width={size}
      height={size}
      className={`rounded-full object-contain ${className}`}
      style={{ minWidth: size, minHeight: size }}
      onError={(e) => {
        // Fallback to placeholder if image not found
        const target = e.target as HTMLImageElement;
        target.src = `https://via.placeholder.com/${size}/1e40af/ffffff?text=AiriQ`;
      }}
    />
  );
}

