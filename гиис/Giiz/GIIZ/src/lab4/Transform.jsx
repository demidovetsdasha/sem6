import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

function Transform() {
  const containerRef = useRef(null);
  const [object, setObject] = useState(null);
  const [controlsEnabled, setControlsEnabled] = useState(false);
  
  // Three.js refs
  const scene = useRef(new THREE.Scene());
  const camera = useRef(new THREE.PerspectiveCamera(75, 600/400, 0.1, 1000));
  const renderer = useRef(null);
  const controls = useRef(null);
  const transformMatrix = useRef(new THREE.Matrix4());

  // Инициализация Three.js
  useEffect(() => {
    if (!containerRef.current) return;

    // Инициализация рендерера
    renderer.current = new THREE.WebGLRenderer({ antialias: true });
    renderer.current.setSize(600, 400);
    renderer.current.setClearColor(0xf0f0f0);
    containerRef.current.appendChild(renderer.current.domElement);

    // Настройка камеры
    camera.current.position.set(5, 5, 5);
    camera.current.lookAt(0, 0, 0);

    // Настройка освещения
    scene.current.add(new THREE.AmbientLight(0xffffff, 0.5));
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(5, 5, 5);
    scene.current.add(directionalLight);
    scene.current.add(new THREE.AxesHelper(5));

    // OrbitControls
    controls.current = new OrbitControls(camera.current, renderer.current.domElement);
    controls.current.enabled = controlsEnabled;

    // Анимация
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.current.render(scene.current, camera.current);
    };
    animate();

    // Очистка
    return () => {
      if (containerRef.current && renderer.current?.domElement) {
        containerRef.current.removeChild(renderer.current.domElement);
      }
      controls.current?.dispose();
    };
  }, []);

  // Загрузка 3D-объекта
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const lines = event.target.result.split('\n');
      const vertices = [];
      const faces = [];

      // Парсинг OBJ файла
      lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('v ')) {
          const [, x, y, z] = trimmed.split(' ').map(Number);
          vertices.push(new THREE.Vector3(x, y, z));
        }
        if (trimmed.startsWith('f ')) {
          const face = trimmed.split(' ').slice(1)
            .map(i => parseInt(i.split('/')[0]) - 1);
          faces.push(face);
        }
      });

      if (vertices.length === 0) return;

      // Создание геометрии
      const geometry = new THREE.BufferGeometry();
      geometry.setFromPoints(vertices);
      
      if (faces.length > 0) {
        geometry.setIndex(faces.flat());
        geometry.computeVertexNormals();
      }

      const material = new THREE.MeshPhongMaterial({
        color: 0x2194ce,
        wireframe: true,
        wireframeLinewidth: 2
      });

      const mesh = new THREE.Mesh(geometry, material);
      scene.current.add(mesh);
      setObject(mesh);
    };

    reader.readAsText(file);
  };

  // Обработка клавиатуры
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!object) return;

      const m = new THREE.Matrix4();
      const angle = Math.PI / 16;
      const step = 0.2;

      switch(e.key.toLowerCase()) {
        // Перемещение
        case 'w': m.makeTranslation(0, step, 0); break;
        case 's': m.makeTranslation(0, -step, 0); break;
        case 'a': m.makeTranslation(-step, 0, 0); break;
        case 'd': m.makeTranslation(step, 0, 0); break;
        case 'q': m.makeTranslation(0, 0, step); break;
        case 'e': m.makeTranslation(0, 0, -step); break;
        
        // Масштабирование
        case 'z': m.makeScale(1.1, 1.1, 1.1); break;
        case 'x': m.makeScale(0.9, 0.9, 0.9); break;
        
        // Поворот
        case 'i': m.makeRotationX(angle); break;
        case 'k': m.makeRotationX(-angle); break;
        case 'j': m.makeRotationY(angle); break;
        case 'l': m.makeRotationY(-angle); break;
        case 'u': m.makeRotationZ(angle); break;
        case 'o': m.makeRotationZ(-angle); break;
        
        // Отражение
        case 'r': m.makeScale(-1, 1, 1); break;
        case 't': m.makeScale(1, -1, 1); break;
        case 'y': m.makeScale(1, 1, -1); break;
        
        // Перспектива
        case 'p': 
          camera.current.position.set(5, 5, 5);
          camera.current.lookAt(0, 0, 0);
          break;
        case '[': 
          camera.current.fov -= 5; 
          camera.current.updateProjectionMatrix(); 
          break;
        case ']': 
          camera.current.fov += 5; 
          camera.current.updateProjectionMatrix(); 
          break;
      }

      transformMatrix.current.multiply(m);
      object.matrix = transformMatrix.current;
      object.matrixAutoUpdate = false;
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [object]);

  const containerStyle = {
    display: 'flex',
    gap: '25px',
    padding: '3px',
    backgroundColor: '#fff',
    borderRadius: '8px',
  };

  return (
    <div style={containerStyle}>
        <div ref={containerRef} style={{ width: '600px', height: '400px' }} />

      <div style={{ margin: '20px' }}>
        <input type="file" onChange={handleFileUpload} accept=".obj" />
        <div style={{ marginTop: '10px' }}>
          <label>
            <input 
              type="checkbox" 
              checked={controlsEnabled} 
              onChange={(e) => {
                setControlsEnabled(e.target.checked);
                controls.current.enabled = e.target.checked;
              }} 
            />
            Включить управление камерой
          </label>
        </div>
        <div style={{ marginTop: '10px' }}>
          Управление:
          <ul>
            <li>WASD/QE - перемещение</li>
            <li>Z/X - масштабирование</li>
            <li>IJKLUO - вращение</li>
            <li>R/T/Y - отражение</li>
            <li>P - сброс камеры</li>
            <li>[ ] - изменение FOV</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Transform;