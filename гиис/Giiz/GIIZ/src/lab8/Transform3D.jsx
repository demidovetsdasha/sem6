import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const Transform3D = () => {
  const containerRef = useRef(null);
  const [controlsEnabled, setControlsEnabled] = useState(false);
  
  // Three.js refs
  const scene = useRef(new THREE.Scene());
  const camera = useRef(new THREE.PerspectiveCamera(45, 600/400, 0.1, 1000));
  const renderer = useRef(null);
  const controls = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Инициализация рендерера
    renderer.current = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true
    });
    renderer.current.setSize(600, 400);
    renderer.current.setClearColor(0xffffff, 0);
    containerRef.current.appendChild(renderer.current.domElement);

    // Настройка камеры для вида "3 грани"
    camera.current.position.set(5, 5, 5);
    camera.current.lookAt(0, 0, 0);

    // Освещение
    scene.current.add(new THREE.AmbientLight(0xffffff, 0.8));
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(-5, 5, 5);
    scene.current.add(directionalLight);

    // Создание куба
    const geometry = new THREE.BoxGeometry(3, 3, 3);
    
    // Основной материал (белый)
    const material = new THREE.MeshPhongMaterial({
      color: 0xffffff,
      polygonOffset: true,
      polygonOffsetFactor: 1,
      polygonOffsetUnits: 1
    });

    // Геометрия для видимых ребер
    const edges = new THREE.EdgesGeometry(geometry, 30);
    const edgeMaterial = new THREE.LineBasicMaterial({ 
      color: 0x000000,
      linewidth: 2
    });

    const cube = new THREE.Mesh(geometry, material);
    const wireframe = new THREE.LineSegments(edges, edgeMaterial);

    const group = new THREE.Group();
    group.add(cube);
    group.add(wireframe);
    scene.current.add(group);

    // OrbitControls
    controls.current = new OrbitControls(camera.current, renderer.current.domElement);
    controls.current.enableDamping = true;
    controls.current.dampingFactor = 0.05;

    // Анимация
    const animate = () => {
      requestAnimationFrame(animate);
      controls.current.update();
      renderer.current.render(scene.current, camera.current);
    };
    animate();

    return () => {
      containerRef.current?.removeChild(renderer.current.domElement);
      controls.current?.dispose();
    };
  }, []);

  return (
    <div style={{ display: 'flex', gap: 20, padding: 20 }}>
      <div ref={containerRef} style={{ width: 600, height: 400 }} />
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        <label>
          <input
            type="checkbox"
            checked={controlsEnabled}
            onChange={(e) => {
              setControlsEnabled(e.target.checked);
              controls.current.enabled = e.target.checked;
            }}
          />
          Вращение камеры
        </label>
        <div style={{color: '#666', fontSize: '0.9em'}}>
          При повороте будут видны только 3 грани в угле
        </div>
      </div>
    </div>
  );
};

export default Transform3D;