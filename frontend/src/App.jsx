import { useState } from "react";
import { PuffLoader } from "react-spinners";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function App() {
  const [features, setFeatures] = useState([""]);
  const [prioritizedFeatures, setPrioritizedFeatures] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (index, value) => {
    const updated = [...features];
    updated[index] = value;
    setFeatures(updated);
  };

  const addFeature = () => {
    setFeatures([...features, ""]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("https://ai-feature-prioritization-tool.onrender.com/api/prioritize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(setPrioritizedFeatures(data));
        toast.success("✅ Successfully prioritized features!");
      } else {
        console.error("Error:", data.error);
        toast.error("❌ Failed to prioritize features.");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("❌ Error connecting to server.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-start py-10 px-4 sm:px-8 md:px-16">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-2 text-center">
        🛠️ AI Feature Prioritization Tool
      </h1>
      <p className="text-gray-500 mb-8 text-center">
        Upload your feature requests below!
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col items-center w-full max-w-lg space-y-4">
        {features.map((feature, idx) => (
          <input
            key={idx}
            type="text"
            value={feature}
            onChange={(e) => handleChange(idx, e.target.value)}
            placeholder={`Feature ${idx + 1}`}
            className="border border-gray-300 rounded-md p-3 w-full focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
          />
        ))}

<div className="flex flex-wrap justify-center gap-4 pt-4">
  <button
    type="button"
    onClick={addFeature}
    className="flex items-center justify-center gap-2 px-5 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-md transition transform hover:scale-105"
  >
    ➕ Add Feature
  </button>
  
  <button
    type="submit"
    className="flex items-center justify-center gap-2 px-5 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition transform hover:scale-105"
  >
    🚀 Prioritize
  </button>

  <button
    type="button"
    onClick={() => {
      setFeatures([""]);
      setResult("");
    }}
    className="flex items-center justify-center gap-2 px-5 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md transition transform hover:scale-105"
  >
    ♻️ Reset
  </button>
</div>

      </form>

      {loading && (
        <div className="mt-12 flex flex-col items-center">
          <PuffLoader color="#6366F1" size={80} />
          <p className="text-gray-400 mt-2">Loading AI magic...</p>
        </div>
      )}

{prioritizedFeatures.length > 0 && (
  <div style={{ width: '100%', height: 500, marginTop: '2rem' }}>
    <ResponsiveContainer>
      <ScatterChart
        margin={{ top: 40, right: 20, bottom: 40, left: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          type="number"
          dataKey="effort"
          name="Effort"
          domain={[1, 5]}
          tickCount={5}
        >
          <Label value="Effort (1=Low, 5=High)" position="insideBottom" dy={20} />
        </XAxis>
        <YAxis
          type="number"
          dataKey="impact"
          name="Impact"
          domain={[1, 5]}
          tickCount={5}
        >
          <Label value="Impact (1=Low, 5=High)" angle={-90} position="insideLeft" dx={-10} />
        </YAxis>

        {/* Quadrant Dividers */}
        <ReferenceLine x={3} stroke="gray" strokeDasharray="3 3" />
        <ReferenceLine y={3} stroke="gray" strokeDasharray="3 3" />

        {/* Tooltips */}
        <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ active, payload }) => {
          if (active && payload && payload.length) {
            const { feature, effort, impact } = payload[0].payload;
            return (
              <div style={{ background: 'white', border: '1px solid #ccc', padding: '10px' }}>
                <p><strong>{feature}</strong></p>
                <p>Effort: {effort}</p>
                <p>Impact: {impact}</p>
              </div>
            );
          }
          return null;
        }} />

        {/* Features */}
        <Scatter
          name="Features"
          data={prioritizedFeatures}
          fill="#8884d8"
          animationDuration={800}
        />
      </ScatterChart>
    </ResponsiveContainer>
  </div>
)}

  <div className="mt-12 text-gray-500 text-sm">
  <p>Made with ❤️ by BW</p>
  <p>Powered by OpenAI</p>
  </div>

      <ToastContainer />
    </div>
  );
}

export default App;
