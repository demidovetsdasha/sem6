import React, { useEffect, useRef, useState } from "react";
import * as BABYLON from "babylonjs";

const vertices = [
  [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
  [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]
].map(v => [v[0]+0.5, v[1]+0.5, v[2]+0.5 ]);

const edges = [
  [0,1],[1,2],[2,3],[3,0], // Bottom
  [4,5],[5,6],[6,7],[7,4], // Top
  [0,4],[1,5],[2,6],[3,7]  // Sides
];

// Для каждой вершины храним связанные ребра
const vertexEdges = Array(8).fill().map((_, i) => 
  edges.reduce((acc, [a, b], idx) => 
    (a === i || b === i) ? [...acc, idx] : acc, [])
);

const faces = [
  { vertices: [4,5,6,7], normal: new BABYLON.Vector3(0, 0, 1) },
  { vertices: [0,1,2,3], normal: new BABYLON.Vector3(0, 0, -1) },
  { vertices: [1,5,6,2], normal: new BABYLON.Vector3(1, 0, 0) },
  { vertices: [0,3,7,4], normal: new BABYLON.Vector3(-1, 0, 0) },
  { vertices: [2,6,7,3], normal: new BABYLON.Vector3(0, 1, 0) },
  { vertices: [0,4,5,1], normal: new BABYLON.Vector3(0, -1, 0) }
];

const edgeMap = new Map();
faces.forEach((face, faceIndex) => {
  face.vertices.forEach((v, i) => {
    const a = v;
    const b = face.vertices[(i+1)%4];
    const key = `${Math.min(a,b)}-${Math.max(a,b)}`;
    edgeMap.set(key, [...(edgeMap.get(key) || []), faceIndex]);
  });
});

const edgeFaces = edges.map(edge => 
  edgeMap.get(`${Math.min(edge[0], edge[1])}-${Math.max(edge[0], edge[1])}`) || []
);

export default function BabylonCube() {
  const canvasRef = useRef(null);
  const [visibleEdges, setVisibleEdges] = useState({ contour: 0, corner: 0 });
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const engine = new BABYLON.Engine(canvas, true);
    const scene = new BABYLON.Scene(engine);
    scene.clearColor = new BABYLON.Color4(1,1,1,1);
    
    const camera = new BABYLON.ArcRotateCamera(
      "camera",
      -Math.PI/2,
      Math.PI/3,
      8,
      new BABYLON.Vector3(0.5, 0.5, 0.5),
      scene
    );
    camera.setPosition(new BABYLON.Vector3(0.5, 2, -5));
    camera.attachControl(canvas, true);
    cameraRef.current = camera;
    
    new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0,1,0), scene);
    sceneRef.current = scene;

    engine.runRenderLoop(() => scene.render());
    return () => engine.dispose();
  }, []);

  const findClosestVertex = (eye) => {
    let closestVertex = 0;
    let minDistance = Infinity;
    
    vertices.forEach((v, i) => {
      const vertexPos = new BABYLON.Vector3(...v);
      const distance = BABYLON.Vector3.DistanceSquared(eye, vertexPos);
      if (distance < minDistance) {
        minDistance = distance;
        closestVertex = i;
      }
    });
    
    return closestVertex;
  };

  const updateEdges = () => {
    if (!sceneRef.current) return;

    // Удаление старых линий
    sceneRef.current.meshes
      .filter(m => m.name.startsWith("edge-"))
      .forEach(m => m.dispose());

    const eye = cameraRef.current.position;
    
    // Определение видимых граней
    const visibleFaces = faces.map(face => {
      const facePoint = new BABYLON.Vector3(...vertices[face.vertices[0]]);
      const toCamera = eye.subtract(facePoint);
      return BABYLON.Vector3.Dot(face.normal, toCamera) > 0;
    });

    // Отрисовка контурных ребер (синие)
    let contourCount = 0;
    edges.forEach(([a, b], i) => {
      const adjacentFaces = edgeFaces[i];
      const visibleCount = adjacentFaces.filter(fi => visibleFaces[fi]).length;
      
      if (visibleCount === 1) {
        const points = [
          new BABYLON.Vector3(...vertices[a]),
          new BABYLON.Vector3(...vertices[b])
        ];
        const line = BABYLON.MeshBuilder.CreateLines(`edge-contour-${i}`, {
          points,
          updatable: true
        }, sceneRef.current);
        line.color = new BABYLON.Color3(0, 0, 1);
        line.enableEdgesRendering();
        line.edgesWidth = 2;
        contourCount++;
      }
    });
    // Поиск и отрисовка ближайшего угла (красные)
    const closestVertex = findClosestVertex(eye);
    const cornerEdges = vertexEdges[closestVertex];
    let cornerCount = 0;
    
    cornerEdges.forEach(edgeIdx => {
      const [a, b] = edges[edgeIdx];
      const points = [
        new BABYLON.Vector3(...vertices[a]),
        new BABYLON.Vector3(...vertices[b])
      ];
      const line = BABYLON.MeshBuilder.CreateLines(`edge-corner-${edgeIdx}`, {
        points,
        updatable: true
      }, sceneRef.current);
      line.color = new BABYLON.Color3(1, 0, 0);
      line.enableEdgesRendering();
      line.edgesWidth = 4;
      cornerCount++;
    });

    setVisibleEdges({ contour: contourCount, corner: cornerCount });
  };

  return (
    <div style={{ 
      width: '67vw', 
      height: '67vh', 
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      background: '#f0f0f0'
    }}>
      <div style={{
        width: '80%',
        height: '80%',
        border: '2px solid #333',
        borderRadius: '8px',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
        <button 
          onClick={updateEdges}
          style={{
            position: 'absolute',
            bottom: '40px',
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '12px 24px',
            background: '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '25px',
            cursor: 'pointer',
            fontSize: '16px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            display: 'flex',
            gap: '10px'
          }}
        >
          <span>Обновить видимость</span>
        </button>
      </div>
    </div>
  );
}