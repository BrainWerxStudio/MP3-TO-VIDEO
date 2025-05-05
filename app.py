import React, { useState } from "react";
import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Music, Film } from "lucide-react";

const videoStyles = [
  {
    name: "Anime Visualizer",
    thumbnail: "https://drive.google.com/uc?id=1kl73Idu3CSVCk3lOrqBy1q_OEwTNQ3fd",
    preview: "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",
    description: "Animated vibes, inspired by AMVs. Ideal for pop or K-rap."
  },
  {
    name: "Dreamscape AI",
    thumbnail: "https://drive.google.com/uc?id=1vNk1tWe4Bz4DTe2gdjzyefzyQX-Q3PQ5",
    preview: "https://drive.google.com/uc?id=1z9aiuKQloJuBO0mnzGbYNcnw21z83Ndw",
    description: "Surreal, AI-generated worlds. Works great with ambient or R&B."
  },
  {
    name: "Cyberpunk City",
    thumbnail: "https://drive.google.com/uc?id=1aU2oDqX5lEr7xOkwAsgATwgmFKhV8KfD",
    preview: "https://drive.google.com/uc?id=1Xfz9DzMJwtW7VLxE5G5yJFXbZemijydD",
    description: "Futuristic, neon-lit cityscapes. Great for synthwave or EDM."
  },
  {
    name: "Street Graffiti",
    thumbnail: "https://drive.google.com/uc?id=1ZfyZm_Ay-mquuyBpXlwzTZ8ivw2Gi_q9",
    preview: "https://drive.google.com/uc?id=1CSHAOyOP4RDTQOar8xVyrXuiQM7NeSfs",
    description: "Animated street art. Perfect for hip-hop or underground rap."
  },
  {
    name: "Cosmic Nebula",
    thumbnail: "https://drive.google.com/uc?id=1BfiZREooj8C39ePfmrMO4-G6ruuoyBNW",
    preview: "https://drive.google.com/uc?id=14cW4B1M2_dnVKB2GJnefJHQyiDxaAEtk",
    description: "Epic space visuals. Best for chill, spacey beats."
  },
  {
    name: "Matrix Code",
    thumbnail: "https://drive.google.com/uc?id=1CZOHKlTu1qI4Nh-2H67mwqDlWw3RkCz8",
    preview: "https://drive.google.com/uc?id=1e-FFFDndZWaKcQS5iY4uyNFHMD9yixkl",
    description: "Code rain + glitch. Killer for dark techno or cyber themes."
  },
  {
    name: "Urban Glitch",
    thumbnail: "https://drive.google.com/uc?id=1ll7_dJ9Zr18gLjk3D6u_eJxwIkFQKtQZ",
    preview: "https://drive.google.com/uc?id=1oS5JPDsobTVxiNdDNADZYjQjJjYfb3Sj",
    description: "Neon, chaotic motion. Great for trap or electronic beats."
  },
  {
    name: "VHS Retro",
    thumbnail: "https://drive.google.com/uc?id=1Wq_9L96zxNU5dKOpw64iQ8HbTiiih4pa",
    preview: "https://drive.google.com/uc?id=1eXd_rOi9M6AYF2yY7WOfxnoiZ0kXz3rm",
    description: "Old-school grain & 90s nostalgia. Best for lofi or synth."
  }
];

export default function MusicVideoGen() {
  const [selectedStyle, setSelectedStyle] = useState(null);
  const [hovered, setHovered] = useState(null);
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleGenerate = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 3000); // mock load
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
        />
        {file && <p className="mt-3 text-green-400 font-semibold">🎧 Uploaded: {file.name}</p>}
      </div>

      <h2 className="text-3xl font-bold mb-6 text-center">🔥 Choose Your Vibe</h2>
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
          >
            <CardContent className="p-2 bg-black">
              <div className="rounded-xl overflow-hidden h-48">
                {hovered === i ? (
                  <video
                    src={style.preview}
                    autoPlay
                    muted
                    loop
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <img
                    src={style.thumbnail}
                    alt={`${style.name} Thumbnail`}
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
        >
          {isLoading ? "🔄 Generating..." : file && selectedStyle ? "🚀 Generate Music Video"
