// Blinged-out version of the Music Video Generator frontend UI with animations and styling

import React, { useState } from "react";
import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Music, Film } from "lucide-react";

const videoStyles = [
  // (same as before, unchanged)
];

export default function MusicVideoGen() {
  const [selectedStyle, setSelectedStyle] = useState(null);
  const [hovered, setHovered] = useState(null);
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedVideoUrl, setGeneratedVideoUrl] = useState(null);

  const handleUpload = (e) => {
    const uploadedFile = e.target.files?.[0];
    if (!uploadedFile) return;

    if (uploadedFile.type !== "audio/mpeg") {
      alert("Please upload a valid MP3 file.");
      return;
    }
    if (uploadedFile.size > 20 * 1024 * 1024) {
      alert("File must be under 20MB.");
      return;
    }

    setFile(uploadedFile);
    setGeneratedVideoUrl(null); // Reset output if new file is uploaded
  };

  const handleGenerate = () => {
    if (!file || !selectedStyle) {
      alert("Upload an MP3 and choose a video style first.");
      return;
    }

    setIsLoading(true);
    setGeneratedVideoUrl(null);
    
    setTimeout(() => {
      setIsLoading(false);
      setGeneratedVideoUrl("/mock/generated-video.mp4"); // Mock result
    }, 3000);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-10 max-w-7xl mx-auto text-white bg-gradient-to-br from-black via-gray-900 to-gray-800 rounded-3xl shadow-2xl"
    >
      <h1 className="text-5xl font-extrabold mb-8 text-center flex justify-center items-center gap-4">
        <Music className="w-10 h-10 text-pink-500 animate-bounce" />
        MP3 to Music Video Generator
        <Film className="w-10 h-10 text-blue-400 animate-pulse" />
      </h1>

      <div className="mb-10 text-center">
        <input
          type="file"
          accept="audio/mp3"
          onChange={handleUpload}
          className="block mx-auto text-sm file:bg-gradient-to-r file:from-pink-500 file:to-blue-600 file:text-white file:px-5 file:py-3 file:rounded-lg file:border-none file:cursor-pointer file:shadow-md"
          aria-label="Upload MP3 file"
        />
       {file && <p className="mt-3 text-green-400 font-semibold">{'\u{1F3A7}'} Uploaded: {file.name}</p>}
      </div>

     <h2 className="text-3xl font-bold mb-6 text-center">{'\u{1F525}'} Choose Your Vibe</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
        {videoStyles.map((style, i) => (
          <motion.div
            key={style.name}
            whileHover={{ scale: 1.05 }}
            className={`rounded-2xl overflow-hidden border-4 transition-all duration-300 ${
              selectedStyle?.name === style.name ? "border-pink-500 shadow-xl" : "border-gray-600"
            }`}
            onClick={() => setSelectedStyle(style)}
            onMouseEnter={() => setHovered(i)}
            onMouseLeave={() => setHovered(null)}
            role="button"
            tabIndex={0}
            aria-label={`Select ${style.name} style`}
          >
            <CardContent className="p-2 bg-black">
              <div className="rounded-xl overflow-hidden h-48">
                {hovered === i ? (
                  <video
                    src={style.preview}
                    muted
                    loop
                    autoPlay
                    className="w-full h-full object-cover"
                    aria-hidden
                  />
                ) : (
                  <img
                    src={style.thumbnail}
                    alt={`${style.name} thumbnail preview`}
                    className="w-full h-full object-cover"
                  />
                )}
              </div>
              <div className="mt-3 text-center">
                <h3 className="text-xl font-semibold text-pink-400">{style.name}</h3>
                <p className="text-sm text-gray-400 mt-1">{style.description}</p>
              </div>
            </CardContent>
          </motion.div>
        ))}
      </div>

      <div className="mt-12 text-center">
        <Button
          onClick={handleGenerate}
          disabled={!file || !selectedStyle || isLoading}
          className="text-lg px-8 py-4 rounded-xl bg-gradient-to-r from-pink-500 to-blue-600 hover:from-blue-600 hover:to-pink-500 shadow-lg"
          aria-label="Generate music video"
        >
          {isLoading
            ? "🔄 Generating..."
            : file && selectedStyle
            ? "🚀 Generate Music Video"
            : "Upload & Choose Style"}
        </Button>
        {isLoading && (
          <p className="mt-4 text-yellow-300 animate-pulse">
            Hold tight... cooking up your visual masterpiece 🎬
          </p>
        )}
      </div>

      {generatedVideoUrl && (
        <div className="mt-10 text-center">
         <h3 className="text-2xl font-bold mb-4 text-green-400">{'\u{2705}'} Your Video Is Ready!</h3>
          <video
            src={generatedVideoUrl}
            controls
            className="w-full max-w-2xl mx-auto rounded-xl shadow-lg"
          />
        </div>
      )}
    </motion.div>
  );
}










